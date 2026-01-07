from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    def __str__(self):
        return self.content[:50]

    def clean(self):
        if self.deadline:
            compare_date = timezone.now()
            if self.deadline < compare_date:
                raise ValidationError(
                    {"deadline": "Deadline cannot be earlier than the creation date."}
                )
