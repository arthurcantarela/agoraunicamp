# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import *
from .forms import *

def signin(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return home(request)
            error_message = 'Usuário ou senha incorretos.'
        else:
            error_message = 'Os dados preenchidos não são válidos'
    else:
        # if request.user is not None:
        #     return home(request)
        form = LoginForm()

    return render(request, 'signin.html', {'form': form, 'error_message': error_message})

def home(request):
    return render(request, 'home.html', {
        'user': request.user
    })

def vote(request, question_id):
    user = User.objects.get(user=request.user)
    question = ChoiceQuestion.objects.get(pk=question_id)
    if request.method == 'POST':
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        Vote.objects.update_or_create(
            user = user,
            question = question,
            defaults={'selected_choice': selected_choice}
        )
    return render(request, 'question.html', {
        'question': question,
        'choices': question.choice_set.all(),
        'vote': question.vote_set.get(user=user)
    })
