from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.http import HttpResponse, HttpResponseRedirect
from orders.forms.order import OrderCreateForm
from ecomapp.models.shop import Product, Variants
from cart.models import CartItem, Cart
from orders.models import Order, OrderItem
from user.models import UserProfile
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
import weasyprint


def order_checkout(request):
    template = 'order/order_checkout.html'
    current_user = request.user
    cart_item = CartItem.objects.filter(user_id=current_user.id)
    cart = Cart.objects.get(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order_option = order_form.cleaned_data['order_option']
            if order_option == "user":
                order.email = profile.email
                order.phone = profile.phone
                order.first_name = profile.first_name
                order.last_name = profile.last_name
                order.father_name = profile.father_name
                order.city = profile.city
                # DELIVERY OPTION
                delivery_option = order_form.cleaned_data['delivery_option']
                if delivery_option == "delivery":
                    order.street = profile.street
                    order.house = profile.house
                    order.apartment = profile.apartment
                else:
                    order.warehouse_number = profile.warehouse_number
            else:
                order.email = order_form.cleaned_data['email']
                order.phone = order_form.cleaned_data['phone']
                order.first_name = order_form.cleaned_data['first_name']
                order.last_name = order_form.cleaned_data['last_name']
                order.father_name = order_form.cleaned_data['father_name']
                order.city = order_form.cleaned_data['city']

                # DELIVERY OPTION
                delivery_option = order_form.cleaned_data['delivery_option']
                if delivery_option == "delivery":
                    order.street = order_form.cleaned_data['street']
                    order.house = order_form.cleaned_data['house']
                    order.apartment = order_form.cleaned_data['apartment']
                else:
                    order.warehouse_number = order_form.cleaned_data['warehouse_number']

            order.comments = order_form.cleaned_data['comments']
            order.user_id = current_user.id
            ordercode = get_random_string(5).upper()
            order.code = ordercode

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart_item:
                detail = OrderItem()
                detail.order_id = order.id
                detail.user_id = current_user.id
                detail.product_id = item.product_id
                detail.quantity = item.quantity
                if item.product.variant == 'None':
                    detail.price = item.product.price
                else:
                    detail.price = item.variant.price
                detail.variant_id = item.variant_id
                detail.save()

                if item.product.variant == 'None':
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=item.product_id)
                    variant.quantity -= item.quantity
                    variant.save()

            # Сlear Сart and CartItem
            CartItem.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            Cart.objects.filter(user_id=current_user.id).delete()
            request.session['cart'] = 0

            payment_option = order_form.cleaned_data['payment_option']
            if payment_option == 'cash':
                messages.success(request, _("Ваше замовлення прийнято в обробку. Щиро дякую!"))
                return render(request, "order/order_success.html", {'ordercode': ordercode, })
            elif payment_option == 'card':
                return redirect(reverse('pay_liqpay'))
            else:
                messages.warning(request, _("Обрано недійсний варіант оплати"))
                HttpResponseRedirect("/checkout")
    else:
        order_form = OrderCreateForm()

    context = {
        'cart': cart,
        'cart_item': cart_item,
        'order_form': order_form,
        'profile': profile,
    }
    return render(request, template, context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response


