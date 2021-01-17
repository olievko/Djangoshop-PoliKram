from django import template

from home.forms import ContactForm

register = template.Library()


@register.inclusion_tag('contactform/tags/contact_form.html', takes_context=True)
def contact_form(context, form=None, *args, **kwargs):
    if form is None:
        form = ContactForm()
    return {'form': form}
