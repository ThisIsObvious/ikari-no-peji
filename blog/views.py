from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import Note_form

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, num):
    post = get_object_or_404(Post, pk=num)
    return render(request, 'blog/post_detail.html', {'post': post})

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
