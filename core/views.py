from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from articles.views import articles, ARTICLES_NUM_PAGES
from articles.models import Article
from authentication.models import Profile
from .forms import ProfileForm, ChangePasswordForm, ProfileImageForm


def home(request):
    return articles(request)


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_articles = page_user.article_set.filter(status=Article.PUBLISHED)
    paginator = Paginator(all_articles, ARTICLES_NUM_PAGES)
    articles = paginator.page(1)
    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'articles': articles,
        'page': 1
    })


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            user.profile.save()
            messages.add_message(request, 
                                 messages.SUCCESS, 
                                 'Your profile was successfully edited.')
            # return HttpResponseRedirect(reverse('profile', args=(user.username, )))

    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location
        })

    return render(request, 'core/settings.html', {'form': form})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, 
                                 messages.SUCCESS, 
                                 'Your password was successfully changed.')
            return HttpResponseRedirect(reverse('core:password'))

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form})


@login_required
def upload_picture(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.get('image')
            image.name = str(user.username) + '.jpg'
            user.profile.image = image
            user.profile.save()
            return HttpResponseRedirect(reverse('core:upload_picture'))

    else:
        form = ProfileImageForm()

    return render(request, 'core/picture.html', {'form': form})