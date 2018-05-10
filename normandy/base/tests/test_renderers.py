from normandy.base.api.renderers import CanonicalJSONRenderer


class TestCanonicalJSONRenderer(object):
    def test_it_works(self):
        data = {'a': 1, 'b': 2}
        rendered = CanonicalJSONRenderer().render(data)
        assert rendered == b'{"a":1,"b":2}'
