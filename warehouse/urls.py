from django.conf.urls import url

from warehouse import views


urlpatterns = [
    url('autocomplete', views.autocomplete, name='autocomplete'),
    url('refresh', views.refresh, name='refresh')
]