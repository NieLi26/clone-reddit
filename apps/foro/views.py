from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404


from .models import Post, Subreddit, Comment
from .forms import SubredditForm, PostForm, CommentForm


class PostDetailView(View):
    def get(self, request, post, year, month, day, **kwargs):
        post = get_object_or_404(Post,
                                 slug=post,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)

        # List of active comments for this post
        comments = post.comments.filter(active=True)

        # Form for users to comment
        form = CommentForm()
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'foro/post/detail.html', context)


class CommentCreateListView(View):
    def post(self, request, *args, **kwargs):
        response = {}
        try:
            post_slug = request.POST.get('slug')
            comment_parent = request.POST.get('parent')
            # print(int(comment_parent))
            post = Post.objects.get(slug=post_slug)
            action = request.POST.get('action')
            if action == 'create_comment':
                # create comment
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.author = request.user
                    comment.post = post
                    comment_instance = Comment.objects.get(id=comment_parent)
                    comment.parent = comment_instance
                    comment.save()
                    response['status'] = 'ok'
                else:
                    response['status'] = 'error'
                    print(form.errors)
            else:
                # List of active comments for this post
                data = [i.toJSON() for i in post.comments.filter(active=True)]
                response['data'] = data
        except Post.DoesNotExist:
            response['error'] = 'Post does not exist'
        except Exception as e:
            print(str(e))
            response['error'] = 'Unexpected error'
        # else:
        #     response['error'] = 'Invalid option'
        return JsonResponse(response)


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            'posts': posts,
        }
        return render(request, 'foro/post/list.html', context)


class PostCreateView(View):
    def get(self, request, subreddit):
        subreddit = get_object_or_404(Subreddit,
                                      name=subreddit)
        form = PostForm(user=request.user,
                        subreddit=subreddit)
        context = {
            'form': form,
            'subreddit': subreddit
        }
        return render(request, 'foro/post/create.html', context)

    def post(self, request, subreddit):
        subreddit = get_object_or_404(Subreddit,
                                      name=subreddit)
        form = PostForm(request.POST,
                        user=request.user,
                        subreddit=subreddit)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('foro:subreddit_detail',
                                    args=[post.subreddit.name]))
        context = {
            'form': form,
            'subreddit': subreddit
        }
        return render(request, 'foro/post/create.html', context)


class PostLike(View):
    def post(self, request, *args, **kwargs):
        post_slug = request.POST.get('slug')
        action = request.POST.get('action')
        like_exists = None
        dislike_exists = None
        if post_slug and action:
            try:
                post = Post.objects.get(slug=post_slug)
                user_like = post.users_like \
                                .filter(pk=request.user.pk) \
                                .exists()
                user_dislike = post.users_dislike \
                                   .filter(pk=request.user.pk) \
                                   .exists()
                if action == 'like':
                    if user_dislike:
                        post.users_like.add(request.user)
                        post.users_dislike.remove(request.user)
                        like_exists = True
                        dislike_exists = False
                    else:
                        if user_like:
                            post.users_like.remove(request.user)
                            like_exists = False
                            dislike_exists = False
                        else:
                            post.users_like.add(request.user)
                            like_exists = True
                            dislike_exists = False
                else:
                    if user_like:
                        post.users_dislike.add(request.user)
                        post.users_like.remove(request.user)
                        like_exists = False
                        dislike_exists = True
                    else:
                        if user_dislike:
                            post.users_dislike.remove(request.user)
                            like_exists = False
                            dislike_exists = False
                        else:
                            post.users_dislike.add(request.user)
                            like_exists = False
                            dislike_exists = True
                return JsonResponse({'status': 'ok',
                                     'likes': post.users_like.count(),
                                     'like_exists': like_exists,
                                     'dislike_exists': dislike_exists,
                                     'dislikes': post.users_dislike.count()})
            except Post.DoesNotExist:
                pass
        return JsonResponse({'status': 'error'})


@method_decorator(require_POST, name='dispatch')
class SubredditCreateView(LoginRequiredMixin, View):
    # def get(self, request, *args, **kwargs):
    #     form = SubredditForm(user=request.user)
    #     context = {
    #         'form': form,
    #     }
    #     return render(request, 'foro/subreddit/create.html', context)

    def post(self, request, *args, **kwargs):
        form = SubredditForm(request.POST, user=request.user)
        if form.is_valid():
            subreddit = form.save()
            return redirect(reverse('foro:subreddit_detail', args=[subreddit.name]))
        # context = {
        #     'form': form,
        # }
        return redirect('pages:home')


class SubredditDetailView(LoginRequiredMixin, View):
    def get(self, request, name):
        subreddit = Subreddit.objects.get(name=name)
        context = {
            'subreddit': subreddit,
        }
        return render(request, 'foro/subreddit/detail.html', context)

