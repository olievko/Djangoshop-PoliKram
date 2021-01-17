from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.utils import translation
from home.models import Setting, SettingLang, Language, ContactMessage
from home.forms import ContactForm
from user.models import UserProfile


def selectlanguage(request):
    if request.method == 'POST':
        cur_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return HttpResponseRedirect("/" + lang)


def aboutus(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = get_object_or_404(Setting, pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {
        'setting': setting,
    }
    return render(request, 'about.html', context)


def warranty(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = get_object_or_404(Setting, pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {
        'setting': setting,
    }
    return render(request, 'warranty.html', context)


def shipmentpayment(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = get_object_or_404(Setting, pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {
        'setting': setting,
    }
    return render(request, 'shipmentpayment.html', context)


def purchasereturn(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = get_object_or_404(Setting, pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {
        'setting': setting,
    }
    return render(request, 'purchasereturn.html', context)


def contact(request):
    # currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0,'',currentlang)

    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            data = ContactMessage()
            data.contact_name = form.cleaned_data['contact_name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.save()
            cc_myself = form.cleaned_data['cc_myself']

            site = get_current_site(request)

            tpl = getattr(settings, 'CONTACTFORM_MSG_TEMPLATE', 'contactform/message.txt'),
            message = render_to_string(tpl, {
                'site': site,
                'contact_name': data.contact_name,
                'email': data.email,
                'subject': data.subject,
                'comment': data.comment,
                'cc_myself': cc_myself
            })

            recipients = settings.CONTACTFORM_RECIPIENTS

            if cc_myself:
                recipients.append(data.email)

            try:
                email = EmailMessage(
                        getattr(settings, 'CONTACTFORM_SUBJECT', _('Нове повідомлення')),
                        message,
                        getattr(settings, 'CONTACTFORM_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL),
                        recipients,
                        reply_to=[data.email])
                email.send(fail_silently=False)
            except BadHeaderError:
                 return HttpResponse('Invalid header found.')

            messages.success(request, _('Ваше повідомлення успішно надіслано. Дякую Вам !'))
            return HttpResponseRedirect('/')
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    form = ContactForm
    context = {
        'setting': setting,
        'form': form
    }
    return render(request, 'contactform/contact.html', context)


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)


@login_required(login_url='/login')
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language = Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    data = UserProfile.objects.get(user_id=curren_user.id)
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()
    return HttpResponseRedirect(lasturl)