from django import template
from ecomapp.models.shop import Category, Brand
from cart.models import CartItem
from home.models import Setting
from user.models import UserWishlist
from user.forms import EmailSignupForm

register = template.Library()


@register.simple_tag
def cartcount(userid):
    count = CartItem.objects.filter(user_id=userid).count()
    return count


@register.simple_tag
def wishlistcount(userid):
    return UserWishlist.objects.filter(parent_id=userid).count()


@register.simple_tag
def get_category():
    return Category.objects.filter(is_active=True)


@register.simple_tag
def get_brand():
    return Brand.objects.all()


@register.inclusion_tag('tags/setting_sidebar.html')
def get_setting_sidebar():
    setting = Setting.objects.get(pk=1)
    return {"setting": setting}


@register.inclusion_tag('tags/setting_footer.html')
def get_setting_footer():
    setting = Setting.objects.get(pk=1)
    return {"setting": setting}


@register.inclusion_tag('tags/subscribe.html')
def get_signup_form():
    signup_form = EmailSignupForm()
    return {"signup_form": signup_form}


