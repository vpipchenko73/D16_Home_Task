from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post (models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('hial', 'Хилы'),
        ('dd', 'ДД'),
        ('torgashi', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quiest', 'Квестигры'),
        ('kuznetz', 'Кузнецы'),
        ('kojevnik', 'Кожевники'),
        ('zelpovar', 'Зельевары'),
        ('masterzak', 'Мастера заклинаний'),
    )

    dateCreation = models.DateField(auto_now_add=True )
    title = models.CharField(max_length=128)
    text = models.TextField()
    category = models.CharField(max_length=10, choices=TYPE, default='tank')
    upload_image = models.ImageField(upload_to='upload_image/',blank= True)
    upload_file = models.FileField(upload_to='upload_file/', blank= True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    sum_comment = models.SmallIntegerField(default=0)
    status = models.BooleanField(default= False)

    def __str__(self):
       return f"{self.title[0:16]} / {self.text[0:32]}{'...'} Автор- {self.autor}"


class Comment_User(models.Model):
    comment_dateCreation = models.DateField(auto_now_add=True )
    comment_text = models.TextField()
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_autor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_status = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.comment_text[0:32]}{'...'} Автор- {self.comment_autor} Post- {self.comment_post}"


