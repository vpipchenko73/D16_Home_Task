from django.urls import path

from .views import PostList, PostDetailView,\
    PostCreateView, CommentCreateView, PostUpdateView,\
    UserPostList, UserPostDetailView, CommentUserDeleteView,\
    CommentUserDetailView


urlpatterns = [
    path('', PostList.as_view(), name='base_user_page'),
    path('ads_user/', UserPostList.as_view(), name='ads_user_page'),
    path('ads_user/<int:pk>', UserPostDetailView.as_view(), name='ads_user_detail'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_user_detail'), # ссылка на конкретную новость
    path('create/', PostCreateView.as_view(), name='post_create'),#ссылка на создание новости
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('comment/<int:pk>', CommentCreateView.as_view(), name='comment_create'),#ссылка на создание новости
    path('comment_del/<int:pk>', CommentUserDeleteView.as_view(), name='ads_comment_delete'),
    path('accept/<int:pk>', CommentUserDetailView.as_view(), name='ads_comment_accept'),
]