from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Post, Comment, Category
from accounts.models import CustomUser
from django.db.models import Q

# 🏠 Homepage (recent posts + popular bloggers + categories)
def home(request):
    categories = Category.objects.all()[:10]
    recent = Post.objects.all().order_by('-created_at')[:6]
    popular_bloggers = User.objects.all()[:6]
    return render(request, 'posts/home.html', {
        'categories': categories,
        'posts': recent,
        'bloggers': popular_bloggers
    })


def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__icontains=query) |               
            Q(category__name__icontains=query)       
        ).distinct()

    return render(request, 'posts/search_results.html', {
        'query': query,
        'results': results
    })

# 📜 List all posts
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()  # ✅ fixed variable name
    return render(request, 'posts/post_list.html', {'posts': posts, 'categories': categories})


# 🧾 View post details + comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})


# ✍️ Create new post (no CSRF)
@csrf_exempt
def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_slug = request.POST.get('category', '').strip()
        tags = request.POST.get('tags', '').strip()
        media = request.FILES.get('media')

        category = None
        if category_slug:
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': category_slug}
            )

        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category,
            tags=tags
        )

        # ✅ File upload handling
        if media:
            fs = FileSystemStorage()
            filename = fs.save(media.name, media)
            post.media = filename
            post.save()

        return redirect('post_detail', pk=post.pk)

    categories = Category.objects.all()
    return render(request, 'posts/post_form.html', {'action': 'Create', 'categories': categories})


# ✏️ Edit post
@csrf_exempt
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You can't edit this post.")

    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.tags = request.POST.get('tags', post.tags)
        category_slug = request.POST.get('category', '')
        media = request.FILES.get('media')

        # ✅ Fixed wrong variable names and logic
        if category_slug:
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': category_slug}
            )
            post.category = category

        if media:
            fs = FileSystemStorage()
            filename = fs.save(media.name, media)
            post.media = filename

        post.save()
        return redirect('post_detail', pk=post.pk)

    categories = Category.objects.all()
    return render(request, 'posts/post_form.html', {'action': 'Edit', 'post': post, 'categories': categories})


# 🗑️ Delete post
@csrf_exempt
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You can't delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'posts/post_delete_confirm.html', {'post': post})


# 💬 Add comment
@csrf_exempt
def add_comment(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('posts/post_detail', pk=post.pk)
    
def user_posts(request, username):
    user_profile = get_object_or_404(CustomUser, username=username)
    sort = request.GET.get('sort', 'newest')

    posts = Post.objects.filter(author=user_profile)

    if sort == 'oldest':
        posts = posts.order_by('created_at')
    elif sort == 'popular':
        posts = posts.order_by('-views', '-likes')
    else:  # newest
        posts = posts.order_by('-created_at')

    return render(request, 'posts/user_posts.html', {
        'profile_user': user_profile,
        'posts': posts,
        'sort': sort,
    })
    
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/view_post.html', {'post': post})