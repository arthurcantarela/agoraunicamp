# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from taggit.models import Tag
from .models import *
from .forms import *

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'login' in request.path:
            return None
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return None

def user_login(request):
    error_message = None
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            error_message = 'Usuário ou senha incorretos.'
        else:
            error_message = 'Os dados preenchidos não são válidos'
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message,
    })

def project(request, acronym):
    project = get_object_or_404(Project, acronym=acronym)
    return render(request, 'project.html', {
        'user': User.objects.get(user=request.user),
        'project': project,
        'publications': project.publication_set.all(),
        'all_tags': Tag.objects.all(),
    })

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
    user = User.objects.get(user=request.user)
    return render(request, 'home.html', {
        'user': request.user,
        'projects': Project.objects.all()
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
        HttpResponse('Vote registered.')
    return render(request, 'question.html', {
        'question': question,
        'choices': question.choice_set.all(),
        'vote': question.vote_set.get(user=user)
    })

def proposal(request, question_id):
    user = User.objects.get(user=request.user)
    question = ProposalQuestion.objects.get(pk=question_id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if 'proposal' in key and value:
                Proposal.objects.create(
                    proposal_text = value,
                    question = question,
                    proponent = user,
                )
        return HttpResponse('Deu certo')
    return None

def test(request, question_id):
    question = ChoiceQuestion.objects.get(pk=question_id)
    form = ChoiceQuestionForm(choices = question.choice_set.all())
    return render(request, 'question.html', {
        'form': form
    })
