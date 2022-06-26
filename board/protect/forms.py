from django.forms import ModelForm, BooleanField
from info.models import Post, Comment_User

# создаем модельную форму

class PostForm(ModelForm):
    # в класс мета заносим модель и нужные нам поля
    class Meta:
        model=Post
        fields=['title', 'text','category','upload_image','upload_file',]


class CommentForm(ModelForm):
    # в класс мета заносим модель и нужные нам поля
    class Meta:
        model=Comment_User
        fields=['comment_text']


