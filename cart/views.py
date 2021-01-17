from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from cart.forms.cart import ShopCartForm
from ecomapp.models.shop import Product, Variants
from cart.models import CartItem, Cart
from coupons.forms.coupons import CouponApplyForm
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _


@login_required(login_url='/login')
@require_POST
def add_to_cart_view(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Product.objects.get(pk=id)
    variant_id = request.POST.get('variantid')
    cart_qs = Cart.objects.filter(user_id=current_user.id)

    if product.variant != 'None':
        check_in_variant = CartItem.objects.filter(variant_id=variant_id, user_id=current_user.id)
        if check_in_variant:
            control = 1
        else:
            control = 0
    else:
        check_in_product = CartItem.objects.filter(product_id=id, user_id=current_user.id)
        if check_in_product:
            control = 1
        else:
            control = 0

    form = ShopCartForm(request.POST)
    if form.is_valid():
        if cart_qs.exists():
            cart = cart_qs[0]
            if control == 1:
                if product.variant == 'None':
                    cart_item = CartItem.objects.get(product_id=id, user_id=current_user.id)
                    cart_item.price = product.price
                else:
                    cart_item = CartItem.objects.get(product_id=id, variant_id=variant_id, user_id=current_user.id)
                    variant = Variants.objects.get(pk=variant_id)
                    cart_item.price = variant.price
                cart_item.quantity += form.cleaned_data['quantity']
                cart_item.save()
            else:
                cart_item = CartItem()
                cart_item.user_id = current_user.id
                cart_item.product_id = id
                cart_item.variant_id = variant_id
                cart_item.quantity = form.cleaned_data['quantity']
                if product.variant == 'None':
                    cart_item.price = product.price
                else:
                    variant = Variants.objects.get(pk=variant_id)
                    cart_item.price = variant.price
                cart_item.save()

                cart.items.add(cart_item)
        else:
            cart = Cart.objects.create(user_id=current_user.id)
            cart_item = CartItem()
            cart_item.user_id = current_user.id
            cart_item.product_id = id
            cart_item.variant_id = variant_id
            cart_item.quantity = form.cleaned_data['quantity']
            if product.variant == 'None':
                cart_item.price = product.price
            else:
                variant = Variants.objects.get(pk=variant_id)
                cart_item.price = variant.price
            cart_item.save()
            cart.items.add(cart_item)
    else:
        cart_item = CartItem()
        cart_item.user_id = current_user.id
        cart_item.product_id = id
        cart_item.variant_id = variant_id
        cart_item.quantity = form.cleaned_data['quantity']
        if product.variant == 'None':
            cart_item.price = product.price
        else:
            variant = Variants.objects.get(pk=variant_id)
            cart_item.price = variant.price
        cart_item.save()
        cart = cart_qs[0]
        cart.items.add(cart_item)
    messages.success(request, _("Товар доданий до кошика"))
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def remove_from_cart_view(request, id):
    current_user = request.user
    cart_qs = Cart.objects.filter(user_id=current_user.id)
    cart = cart_qs[0]
    cart_item = CartItem.objects.filter(id=id, user_id=current_user.id)[0]
    cart.items.remove(cart_item)
    cart_item.delete()
    messages.success(request, _("Ваш товар видалений з кошику."))
    return redirect("/cart")


@login_required(login_url='/login')
def add_single_item_to_cart(request, id):
    current_user = request.user
    product = Product.objects.get(id=id)
    if product.variant != 'None':
        variant_id = request.POST.get('variantid')
        cart_item = CartItem.objects.get(product_id=id, variant_id=variant_id, user_id=current_user.id)
    else:
        cart_item = CartItem.objects.get(product_id=id, user_id=current_user.id)
    cart_item.quantity += 1
    cart_item.save()
    messages.info(request, _("Кількість товару була оновлена."))
    return redirect("/cart")


@login_required(login_url='/login')
def remove_single_item_from_cart(request, id):
    current_user = request.user
    product = Product.objects.get(id=id)
    cart_qs = Cart.objects.filter(user_id=current_user.id)
    cart = cart_qs[0]
    if product.variant != 'None':
        variant_id = request.POST.get('variantid')
        cart_item = CartItem.objects.get(product_id=id, variant_id=variant_id, user_id=current_user.id)
    else:
        cart_item = CartItem.objects.filter(product_id=id, user_id=current_user.id)[0]

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart.items.remove(cart_item)
        cart_item.delete()
    messages.info(request, _("Кількість товару була оновлена."))
    return redirect("/cart")


def cart_view(request):
    template = "cart/cart.html"
    current_user = request.user
    cart_item = CartItem.objects.filter(user_id=current_user.id)
    if cart_item.exists():
        cart = Cart.objects.get(user_id=current_user.id)
        context = {
            'cart': cart,
            'cart_item': cart_item,
            'coupon_form': CouponApplyForm(),
        }
        return render(request, template, context)
    else:
        messages.warning(request, _("У вас немає жодного товару у кошику."))
        return redirect("/")
