from django.urls import path
from .views import PostList, PostDetailView
# импортируем наше представление

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # ссылка на конкретную новость

]