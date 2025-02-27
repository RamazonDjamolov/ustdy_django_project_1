from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import CustomUser
from .models import Post
from .forms import PostModelForm
from django.core.paginator import Paginator


@login_required
def post_list(request):
    q = request.GET.get("q")
    posts = Post.objects.for_user(request.user)
    if q and q != "None":
        posts = Post.objects.search(request.user, q)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    data = {
        'q': q,
        'posts': posts,
    }
    return render(request, 'list.html', context=data)


@login_required
def post_detail(request, id):
    if id:
        post = Post.objects.get(pk=id)
        return render(request, 'detail.html', {'post': post})
    return render(request, 'list.html')


@login_required
def delete_post(request, id):
    if id:
        post = Post.objects.get(pk=id)
        post.delete()
    return redirect('posts:list')


@login_required
def edit_post(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        forms = PostModelForm(request.POST, instance=post)
        if forms.is_valid():
            forms.save()
            return redirect("posts:list")
        return render(request, "edit.html", {"forms": forms, "post": post})
    post = Post.objects.get(pk=id)
    forms = PostModelForm(instance=post)
    return render(request, "edit.html", context={"post": post, "forms": forms})


@login_required
def create(request):
    if request.method == 'POST':
        forms = PostModelForm(request.POST)

        if forms.is_valid():
            post = forms.save(commit=False)
            post.author = CustomUser.objects.get(pk=request.user.pk)
            forms.save()
            return redirect(reverse('posts:list'))
        return render(request, "create.html", {"forms": forms})
    forms = PostModelForm()
    return render(request, "create.html", {"forms": forms})
