from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.muestra_datos, name='post_list'),
]