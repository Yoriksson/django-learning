from django.contrib import admin
# from ckeditor.widgets import CKEditorWidget

from blog.models import Blog, Comment
from django import forms


class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['title', 'slug', 'author', 'time_create', 'time_update', 'is_published']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['commenter', 'time_published', 'body', 'post']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
# class BlogAdminForm(forms.ModelForm):
# content = forms.CharField(widget=CKEditorWidget())

# class Meta:
#     model = Blog
