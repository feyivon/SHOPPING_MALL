from django.urls import path
from my_app.views import (homePage, addProduct, 
                          detailedPage, productEdit, 
                          deleteProduct, cartDetails, 
                          add_to_cart, confirmDelete,
                          delete_from_cart, clear_cart,
                          update_cart_quantity, save_cart,
                          view_saved_cart_details, view_saved_carts)

urlpatterns=[
    path('', homePage, name='homePage'),
    path('add/product/', addProduct, name='add_product'),
    path('product/<int:pk>/details/', detailedPage, name='detailed_page'),
    path('editproduct/<int:pk>/page/', productEdit, name='edit_product'),
    path('delete/product/<int:pk>/item/', deleteProduct, name='item_delete'),
    path('cart/details/page/', cartDetails, name='cart_list'),
    path('addtocart/<int:product_id>/product/', add_to_cart, name='add_to_cart'),
    path('confirm/delete/<int:pk>/product/', confirmDelete, name='confirm_delete'),
    path('removefromcart/<int:product_id>/', delete_from_cart, name='remove_from_cart'),
    path('clearall/cart/', clear_cart, name='clear_cart'),
    path('updatecart/<int:product_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path('save_cart/', save_cart, name='save_cart'),
    path('saved_carts/', view_saved_carts, name='view_saved_carts'),
    path('saved_cart/<int:saved_cart_id>/', view_saved_cart_details, name='view_saved_cart_details'),

]