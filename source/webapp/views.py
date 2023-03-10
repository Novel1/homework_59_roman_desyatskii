from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import TrackerForm
from webapp.models import Tracker

from webapp.forms import SearchForm

from webapp.models.project import Project

from webapp.forms import ProjectForm


# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
    model = Tracker
    context_object_name = 'tracker'
    ordering = ('created_at',)
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        if self.search_value:
            query = Q(summary__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            if not context['paginator'].count:
                context['error'] = "Задачи не найдены"
        return context


class TrackerDetail(TemplateView):
    template_name = 'tracker_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracker'] = get_object_or_404(Tracker, pk=kwargs['pk'])
        return context


class TrackerAdd(View):
    template_name = 'add_view.html'

    def get(self, request, *args, **kwargs):
        form = TrackerForm()
        return render(request, 'add_view.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TrackerForm(request.POST)
        if not form.is_valid():
            return render(request, 'add_view.html', {'form': form})
        else:
            tracker = form.save()
            return redirect('tracker_view', pk=tracker.pk)


class TrackerUpdateView(UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker_update.html'

    def get_success_url(self):
        return reverse('tracker_view', kwargs={'pk': self.object.pk})


class DeleteTrackerView(DeleteView):
    template_name = 'tracker_delete.html'
    model = Tracker
    success_url = reverse_lazy('index')


class ProjectView(ListView):
    template_name = 'project_index.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetail(DetailView):
    template_name = 'project_view.html'
    model = Project
    context_object_name = 'project'


class ProjectAdd(CreateView):
    template_name = 'project_add.html'
    model = Project
    form_class = ProjectForm

    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        return render(request, 'project_add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if not form.is_valid():
            return render(request, 'project_add.html', {'form': form})
        else:
            project = form.save()
            return redirect('project_view', pk=project.pk)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect('project_view', pk=project.pk)