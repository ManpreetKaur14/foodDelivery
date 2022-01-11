from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

def index(request):
    banner=Menu.objects.filter(isBanner=True)
    popular=Menu.objects.filter(isPopular=True)
    menu=Menu.objects.all()
    if request.method=='GET':
        return render(request, 'index.html',{
            'banner':banner,
            'popular':popular,
            'menu':menu,
        })
    if request.method=='POST':
        term=request.POST.get('searchbar')
        if term=='':
            return render(request, 'index.html',{
                'error':'Menu not found',
                'banner':banner,
                'popular':popular,
                'menu':menu,
                'anchor':'dishes'
            })
        searchTerm=term.lower()
        searchTerm=searchTerm.split(' ')
        searchList=dict()
        tmp=Menu.objects.all()
        for i in searchTerm:
            for j in tmp:
                if i in j.searchTag:
                    if j in searchList:
                        searchList[j]+=1
                    else:
                        searchList[j]=1
        if searchList:
            searchList={k: v for k, v in sorted(searchList.items(), key=lambda item: item[1])}
            return render(request, 'index.html',{
                'term': term,
                'popular':searchList,
                'banner':banner,
                'menu':menu,
                'anchor':'dishes'

            })
        else:
            return render(request, 'index.html',{
                'error':f'No Result for {term}',
                'banner':banner,
                'popular':popular,
                'menu':menu,
                'anchor':'dishes'
            })


def Userlogin(request):
    if request.method=='POST':
        user=authenticate(username=request.POST.get('uname'), password=request.POST.get('psw'))
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html',{'error':'Account not active'})
        else:
            return render(request, 'login.html',{'error':'Invalid Login Credentials'})

    if request.user.is_authenticated:
            return redirect('index')
    return render(request, 'login.html')

def signUp(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'signup.html')
    if request.method=='POST':
        username=request.POST.get('uname')
        #! if the username already exists in the database
        if User.objects.filter(username=username).exists():
            return render(request,'signup.html',{'error':'Username already exists'})
        email=request.POST.get('mail')
        #! if the email already exists in the database
        if User.objects.filter(email=email).exists():
            return render(request,'signup.html',{'error':'Email already exists'})
        #! if the entered email is in valid format
        if not isValidMail(email):
                return render(request,'form.html',{'error':'Email not in proper format!'})
        #TODO: Password validation is to be done
        password=request.POST.get('psw')

        #? if all the data provided is valid: then register the user to the database and login the used into the server
        user=User.objects.create(username=username, email=email, password=password)
        user.set_password(password)
        user.save()
        #* Now authenticate and login the user to the server
        user=authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')

@login_required(login_url='login')
def Userlogout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def updateItem(request):
    if request.method=='GET':
        return JsonResponse('ERR: Not a GET endpoint', safe=False, status=403)
    data=json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    if action=='add':
        item=Menu.objects.get(dishId=productId)
        if item:
            # print('_________________incart_______________',Cart.objects.filter(item=item).count())
            if Cart.objects.filter(item=item, user=request.user).count()!=0:
                inCart=Cart.objects.get(item=item, user=request.user)
                inCart.qty+=1
                inCart.save()
                return JsonResponse(f'{inCart.item.dishName} quantity has been updated to {inCart.qty}', safe=False)
            model=Cart()
            model.user=request.user
            model.item=item
            model.save()
            return JsonResponse(f'{item.dishName} was added to the cart', safe=False)

        else:
            return JsonResponse('Item not found', safe=False, status=404)
    if action=='remove':
        item=Menu.objects.get(dishId=productId)
        if item:
            # print('_________________incart_______________',Cart.objects.filter(item=item).count())
            if Cart.objects.filter(item=item, user=request.user).count()!=0:
                inCart=Cart.objects.get(item=item, user=request.user)
                inCart.qty-=1
                inCart.save()
                return JsonResponse(f'{inCart.item.dishName} quantity has been updated to {inCart.qty}', safe=False, status=200)
            else:
                return JsonResponse(f'{incart.item.dishName} not present in the cart for the current user', status=404)
    if action=='delete':
        item=Menu.objects.get(dishId=productId)
        if item:
            if Cart.objects.filter(item=item, user=request.user).count()!=0:
                inCart=Cart.objects.get(item=item, user=request.user)
                inCart.delete()
                return JsonResponse(f'{inCart.item.dishName} was removed from thr cart', safe=False, status=200)
    else:
        return JsonResponse('ERR: 403', safe=False, status=403)

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
amount=0;
@login_required(login_url='login')
def viewCart(request):
    cart=Cart.objects.filter(user=request.user)
    context={'items':cart, 'total':len(cart)}
    if request.method=='GET':
        return render(request, 'cart.html', context=context)
    if request.method=='POST':
        currency = 'INR'
        global amount 
        amount= int(request.POST.get('amount'))*100  # Rs. 200
        # amount=20000
 
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        context['post']=True
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
    
        return render(request, 'cart.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        global amount
           
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
 
            # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        print('__________', result)
        if result is None:
                print('before')
                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                print('after')
                # render success page on successful caputre of payment
                print('_______payment success_________',request.user)
                deleteCart(request.user)
                return render(request, 'checkout.html')
        else:

            # if signature verification fails.
            return render(request, 'paymentfail.html')
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
def deleteCart(user):
    items=Cart.objects.filter(user=user)
    for i in items:
        i.delete()

#TODO: simple email validation added but to be improved
def isValidMail(mail):
    #test@test.com
    try:
        address,domain=mail.split('@')
    except ValueError as err:
        return False
    else:
        return True