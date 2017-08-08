import pytest

from normandy.studies.api.v2.serializers import ExtensionSerializer
from normandy.studies.tests import ExtensionFactory


@pytest.mark.django_db()
class TestExtensionSerializer:
    def test_it_works(self):
        extension = ExtensionFactory()
        serializer = ExtensionSerializer(extension)

        assert serializer.data == {
            'id': extension.id,
            'name': extension.name,
            'xpi': extension.xpi.url
        }
