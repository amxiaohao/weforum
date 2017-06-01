from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Article, ArticleComment, Tag
from .forms import ArticleForm

ARTICLES_NUM_PAGES = 10


def _articles(request, articles):
    paginator = Paginator(articles, ARTICLES_NUM_PAGES)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()

    return render(request, 'articles/articles.html', {
        'articles': articles,
        'popular_tags': popular_tags,
    })


def articles(request):
    article_list = Article.get_published()
    return _articles(request, article_list)


def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'articles/article.html', {'article': article})


@login_required
def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.create_user = request.user
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.status = form.cleaned_data.get('status')
            article.save()
            tags = form.cleaned_data.get('tags')
            article.create_tags(tags)
            return HttpResponseRedirect(reverse('articles:articles'))

    else:
        form = ArticleForm()

    return render(request, 'articles/write.html', {'form': form})


def tag(request, tag_name):
    tags = get_list_or_404(Tag, tag=tag_name)
    articles = []
    for tag in tags:
        if tag.article.status == Article.PUBLISHED:
            articles.append(tag.article)

    return _articles(request, articles)


@login_required
def draft(request):
    draft_list = Article.objects.filter(create_user=request.user, 
                                        status=Article.DRAFT)
    return render(request, 'articles/draft.html', {'draft_list': draft_list})


@login_required
def edit(request, pk):
    tags = ''
    article = get_object_or_404(Article, pk=pk)

    if article.create_user.id != request.user.id:
        return HttpResponseRedirect(reverse('articles:articles'))

    for tag in article.get_tags():
        tags = '{0} {1}'.format(tags, tag.tag)
    tags = tags.strip()

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('articles:articles'))
    else:
        form = ArticleForm(instance=article, initial={'tags': tags})
    return render(request, 'articles/edit.html', {'form': form})


@login_required
def comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        comment = comment.strip()
        if len(comment) > 0:
            article_comment = ArticleComment(user=request.user, 
                                             article=article, 
                                             comment=comment)
            article_comment.save()
        return HttpResponseRedirect(reverse('articles:article', args=(article.slug, )))
    else:
        return render(request, 'articles/article.html', {'article': article})
