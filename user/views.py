from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.utils import translation
from django.utils.translation import gettext_lazy as _

from ecomapp.models.shop import Product, ProductReview
from orders.models import Order, OrderItem

from user.models import UserWishlist, UserWishlistForm
from user.forms import *

import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=MAILCHIMP_EMAIL_LIST_ID
)


@login_required(login_url='/login')
def account_view(request):
    template = "user/user_profile.html"
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'profile': profile,
    }
    return render(request, template, context)


def registration_form(request):
    template = "account/signup.html"
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            new_user.username = username
            new_user.set_password(password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            login_user = authenticate(username=username, password=password)
            if login_user:
                login(request, login_user)
                # Create data in profile table for user
                current_user = request.user
                data = UserProfile()
                data.user_id = current_user.id
                data.image = "Users/user.png"
                data.save()
                messages.success(request, _("Ваш обліковий запис створено"))
                return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/user/signup')
    form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, template, context)


def login_form(request):
    template = "account/login.html"
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    current_user = request.user
                    userprofile = UserProfile.objects.get(user_id=current_user.id)
                    request.session['userimage'] = userprofile.image.url
                    request.session[translation.LANGUAGE_SESSION_KEY] = userprofile.language.code
                    request.session['currency'] = userprofile.currency.code
                    translation.activate(userprofile.language.code)
                    return HttpResponseRedirect('/'+userprofile.language.code)
                else:
                    messages.warning(request, _("Ваш обліковий запис неактивний"))
            else:
                messages.warning(request, _("Ім'я користувача та/або пароль, які ви вказали, є неправильними"))
                return HttpResponseRedirect('/user/login')
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
     }
    return render(request, template, context)


def logout_func(request):
    logout(request)
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
        del request.session['currency']
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Ваш обліковий запис оновлено'))
            return HttpResponseRedirect('/user')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user/user_update.html', context)


@login_required(login_url='/login')
def user_password_change(request):
    if request.method == 'POST':
        form = FormChangePassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Ваш пароль був успішно оновлений!'))
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        form = FormChangePassword(request.user)
        return render(request, 'user/user_password.html', {'form': form})


def user_password_reset(request):
    if request.method == 'POST':
        form = FormResetPassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.html"
                    context = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'PoliKram',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse(_('Invalid header found.'))
                    messages.success(request, _('На вашу скриньку надійшло повідомлення із інструкціями щодо скидання паролю.'))
                    return HttpResponseRedirect("/")
            messages.error(request, _('Введений E-mail не зареєстрований. Ввідіть зареєстрований E-mail!'))
    form = FormResetPassword()
    return render(request, 'account/password_reset_form.html', {'form': form})


@login_required(login_url='/login')
def user_orders(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id).order_by('id')
    count = Order.objects.filter(user_id=current_user.id).count()
    if orders.exists():
        order_item = OrderItem.objects.all()
        context = {
            'orders': orders,
            'order_item': order_item,
            'count': count,
        }
        return render(request, 'user/user_orders.html', context)
    messages.warning(request, _("У вас немає жодного замовлення."))
    return redirect(url)


@login_required(login_url='/login')
def user_order_detail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_item = OrderItem.objects.filter(order_id=id)
    context = {
        'order': order,
        'order_item': order_item,
    }
    return render(request, 'user/user_order_detail.html', context)


def user_comments(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    comments = ProductReview.objects.filter(user_id=current_user.id)
    if comments.exists():
        context = {
            'comments': comments,
        }
        return render(request, 'user/user_comments.html', context)
    messages.warning(request, _("У вас немає жодного відгуку."))
    return redirect(url)


@login_required(login_url='/login')
def user_deletecomment(request, id):
    current_user = request.user
    ProductReview.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, _('Коментар видалено..'))
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def user_wishlist_add(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')
        checkinvariant = UserWishlist.objects.filter(variant_id=variantid, parent_id=current_user.id)
        if checkinvariant:
            control = 1
        else:
            control = 0
    else:
        checkinproduct = UserWishlist.objects.filter(product_id=id, parent_id=current_user.id)
        if checkinproduct:
            control = 1
        else:
            control = 0
    if request.method == 'POST':
        form = UserWishlistForm(request.POST)
        if form.is_valid():
            if control == 1:
                if product.variant == 'None':
                    data = UserWishlist.objects.get(product_id=id, parent_id=current_user.id)
                else:
                    data = UserWishlist.objects.get(product_id=id, variant_id=variantid, parent_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = UserWishlist()
                data.parent_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, _("Товар доданий в список бажань"))
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = UserWishlist.objects.get(product_id=id, parent_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = UserWishlist()
            data.parent_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()
        messages.success(request, _("Товар доданий в список бажань"))
        return HttpResponseRedirect(url)


def user_wishlist(request):
    template = 'user/user_wishlist.html'
    current_user = request.user
    wishlist = UserWishlist.objects.filter(parent_id=current_user.id)
    if wishlist.exists():
        context = {
            'wishlist': wishlist,
        }
        return render(request, template, context)
    messages.warning(request, _("У вас немає листа бажань."))
    return redirect("/")


@login_required(login_url='/login')
def user_wishlist_del(request, id):
    UserWishlist.objects.filter(id=id).delete()
    messages.success(request, _("Ваш товар був видаленний із списку бажань"))
    return HttpResponseRedirect("/user/wishlist")


def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()


def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = UserSignup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, _("Ви вже підписані"))
            else:
                subscribe(form.instance.email)
                form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))