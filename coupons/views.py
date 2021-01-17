from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from coupons.models import Coupon
from coupons.forms.coupons import CouponApplyForm
from cart.models import Cart
from django.utils.translation import gettext_lazy as _


@require_POST
def coupon_apply(request):
    now = timezone.now()
    url = request.META.get('HTTP_REFERER')
    form = CouponApplyForm(request.POST or None)
    if form.is_valid():
        try:
            code = form.cleaned_data.get('code')
            current_user = request.user
            cart = Cart.objects.get(user_id=current_user.id)
            cart.coupon = Coupon.objects.get(code__iexact=code,
                                             valid_from__lte=now,
                                             valid_to__gte=now,
                                             active=True)
            cart.save()
            messages.success(request, _("Купон успішно додано"))
            return redirect(url)
        except Coupon.DoesNotExist:
            messages.info(request, _("Цього купону не існує"))
            return redirect(url)
