from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from djangoshop.settings import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY
from django.views.generic import TemplateView, View

from orders.liqpay import LiqPay
from orders.models import Order
import weasyprint
from io import BytesIO


# CREATE LIQPAY PAYMENT
class PayView(TemplateView):
    template = 'payment/order_pay_liqpay.html'

    def get(self, request, *args, **kwargs):
        order_id = request.session['order_id']
        order = get_object_or_404(Order, id=order_id)
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'currency': 'UAH',
            'order_id': 'order_id',
            'version': '3',
            'sandbox': 0,
            'server_url': 'https://test.com/billing/pay-callback/',
        }

        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)

        order.paid = True
        order.save()
        subject = 'PoliKram - Рахунок № {}'.format(order.id)
        message = _('В цьому електронному листі прикріплено рахунок-фактуру на вашу нещодавну покупку.')
        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [order.email])
        html = render_to_string('order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()

        context = {
            'order': order,
            'signature': signature,
            'data': data,
        }
        return render(request, self.template, context)


# CONFIRM LIQPAY PAYMENT
@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):

    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)
        return HttpResponse()

