
from django.urls import path
from store import views   # this imports your view functions from views.py

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('place_order/', views.place_order, name='place_order'),
    path('update_cart/',views.update_cart,name='update_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('order-success/', views.order_success, name='order_success'),

]
 # this means: when someone visits "/", show the home view

