from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('accounts/', include('allauth.urls')),
    path('login/',views.Userlogin, name='login'),
	path('update_item/', views.updateItem, name="update_item"),
    path('cart/', views.viewCart, name='viewCart')
]
