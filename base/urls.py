from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns =[
    path("",views.home,name='home'),
    path("product/form/", views.create_product,name ='product_form'),
    path('list/product/', views.list_product,name='list_product'),
    path("category/form/", views.create_catogery,name ='category_form'),
    path('list/category/', views.list_catogery,name='list_category'),
    path('delete-category/<int:pk>/', views.deleteCategory, name="delete-category"),
    path('edit-category/<int:pk>/', views.editCategory, name="edit-category"),
    path('edit-product/int:<pk>',views.editProduct, name= "edit-product"),
    path('delete-product/int:<pk>',views.deleteProduct, name= "delete-product"),
    path('addtocart/<int:product_id>',views.Addcart, name= "add-cart"),
    path('viewcart/',views.cart_detail, name="view-cart"),
    ]
