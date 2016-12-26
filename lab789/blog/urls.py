from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^(\d+)/wall$", views.Wall.as_view(), name = "Wall"),
    url(r"^(\d+)/wall/(\d+)", views.del_post, name="DelPost"),
]