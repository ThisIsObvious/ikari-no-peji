from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Manga, Page
from .forms import Note_form
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, num):
    post = get_object_or_404(Post, pk=num)
    return render(request, 'blog/post_detail.html', {'post': post})

def manga_general(request, num):
    manga = get_object_or_404(Manga, pk=num)
    return render(request, 'blog/manga_general.html', {'manga': manga})
    
def manga_page(request, manga, numb):
    manga = get_object_or_404(Manga, pk=manga)
    page = get_object_or_404(Page, pk=numb)
    return render(request, 'blog/manga_page.html', {'manga': manga}, {'page': page})

@login_required
def post_new(request):
    if request.method == "POST":
        form = Note_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', num=post.pk)
    else:
        form = Note_form()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required    
def post_edit(request, num):
    post = get_object_or_404(Post, pk=num)
    if request.method == "POST":
        form = Note_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', num=post.pk)
    else:
        form = Note_form(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required    
def post_delete(request, num):
    post = get_object_or_404(Post, pk=num)
    post.delete()
    return redirect('blog.views.post_list')
