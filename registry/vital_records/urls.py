from django.conf.urls import url

from .views import common, birth

app_name = 'vital_records'
urlpatterns = [
    url(r'^$', common.index, name='index'),
    url(r'^birth/$', birth.IndexView.as_view(), name='birth.index'),
    url(r'^birth/(?P<pk>[0-9]+)/$', birth.DetailView.as_view(), name='birth.detail')
]
