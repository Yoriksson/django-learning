from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from newblog import settings

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")
    content = RichTextUploadingField(blank=True, verbose_name="Содержание статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время редактирования")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(BaseModel):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Пост")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    body = models.TextField(max_length=255, verbose_name="Текст комментария")
    time_published = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")



class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', default=None,
                                on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)
