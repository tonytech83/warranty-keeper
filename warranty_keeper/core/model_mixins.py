from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteMixin:
    def delete(self, using=None, keep_parents=False):
        """Mark the object as deleted instead of removing it."""
        self.deleted = True
        self.save()