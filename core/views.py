from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.detail import SingleObjectMixin

from core.forms import TaskForm
from core.models import Task, Tag


class IndexView(generic.ListView):
    model = Task
    template_name = "core/index.html"
    paginate_by = 5
    queryset = (
        Task.objects.all().prefetch_related("tags").order_by("done", "created_at")
    )


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("core:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("core:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("core:index")


class TagListView(generic.ListView):
    model = Tag
    paginate_by = 5


@method_decorator(require_POST, name="dispatch")
class UpdateStatusView(SingleObjectMixin, generic.View):
    model = Task

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.done = not self.object.done
        self.object.save(update_fields=["done"])
        return redirect("core:index")

class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("core:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("core:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("core:tag-list")
