from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

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


@require_POST
def toggle_update_is_done(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        task = Task.objects.get(pk=pk)
        task.done = not task.done
        task.save()
        return HttpResponseRedirect(reverse_lazy("core:index"))
    except Task.DoesNotExist:
        return HttpResponse("Task not found")


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
