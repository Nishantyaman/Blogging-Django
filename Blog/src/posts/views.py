from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .forms import PostForm
from .models import Post


# Create your views here.

def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'post_form.html', context)


def posts_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": "detail",
        "instance": instance,
        "share_string": share_string
    }
    return render(request, 'post_detail.html', context)


def posts_list(request):
    today = timezone.now().date()
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())#all()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)|
                                             Q(content__icontains=query) |
                                             Q(user__first_name__icontains=query)|
                                             Q(user__last_name__icontains=query)
                                             ).distinct()
    paginator = Paginator(queryset_list, 2)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)
    context = {
        "object_list": queryset,
        "title": "list",
        "page_request_var": page_request_var,
        "today": today
    }
    return render(request, 'post_list.html', context)
    # return HttpResponse("<h1>List</h1>")


def posts_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a>Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": "detail",
        "instance": instance,
        "form": form
    }
    return render(request, 'post_form.html', context)


def posts_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
	
def test():
	pass
	
def test2():
	pass
