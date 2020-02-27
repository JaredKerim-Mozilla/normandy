from datetime import timedelta

import markus
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from normandy.recipes.models import Recipe
from normandy.recipes.exports import RemoteSettings


metrics = markus.get_metrics("normandy.signing.recipes")


class Command(BaseCommand):
    """
    Update signatures for enabled Recipes that have no signature or an old signature
    """

    help = "Update Recipe signatures"
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--force", action="store_true", help="Update signatures for all recipes"
        )

    def handle(self, *args, force=False, **options):
        remote_settings = RemoteSettings()

        if force:
            recipes_to_update = Recipe.objects.only_enabled()
        else:
            recipes_to_update = self.get_outdated_recipes()

        count = recipes_to_update.count()
        any_baseline = False
        if count == 0:
            self.stdout.write("No out of date recipes to sign")
        else:
            self.stdout.write(f"Signing {count} recipes:")
            for recipe in recipes_to_update:
                self.stdout.write(" * " + recipe.approved_revision.name)
                recipe.update_signature()
                recipe.save()
                remote_settings.publish(recipe, approve_changes=False)
                if recipe.uses_only_baseline_capabilities():
                    any_baseline = True
            # Approve all Remote Settings changes.
            remote_settings.approve_changes(baseline=any_baseline)

        metrics.gauge("signed", count, tags=["force"] if force else [])

        recipes_to_unsign = Recipe.objects.only_disabled().exclude(signature=None)
        count = recipes_to_unsign.count()
        if count == 0:
            self.stdout.write("No disabled recipes to unsign")
        else:
            self.stdout.write(f"Unsigning {count} disabled recipes:")
            for recipe in recipes_to_unsign:
                self.stdout.write(" * " + recipe.approved_revision.name)
                sig = recipe.signature
                recipe.signature = None
                recipe.save()
                sig.delete()

        metrics.gauge("unsigned", count, tags=["force"] if force else [])
        self.stdout.write("all signing done")

    def get_outdated_recipes(self):
        outdated_age = timedelta(seconds=settings.AUTOGRAPH_SIGNATURE_MAX_AGE)
        outdated_filter = Q(signature__timestamp__lt=timezone.now() - outdated_age)
        missing_filter = Q(signature=None)
        return Recipe.objects.only_enabled().filter(outdated_filter | missing_filter)
