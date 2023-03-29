import os
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = settings.AUTH_USER_MODEL


def upload_subreddit_image(instance, filename):
    base, extension = filename.rsplit(".", 1)
    today = datetime.date.today()
    # image_path = f'foro/subreddit/{instance.name}/{today.year}/{today.month}/{today.day}/{instance.name}.{extension}'
    image_path = f'foro/subreddit/{instance.slug}/{today.year}/{today.month}/{today.day}/{instance.slug}.jpg'

    full_path = os.path.join(settings.MEDIA_ROOT, image_path)

    if os.path.exists(full_path):
        os.remove(full_path)
    print('se elimino')
    return image_path


def upload_post_image(instance, filename):
    base, extension = filename.rsplit(".", 1)
    today = datetime.date.today()
    # image_path = f'foro/subreddit/{instance.name}/{today.year}/{today.month}/{today.day}/{instance.name}.{extension}'
    image_path = f'foro/post/{instance.slug}/{today.year}/{today.month}/{today.day}/{instance.slug}.jpg'

    full_path = os.path.join(settings.MEDIA_ROOT, image_path)

    if os.path.exists(full_path):
        os.remove(full_path)
    print('se elimino')
    return image_path


# Representa una comunidad de reddit
class Subreddit(models.Model):
    '''Model definition for Subreddit.'''
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='updated')
    description = RichTextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='foro_subreddits')
    members = models.ManyToManyField(User, blank=True,
                                     related_name='sub_members')
    image = models.ImageField(upload_to=upload_subreddit_image, blank=True)

    class Meta:
        '''Meta definition for Subreddit.'''
        ordering = ['-created']
        verbose_name = 'Subreddit'
        verbose_name_plural = 'Subreddits'

    def __str__(self):
        return self.name
 
    @property
    def get_members_count(self):
        return self.members.count()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    '''Model definition for Post.'''
    title = models.CharField(max_length=100)
    body = RichTextUploadingField(blank=False)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_post_image, blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_liked',
                                        blank=True)
    users_dislike = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name='posts_disliked',
                                           blank=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    subreddit = models.ForeignKey(Subreddit,
                                  on_delete=models.CASCADE,
                                  related_name='posts')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts_created')

    class Meta:
        '''Meta definition for Post.'''
        ordering = ['-created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.title} ----> {self.subreddit}'

    @property
    def get_comments_count(self):
        return self.comments.count()

    @property
    def get_votes_count(self):
        upvotes = self.users_like.count()
        downvotes = self.users_dislike.count()
        return upvotes - downvotes


class Comment(models.Model):
    '''Model definition for Comment.'''
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments_created')
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='comments_liked',
                                        blank=True)
    users_dislike = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name='comments_disliked',
                                           blank=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='responses_comment')

    class Meta:
        '''Meta definition for Comment.'''

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author.get_display_name} on {self.post}'

    @property
    def get_children(self):
        return Comment.objects.filter(parent=self) \
                              .order_by('-created').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    @property
    def get_votes_count(self):
        upvotes = self.users_like.count()
        downvotes = self.users_dislike.count()
        return upvotes - downvotes
    
    def toJSON(self):
        children = [child.toJSON() for child in self.get_children]

        return {
            'id': self.id,
            'name': self.author.username,
            'thumbnail': self.author.get_display_thumbnail,
            'body': self.body,
            'children': children,
            'is_parent': self.is_parent,
            # convertir la fecha a una cadena ISO 8601
            'created': self.created.isoformat(),
            # convetir la fecha a una cadena ISO 8601
            # 'created': self.created.strftime('%Y-%m-%dT%H:%M:%SZ')
        }


    # @classmethod
    # def get_responses_comment(cls, comment_id):
    #     return cls.objects.filter(parent=comment_id) \
    #                       .order_by('-created').all()


    # def toJSON(self):
    #     item = model_to_dict(self)
    #     item['id'] = self.id
    #     item['name'] = self.name
    #     return item

