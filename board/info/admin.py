from django.contrib import admin
from .models import Post, Comment_User

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment_User)
