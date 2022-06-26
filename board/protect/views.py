from django.shortcuts import render
from django.shortcuts import redirect # подчистить потом
from datetime import datetime
from django.core.mail import send_mail

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.views.generic import ListView, DetailView,\
     UpdateView, CreateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from info.models import Post, Comment_User, User
from .forms import PostForm, CommentForm



class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'protect/base_user_page.html'
    context_object_name = 'post_all'
    ordering = ['-dateCreation'] # выводим объявления в обратном порядке по дате создания
    paginate_by = 10  # поставим постраничный вывод в 10 элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = f") . общее количество объявлений ->> {Post.objects.all().count()}"
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'protect/post_user_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_post'] = Comment_User.objects.filter(comment_post=context['post_detail'])
        # выводим комментарии к объявлению
        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    template_name = 'protect/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('base_user_page')

    def form_valid(self, form):  # функция необходима для занесения вне формы автора объявления
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающее поле , которое обязательнщ
        fields.autor = self.request.user
        # сохраняем объявление в БД
        fields.save()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'protect/comment_create.html'
    form_class = CommentForm
    success_url = reverse_lazy('base_user_page')

    def form_valid(self, form, **kwargs):
        id = self.kwargs.get('pk')
        p_comm=Post.objects.get(pk=id)
        p_comm.sum_comment +=1 # увеличиваем количество комментариев на 1
        p_comm.save() # сохраняем изменения в модели
        fields = form.save(commit=False)
        fields.comment_post = p_comm  # добавляем в модель данные поля объявление
        fields.comment_autor = self.request.user # добавляем в модель данные поля автора комментария
        fields.save()
        send_mail(   # рассылаем уведомление автору объявления о новом комментарии
            subject=f'{p_comm.autor.username} у Вас новый комментарий',
            message=f'{p_comm.autor.username} Ваше объявление {p_comm.title} прокомментировали',
            from_email='Umba.dog@yandex.ru',
            recipient_list=[p_comm.autor.email],
            )
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'protect/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('base_user_page')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form, **kwargs):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.autor = self.request.user
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)


class UserPostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'protect/ads_user_page.html'
    context_object_name = 'post_user'
    ordering = ['-dateCreation'] # выводим статьи в обратном порядке по дате создания
    paginate_by = 10  # поставим постраничный вывод в 10 элемент

    def get_queryset(self):
        return Post.objects.filter(autor=self.request.user) # выводим объявления текущего пользователя


class UserPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'protect/ads_user_detail.html'
    context_object_name = 'ads_user_detail'
    success_url = reverse_lazy('ads_user_page') # указатель на страницу возврата

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_post'] = Comment_User.objects.filter(comment_post=context['ads_user_detail'])
        # вывод комметариев в данному объявлению
        return context


class CommentUserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'protect/ads_comment_delete.html'
    queryset = Comment_User.objects.all()
    success_url = reverse_lazy('ads_user_page')

    def form_valid(self, form, **kwargs):
        id = self.kwargs.get('pk')
        comm_us=Comment_User.objects.get(pk=id)
        comm_post=comm_us.comment_post
        comm_post.sum_comment -=1 # уменьшение на 1 числа комментариев к данному объявлению в связи с удалением
        # одного комментария
        comm_post.save()  # сохранение модели
        return super().form_valid(form)



class CommentUserDetailView(LoginRequiredMixin, DetailView):
    model = Comment_User
    template_name = 'protect/ads_comment_accept.html'
    context_object_name = 'ads_comment_detail'
    success_url = reverse_lazy('ads_user_page')

    def post(self, request, *args, **kwargs):
         id = self.kwargs.get('pk')
         comm_us =Comment_User.objects.get(pk=id)
         comm_us.comment_status= True # изменяем на true значит сомментарий акцептирован
         comm_us.save() # сохраняем изменения
         send_mail(   # рассылаем уведомление автору комментария  о принятии автором обьявления его комметария
            subject=f'{comm_us.comment_autor.username} Ваш комментарий принят',
            message=f'{comm_us.comment_autor.username} Ваш комментарий {comm_us.comment_text} принят автором объявления',
            from_email='Umba.dog@yandex.ru',
            recipient_list=[comm_us.comment_autor.email],
            )
         return redirect('/privat_page/ads_user/')


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    id =instance.id
    post_new =Post.objects.get(pk=id)
    all_user =User.objects.all()
    if ( post_new.status ==False ):
       print('***************Рассылка новой статьи*****************')
       for adresat in all_user:
           if (adresat.username !='admin' ):
             send_mail(
                 subject=f'Новое объявление от юзера ->> {post_new.autor.username}',
                 message=f'Новое объявление от юзера ->> {post_new.autor.username}',
                 from_email='Umba.dog@yandex.ru',
                 recipient_list=[adresat.email],
                )
           else:
             print ('Рассылка админу не производится')
       print('***************Рассылка завершена*******************')
       post_new.status =True
       post_new.save()
    else:
       print('Сообщение  уже было разослано')
