from .forms import SubredditForm


def subreddit_form(request):
    return {'subreddit_form': SubredditForm(user=request.user)}
