from django.shortcuts import render

from apps.foro.models import Post
from apps.foro.forms import SubredditForm


def home(request):
    form = SubredditForm(user=request.user)
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'pages/home.html', context)
