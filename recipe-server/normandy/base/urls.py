from django.conf.urls import url

from normandy.base import views
from normandy.base.api import views as api_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/v2/service_info/', api_views.ServiceInfoView.as_view(), name='service-info'),
    url(r'^api/v1/user/me/', api_views.CurrentUserView.as_view(), name='current-user'),
]
