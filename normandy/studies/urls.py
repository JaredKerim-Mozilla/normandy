from django.conf.urls import url, include

from rest_framework import routers

from normandy.studies.api.v2.views import ExtensionViewSet


# API Router
router = routers.SimpleRouter()
router.register('extension', ExtensionViewSet)

app_name = 'studies'

urlpatterns = [
    url(r'^api/v2/', include(router.urls)),
]
