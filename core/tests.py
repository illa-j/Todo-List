from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.forms import TaskForm
from core.models import Task, Tag


class ModelsTests(TestCase):
    def test_tag_name_field_max_length(self):
        self.assertEqual(Tag._meta.get_field("name").max_length, 150)

    def test_tag_str(self):
        self.assertEqual(str(Tag.objects.create(name="test")), "test")

    def test_task_content_field_max_length(self):
        self.assertEqual(Task._meta.get_field("content").max_length, 500)

    def test_task_str(self):
        self.assertEqual(
            str(
                Task.objects.create(
                    content="test",
                    deadline=timezone.now(),
                )
            ),
            "test",
        )

    def test_task_datetime_fields_validation(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(
                content="test",
                deadline=timezone.now() - timedelta(days=1),
            ).full_clean()


class FormsTests(TestCase):
    def test_task_form_contains_tags_field(self):
        form = TaskForm()
        self.assertIn("tags", form.fields)
        self.assertIsInstance(form.fields["tags"].widget, forms.CheckboxSelectMultiple)

    def test_task_form_contains_deadline_field(self):
        form = TaskForm()
        self.assertIn("deadline", form.fields)
        self.assertIsInstance(form.fields["deadline"].widget, forms.DateTimeInput)


class ViewsTests(TestCase):
    def test_index_list_view_template(self):
        res = self.client.get(reverse("core:index"))
        self.assertTemplateUsed(res, "core/index.html")

    def test_tag_list_view_template(self):
        res = self.client.get(reverse("core:tag-list"))
        self.assertTemplateUsed(res, "core/tag_list.html")

    def test_index_list_view_template_paginate(self):
        res = self.client.get(reverse("core:index"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_tag_list_view_template_paginate(self):
        res = self.client.get(reverse("core:tag-list"))
        self.assertTemplateUsed(res, "includes/pagination.html")

    def test_index_list_view_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:index"))
        self.assertEqual(res.context.get("paginator").per_page, 5)

    def test_index_tags_view_is_paginated_view_by_five(self):
        res = self.client.get(reverse("core:tag-list"))
        self.assertEqual(res.context.get("paginator").per_page, 5)
