import hashlib

from django.utils import timezone

import factory

from normandy.base.tests import FuzzyUnicode
from normandy.base.utils import sri_hash
from normandy.recipes.models import (
    Action,
    ApprovalRequest,
    Client,
    Channel,
    Country,
    Locale,
    Recipe,
    RecipeRevision,
    Signature,
)


class ChannelFactory(factory.DjangoModelFactory):
    name = FuzzyUnicode()

    class Meta:
        model = Channel


class CountryFactory(factory.DjangoModelFactory):
    name = FuzzyUnicode()

    class Meta:
        model = Country


class LocaleFactory(factory.DjangoModelFactory):
    name = FuzzyUnicode()

    class Meta:
        model = Locale


class ActionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Action

    name = FuzzyUnicode()
    implementation = 'console.log("test");'

    @factory.lazy_attribute
    def implementation_hash(action):
        if action.implementation is not None:
            return sri_hash(action.implementation.encode(), url_safe=True)

    # It is important that the signature be based on the actual data, and not
    # some static value so that tests can make assertions against what data was
    # signed.

    @factory.post_generation
    def signed(self, create, extracted=False, **kwargs):
        if extracted:
            self.signature = SignatureFactory(data=self.canonical_json())
            self.signature.save()
            self.save()
        else:
            return None


class RecipeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Recipe

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class()
        obj.save()

        revision = RecipeRevisionFactory(**kwargs)
        revision.action.save()
        obj.revise(**revision.data)

        return obj

    @factory.post_generation
    def channels(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for channel in extracted:
                self.channels.add(channel)

    @factory.post_generation
    def countries(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for country in extracted:
                self.countries.add(country)

    @factory.post_generation
    def locales(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for locale in extracted:
                self.locales.add(locale)

    # This should always be before `enabled`
    @factory.post_generation
    def approver(self, create, extracted, **kwargs):
        if extracted:
            approval = ApprovalRequestFactory(revision=self.latest_revision)
            approval.approve(extracted, 'r+')

    # This should always be after `approver` as we require approval to enable a recipe
    @factory.post_generation
    def enabled(self, create, extracted, **kwargs):
        if extracted:
            self.enabled = True
            self.save()

    # NOTE: This should always be last or the signature gets erased.
    # It is important that the signature be based on the actual data, and not
    # some static value so that tests can make assertions against what data was
    # signed.
    @factory.post_generation
    def signed(self, create, extracted=False, **kwargs):
        if extracted:
            self.signature = SignatureFactory(data=self.canonical_json())
            self.signature.save()
            self.save()
        else:
            return None


class FuzzyIdenticonSeed(factory.fuzzy.FuzzyText):
    """A FuzzyText factory to generate identicon seeds."""

    def __init__(self, **kwargs):
        super().__init__(prefix='v1:', **kwargs)


@factory.use_strategy(factory.BUILD_STRATEGY)
class RecipeRevisionFactory(factory.DjangoModelFactory):
    class Meta:
        model = RecipeRevision

    name = FuzzyUnicode()
    action = factory.SubFactory(ActionFactory)
    recipe = factory.SubFactory(RecipeFactory)
    identicon_seed = FuzzyIdenticonSeed()


class ApprovalRequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = ApprovalRequest

    revision = factory.SubFactory(RecipeRevisionFactory)


class SignatureFactory(factory.DjangoModelFactory):
    class Meta:
        model = Signature
        exclude = ['data']

    data = b''
    signature = factory.LazyAttribute(lambda o: hashlib.sha256(o.data).hexdigest())
    public_key = 'MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEh+JqU60off8jnvWkQAnP/P4vdKjP0aFiK4rrDne5rsqNd4A4A/z5P2foRFltlS6skODDIUu4X/C2pwROMgSXpkRFZxXk9IwATCRCVQ7YnffR8f1Jw5fWzCerDmf5fAj5'  # noqa
    x5u = 'https://example.com/fake.x5u'


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    country = 'US'
    request_time = factory.LazyAttribute(lambda o: timezone.now)


ARGUMENTS_SCHEMA = {
    "required": ["surveyId", "surveys"],
    "properties": {
        "surveyId": {"type": "string"},
        "surveys": {
            "type": "array",
            "minItems": 1,
            "items": {
                "properties": {
                    "title": {"type": "string"},
                    "weight": {"type": "integer", "minimum": 1}
                },
                "required": ["title", "weight"]
            },
        },
    },
}


def fake_sign(datas):
    return [{'signature': hashlib.sha256(d).hexdigest()} for d in datas]
