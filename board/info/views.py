from datetime import datetime

from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, CreateView, \
    DeleteView

from .models import Post, Comment_User


class PostList(ListView):
    model = Post
    template_name = 'base_page.html'
    context_object_name = 'post_all'
    ordering = ['-dateCreation'] # выводим статьи в обратном порядке по дате создания
    paginate_by = 10  # поставим постраничный вывод в 10 элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = f") . общее количество объявлений ->> {Post.objects.all().count()}"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_post'] = Comment_User.objects.filter(comment_post=context['post_detail'])
        return context

