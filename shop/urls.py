from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.products, name= "products"),
    path('create/', views.create_product, name='create_product'),
    path('<int:product_id>/edit/', views.product_edit, name= "product_edit"),
    path('<int:tweet_id>/delete/', views.product_del, name= "product_del"),
    path('account_details/', views.account_details, name='account_details'),
    path('register/',views.register, name= "register"),
    path('accounts/',include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)