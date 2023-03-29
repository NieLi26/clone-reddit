from django import forms
from django.utils.text import slugify
from ckeditor.widgets import CKEditorWidget

from .models import Subreddit, Post, Comment


# Every letter to Capitalize(charfield)
class Capitalize(forms.CharField):
    def to_python(self, value):
        return value.capitalize()


class SubredditForm(forms.ModelForm):
    name = forms.CharField(max_length=21,
                           widget=forms.TextInput(attrs={
                            'class': 'block w-full px-4 py-3 text-sm text-gray-700 bg-white border border-gray-200 rounded-md focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-40 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:focus:border-blue-300',
                            'placeholder': 'r/'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SubredditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subreddit
        fields = ('name', )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = ''.join(name.split())
        if Subreddit.objects.filter(name__iexact=name).exists():
            msg = "Ese nombre ya esta en uso"
            raise forms.ValidationError(msg)
        return name

    def save(self, commit=True):
        subreddit = super().save(commit=False)
        name = ''.join(subreddit.name.split())
        subreddit.name = name
        subreddit.slug = slugify(subreddit.name)
        subreddit.created_by = self.user
        if commit:
            subreddit.save()
        return subreddit


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
                                                   'class': 'rounded-lg  flex-1 appearance-none border border-gray-700 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm text-base focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
                                                   'placeholder': 'Title'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.subreddit = kwargs.pop('subreddit', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'body')

    def save(self, commit=True):
        post = super().save(commit=False)
        post.slug = slugify(post.title)
        post.subreddit = self.subreddit
        post.author = self.user
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

