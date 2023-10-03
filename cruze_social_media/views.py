from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import RegistrationForm, PostForm, CommentForm
from django.http import HttpResponse
from django.db.models import Count, F
from .models import Post, Comment, UserProfile
# from django.contrib.auth.decorators import login_required


def forum(request):
    return render(request, 'forum.html')


# @login_required(login_url='cruze_social_media:login')
def home(request):
    user = request.user
    posts = Post.objects.annotate(comment_count=Count('comment'))
    Post.objects.update(views=F('views') + 1)
    context = {
        "user": user,
        "posts": posts,
    }
    rendered1 = render(request, 'base.html', context)
    rendered2 = render(request, 'home.html', context)
    combined_html = f"{rendered1.content.decode('utf-8')} {rendered2.content.decode('utf-8')}"
    response = HttpResponse(combined_html)
    return response


def view_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


def signup(request):
    form = RegistrationForm
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("cruze_social_media:home")
    return render(request, 'auth/signup.html', {'form': form})


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
        else:
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                return redirect("cruze_social_media:home")
            else:
                messages.error(request, "Invalid email or password.")

    return render(request, 'auth/signin.html')


def createpost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('cruze_social_media:home')

    else:
        print("something went wrong")
        form = PostForm()

    return render(request, "createpost.html", {"form": form, })


def display_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Get comments for the specific post
    comments = Comment.objects.filter(post=post)
    Post.objects.filter(pk=pk).update(views=F('views') + 1)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(f'/post/{pk}/')  # Use a relative URL
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "post.html", context)
