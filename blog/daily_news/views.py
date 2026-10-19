from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def homepage(request): # view function
    # retrieve all the blog posts 
    # from the database
    blog_posts = Blog.objects.all()

    return render(request,
                  "daily_news/homepage.html", 
                  context={'blogs': blog_posts}
                )

@login_required
def blog_post(request):
    form = BlogForm()

    # If the user submits a form
    if request.method == "POST":
        # Collect all the data input
        form = BlogForm(request.POST)
        # checks if the input is correct
        if form.is_valid():
            # save the data to the database
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # what next?
            # redirect
            return redirect("home")


    return render(request,
                  "daily_news/create-blog.html", {"form": form}
                  )

# get the id
# Check the db to see if there's any blog post with that ID exist
# conditionally check if it exists:
    # Render the page with the blog post
# else
    # Redirect the user to /not_found
def article(request, pk):
    # Scan through the blog table
    # and get  blog_posts whose its ID
    # is the same as the pk
    blog_posts = Blog.objects.filter(id=pk)

    if blog_posts.exists():
        return render(request,
                      "daily_news/article.html",
                      context={"blog": blog_posts.first()}
                      )
    else:
        return redirect("/not_found")

def not_found(request): 
    return HttpResponse("Not found")

@login_required
def edit_blog(request, pk):
    # Retrieved all blog posts that shared/have the id
    # filter() Returns QuerySet
    blog_posts = Blog.objects.filter(id=pk)

    # Checks if any blog posts were returned
    # If not, redirect the user to not_found
    if not blog_posts.exists():
        return redirect("/not-found")


    # Get the first blog post
    post = blog_posts.first()

    if post.author != request.user:
        return HttpResponse(
            "Permission Denied. You're no the owner of the blog post.", status=403
            ) 
    # HTTP 1xx --> info
    # 2xx -> Request ok
    # 3x -> Redirection 
    # 4xx -> Client/User error
    # 5xx -> Server error

    # Instantiate a form
    form = BlogForm(instance=post)

    # We check if user submit a form
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        # check if the form is valid i.e. user entered valid data
        if form.is_valid():
            _post = form.save(commit=False)
            _post.author = request.user
            _post.published_at = post.published_at
            _post.save()
            # what next?
            # redirect! 
            return redirect("read-blog", pk=post.pk)
    # Display a template to the end-user
    return render(request, 'daily_news/edit_blog.html', {'blog_post': post})

@login_required
def delete_blog(request, pk):
    if request.method == "POST":
        blog = Blog.objects.filter(id=pk).first()

        if blog and blog.author != request.user:
            return HttpResponse(
                        "Permission Denied. You're no the owner of the blog post.", status=403
                        ) 

        if blog:
            blog.delete()
        
        return redirect("home")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "registration/register.html", {"form": form})




@login_required
def profile(request):
    user = request.user
    # use the reverse accessor to obtain all the posts that belong to the user
    # and assign it to a variable called 'user_posts'
    user_posts = user.blog_set.all()
    return render(request, "registration/profile.html", context={'blogs': user_posts})





# python-dotenv: To hides sensitive credentials in our code 
# gunicorn: production server

# pip install python-dotenv gunicorn