from django.urls import path,include
from .views import store,RegisterView,cart,checkout,loginUser,logoutUser,updateItem,processOrder,registerorg,dashboard,addPlant
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',store,name="store"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('register/',RegisterView.as_view(),name='register'),
    path('register_seller/',registerorg,name='register_seller'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('update_item/',updateItem,name="update_item"),
    path('process_order/',processOrder,name="process_order"),
    path('dashboard/',dashboard,name="dashboard"),
    path('addplant/',addPlant,name="addplant"),

]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
