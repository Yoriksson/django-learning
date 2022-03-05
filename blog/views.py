from datetime import datetime
import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from blog.models import Blog, Profile, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from blog.forms import RegistrationForm, MyActivationCodeForm, CommentForm
from django.contrib.auth import authenticate, login, get_user_model

from newblog import settings


def main_page(request):
    posts = Blog.objects.all()
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # context = {
    #     'posts': posts
    # }
    return render(request, "blog/index.html", {'page_obj': page_obj})



def show_post(request, post_slug):
    post = get_object_or_404(Blog, slug=post_slug)
    context = {
        'form': CommentForm,
        'comments': Comment.objects.all(),
        'post': post,
        'title': post.title,
        'author': post.author,
        'time_update': post.time_update
    }

    if request.method == 'POST' and request.user.is_authenticated:

        if not Blog.objects.filter(slug=post_slug).exists():
            return HttpResponse(404)  # обработка ошибки пост не найден
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Blog.objects.get(slug=post_slug)
            Comment.objects.create(post=post, commenter=request.user, body=form.cleaned_data['body'])

            return render(request, 'blog/post.html', context=context)  # все хорошо, коммент сохранен
        return render(request, 'blog/post.html', context=context, )  # обработка ошибки форма не валидная

    return render(request, 'blog/post.html', context=context)


# class ShowPost():
#     model = Blog
#     template_name = 'blog/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'

# class RegisterUser(CreateView):
#     form_class = UserCreationForm
#     template_name = 'blog/register.html'
#     success_url = reverse_lazy('home')


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('/admin')

    if request.POST:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            my_password1 = form.cleaned_data.get('password1')

            code = generate_code()

            if Profile.objects.filter(code=code):
                # for p in Profile.objects.filter(code=code):
                #     p.delete()
                code = generate_code()

            message = code
            user = authenticate(username=username, password=my_password1)
            now = datetime.now()
            send_mail('код подтверждения', message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)

            form.save()
            u_f = User.objects.get(username=username, email=email, is_active=False)

            Profile.objects.create(user=u_f, code=code, date=now)

            if user and user.is_active:
                login(request, user)
                return redirect('/admin')
            else:  # тут добавить редирект на страницу с формой для ввода кода.
                form.add_error(None, 'Аккаунт не активирован')
                return redirect('/activation_code_form/')
                # return render(request, 'registration/register.html', {'form': form})

        else:
            return render(request, 'blog/register.html', {'form': form})
    else:
        return render(request, 'blog/register.html', {'form': RegistrationForm()})


def endreg(request):
    if request.user.is_authenticated:
        return redirect('/admin')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'blog/activation_code_form.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    # user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, profile.user)
                    profile.delete()
                    return redirect('/admin')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'blog/activation_code_form.html', {'form': form})
            else:
                return render(request, 'blog/activation_code_form.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'blog/activation_code_form.html', {'form': form})
