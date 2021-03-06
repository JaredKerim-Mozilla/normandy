import urllib.parse as urlparse

import pytest

from normandy.base.tests import Whatever
from normandy.recipes.tests import (
    ActionFactory,
    ApprovalRequestFactory,
    RecipeFactory,
    SignatureFactory,
    UserFactory,
)
from normandy.recipes.api.v1.serializers import (
    ActionSerializer,
    MinimalRecipeSerializer,
    RecipeSerializer,
    SignedRecipeSerializer,
    SignatureSerializer,
)


@pytest.mark.django_db()
class TestRecipeSerializer:
    def test_it_works(self, rf):
        recipe = RecipeFactory(arguments={"foo": "bar"})
        approval = ApprovalRequestFactory(revision=recipe.latest_revision)
        action = recipe.latest_revision.action
        serializer = RecipeSerializer(recipe, context={"request": rf.get("/")})

        assert serializer.data == {
            "name": recipe.latest_revision.name,
            "id": recipe.id,
            "last_updated": Whatever(),
            "enabled": False,
            "filter_expression": recipe.latest_revision.filter_expression,
            "revision_id": recipe.latest_revision.id,
            "action": action.name,
            "arguments": {"foo": "bar"},
            "is_approved": False,
            "latest_revision_id": recipe.latest_revision.id,
            "approved_revision_id": None,
            "approval_request": {
                "id": approval.id,
                "created": Whatever(),
                "creator": Whatever(),
                "approved": None,
                "approver": None,
                "comment": None,
            },
            "identicon_seed": Whatever.startswith("v1:"),
            "capabilities": sorted(recipe.latest_revision.capabilities),
        }


@pytest.mark.django_db()
class TestMinimalRecipeSerializer:
    def test_it_works(self, rf):
        recipe = RecipeFactory(approver=UserFactory(), arguments={"foo": "bar"})
        action = recipe.approved_revision.action
        serializer = MinimalRecipeSerializer(recipe, context={"request": rf.get("/")})

        assert serializer.data == {
            "name": recipe.approved_revision.name,
            "id": recipe.id,
            "filter_expression": recipe.approved_revision.filter_expression,
            "revision_id": str(recipe.approved_revision.id),
            "action": action.name,
            "arguments": {"foo": "bar"},
            "capabilities": sorted(recipe.approved_revision.capabilities),
            "uses_only_baseline_capabilities": False,
        }

    def test_capabilities_are_sorted(self, rf):
        # the extra_capabilities passed here are purposefully out of order
        recipe = RecipeFactory(
            approver=UserFactory(), arguments={"foo": "bar"}, extra_capabilities=["b", "a"]
        )
        serializer = MinimalRecipeSerializer(recipe, context={"request": rf.get("/")})

        capabilities = serializer.data["capabilities"]
        assert capabilities == sorted(capabilities)
        assert "a" in capabilities
        assert "b" in capabilities


@pytest.mark.django_db()
class TestActionSerializer:
    def test_it_uses_cdn_url(self, rf, settings):
        settings.CDN_URL = "https://example.com/cdn/"
        action = ActionFactory()
        serializer = ActionSerializer(action, context={"request": rf.get("/")})
        assert serializer.data["implementation_url"].startswith(settings.CDN_URL)


@pytest.mark.django_db()
class TestSignedRecipeSerializer:
    def test_it_works_with_signature(self, rf):
        recipe = RecipeFactory(approver=UserFactory(), signed=True)
        context = {"request": rf.get("/")}
        combined_serializer = SignedRecipeSerializer(instance=recipe, context=context)
        recipe_serializer = MinimalRecipeSerializer(instance=recipe, context=context)

        # Testing for shape of data, not contents
        assert combined_serializer.data == {
            "signature": {
                "signature": Whatever(),
                "timestamp": Whatever(),
                "x5u": Whatever(),
                "public_key": Whatever(),
            },
            "recipe": recipe_serializer.data,
        }

    def test_it_works_with_no_signature(self, rf):
        recipe = RecipeFactory(approver=UserFactory(), signed=False)
        action = recipe.approved_revision.action
        serializer = SignedRecipeSerializer(instance=recipe, context={"request": rf.get("/")})

        assert serializer.data == {
            "signature": None,
            "recipe": {
                "name": recipe.approved_revision.name,
                "id": recipe.id,
                "filter_expression": recipe.approved_revision.filter_expression,
                "revision_id": str(recipe.approved_revision.id),
                "action": action.name,
                "arguments": recipe.approved_revision.arguments,
                "capabilities": sorted(recipe.approved_revision.capabilities),
                "uses_only_baseline_capabilities": False,
            },
        }


@pytest.mark.django_db()
class TestSignatureSerializer:
    def test_it_works(self):
        signature = SignatureFactory()
        serializer = SignatureSerializer(instance=signature)

        assert serializer.data == {
            "signature": Whatever.regex(r"[a-f0-9]{40}"),
            "x5u": Whatever.startswith(signature.x5u),
            "timestamp": Whatever.iso8601(),
            "public_key": Whatever.regex(r"[a-zA-Z0-9/+]{160}"),
        }

    def test_it_cachebusts_x5u(self, settings):
        signature = SignatureFactory()

        # If none, do not cache bust
        settings.AUTOGRAPH_X5U_CACHE_BUST = None
        serializer = SignatureSerializer(instance=signature)
        url_parts = list(urlparse.urlparse(serializer.data["x5u"]))
        query = urlparse.parse_qs(url_parts[4])
        assert "cachebust" not in query

        # If set, cachebust using the value
        settings.AUTOGRAPH_X5U_CACHE_BUST = "new"
        serializer = SignatureSerializer(instance=signature)
        url_parts = list(urlparse.urlparse(serializer.data["x5u"]))
        query = urlparse.parse_qs(url_parts[4])
        assert "cachebust" in query
        assert len(query["cachebust"]) == 1
        assert query["cachebust"][0] == "new"
