from django.urls import path
from .views.shop import base_view, category_view, product_view, search, search_auto, add_review, ajaxcolor
from orders.views import order_checkout, admin_order_detail, admin_order_pdf
from cart.views import cart_view, add_to_cart_view, remove_from_cart_view, remove_single_item_from_cart, add_single_item_to_cart
from orders.pay_liqpay import PayView, PayCallbackView
from coupons.views import coupon_apply


urlpatterns = [

    path('', base_view, name='base'),
    # SHOP
    path('category/<slug:category_slug>/', category_view, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', product_view, name='product_detail'),
    path('search/', search, name='search'),
    path('search_auto/', search_auto, name='search_auto'),
    # ADD REVIEW
    path('review/<int:id>/add/', add_review, name='add_review'),
    # CART
    path('cart/', cart_view, name='cart_detail'),
    path('add/product/<int:id>', add_to_cart_view, name='add_to_cart'),
    path('remove/<int:id>/', remove_from_cart_view, name='remove_from_cart'),
    path('add-item/<int:id>/', add_single_item_to_cart, name='add_item_to_cart'),
    path('remove-item/<int:id>/', remove_single_item_from_cart, name='remove_item_from_cart'),
    path('add-coupon/', coupon_apply, name='add-coupon'),
    # ORDER
    path('checkout/', order_checkout, name='order_checkout'),
    # PAYMENT PROCESS
    path('pay/', PayView.as_view(), name='pay_liqpay'),
    path('payment_complete/', PayCallbackView.as_view(), name='payment_complete'),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),
    # AJAX COLOR
    path('ajaxcolor/', ajaxcolor, name='ajaxcolor'),
]
