from django.conf.urls import url
from . import views
import json


urlpatterns = [
    url(r'^author/(\d+)', views.Author_id.as_view(), name = 'author'),
    url(r'^authors/$', views.Authors, name = 'authors'),
    url(r'^$', views.main, name='main'),
]
