from django.conf.urls import url

from . import views

app_name = 'vital_records'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
