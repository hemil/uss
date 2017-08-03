from django.conf.urls import url

from .views import image_view, base_view, keys_view

urlpatterns = [
    url(r'^v1/ping/?$', base_view.ping, name='ping'),
    url(r'^v1/images/?$', image_view.image_handler, name='image_handler'),
    url(r'^v1/keys/?$', keys_view.key_handler, name='key_handler'),
    url(r'^v1/ping/?$', base_view.ping, name='ping'),
]
