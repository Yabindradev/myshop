from django.urls import path
from .import views

# app_name = 'catlog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('prooduct<int:id>/',views.product_detail, name='product_detail'),
    path('help', views.help, name='help'),
    path('login', views.login, name='login'),
    path('singup', views.singup, name='singup'),
    path('logout', views.logout, name='logout'),
    path('sell', views.sell, name='sell'),
    path('dmain', views.dmain, name='dmain'),
    path('dashbord_order/', views.dashbord_order, name='dashbord_order'),
    path('products', views.products, name='products'),
    path('create', views.create, name='create'), 
    path('category', views.category, name='category'),
    path('user_informaction', views.user_informaction, name="user_informaction"),
    path('cart_detail', views.cart_detail, name="cart_detail"),
    path('delete<int:id>/', views.product_delete, name="product_delete"),
    path('edit<int:id>/', views.product_edit, name="product_edit"),
    path('all_producst', views.all_products, name="all_products"),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
    path('user_account', views.user_account, name="user_account"),
    path('order_details', views.order_details, name="order_details"),
    path('order<int:id>/', views.order_details_admin, name="order_details_admin"),
    # path('checkout', views.checkout, name="checkout"),
    # path('create-checkout-session/',views.create_checkout_session, name='checkout'),
    path('user_order', views.user_order, name="user_order"),
    path('category_delete/<int:id>/', views.category_delete_list,
         name="category_delete_list"),
    path('categiry<int:id>/', views.category_edit, name="category_edit"),
    path('user_details', views.user_details, name="user_details"),
    
    
    path('customer_detiles', views.customer_detiles, name="customer_detiles"),
    
    
    
    path('order_delete<int:id>/', views.user_order_delete,
         name="user_order_delete"),
    
    
    path('generate_invoice', views.generate_invoice, name="generate_invoice"),
    
    path('user_order_detials', views.user_order_detials, name="user_order_detials"),
    
    
    path('dashbord_landing', views.dashbord_landing, name="dashbord_landing"),
    
    path('order<int:id>/', views.order_details_admin, name="order_details_admin"),
    
    path('generate_shipping_lable', views.generate_shipping_lable,
         name="generate_shipping_lable"),
    
    path('new_order', views.new_order, name="new_order"),
    
    path('shipped_order', views.shipped_order, name="shipped_order"),
    
    path('delivered_order', views.delivered_order, name="delivered_order"),
    
    path('admin_setting', views.admin_setting, name="admin_setting")

    ]

