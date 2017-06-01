from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Profile
from .forms import SignUpForm
from core.views import home


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html', {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password, 
                                            email=email)
            profile = Profile(user=user)
            profile.save()
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect(reverse('home'))

    else:
        return render(request, 'authentication/signup.html', {'form': SignUpForm()})