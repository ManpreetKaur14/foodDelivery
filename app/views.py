from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='login')
def Userlogout(request):
    logout(request)
    return redirect('index')