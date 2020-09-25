from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path("", views.home_page, name="home"),
    path("user/<str:username>/posts", views.UserPostListView.as_view(), name="user_posts"),
    path("group/list", views.GroupListView.as_view(), name="group_list"),
    path("group/create", views.GroupCreateView.as_view(), name="group_create"),
    path("group/<slug>", views.GroupDetailView.as_view(), name="group_detail"),
    path("group/<slug>/members", views.GroupMembers.as_view(), name="group_members"),
    path("group/<slug>/delete", views.GroupDeleteView.as_view(), name="group_delete"),
    path("group/<slug>/join", views.join_group_view, name="group_join"),
    path("group/user/<str:username>/groups", views.UserGroupListView.as_view(), name="user_groups"),
    path("group/user/<str:username>/groups/folowing", views.UserGroupFolowingListView.as_view(), name="user_groups_folowing"),
    path("group/<slug>/posts", views.PostList.as_view(), name="post_list"),
    path("group/<slug>/posts/create", views.CreatePostView.as_view(), name="post_create"),
    path("group/<slug>/posts/<int:pk>/delete", views.DeletePost.as_view(), name="post_delete"),
    path("group/<slug>/posts/<int:pk>/edit", views.EditPostView.as_view(), name="post_edit"),
    path("group/<slug>/posts/<int:pk>/", views.PostDetailsView.as_view(), name="post_detail"),
    path("group/<slug>/posts/<int:pk>/like", views.like_post_view, name="post_like"),
]

