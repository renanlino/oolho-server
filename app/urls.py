from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    url(r'^movements/$', views.MovementList.as_view()),
    url(r'^movements/(?P<pk>[0-9]+)/$', views.MovementDetail.as_view()),
    url(r'^sensors/$', views.SensorList.as_view()),
    url(r'^sensors/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
