from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from articles.models import Article


@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return HttpResponseRedirect(reverse('search'))

        try:
            search_type = request.GET.get('type')
            if search_type not in ['articles', 'users']:
                search_type = 'articles'
        except Exception:
            search_type = 'articles'

        count = {}
        results = {}
        results['articles'] = Article.objects.filter(
            Q(title__icontains=querystring) | Q(content__icontains=querystring)
        )
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | 
            Q(first_name__icontains=querystring) | 
            Q(last_name__icontains=querystring)
        )
        count['articles'] = results['articles'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })

    else:
        return render(request, 'search/search.html')