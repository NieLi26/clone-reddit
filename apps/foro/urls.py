from django.urls import path

from . import views

app_name = "foro"

urlpatterns = [
     # post
     path("r/<str:subreddit>/post/create/",
          views.PostCreateView.as_view(),
          name="subreddit_post_create"),
     path("r/<str:subreddit>/post/<int:year>/<int:month>/<int:day>/<slug:post>/",
          views.PostDetailView.as_view(),
          name="subreddit_post_detail"),
     path('post/like/',
          views.PostLike.as_view(),
          name='post_like'),

     # subreddit
     path("subreddit/create/",
          views.SubredditCreateView.as_view(),
          name="subreddit_create"),
     path("subreddit/r/<str:name>/",
          views.SubredditDetailView.as_view(),
          name="subreddit_detail"),

     # comment
     path("subreddit/post/comment-json/",
          views.CommentCreateListView.as_view(),
          name="comment_json"),
]
