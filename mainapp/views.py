# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.utils.deprecation import MiddlewareMixin
from taggit.models import Tag
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt

'''
Middleware to requires user to be logged in in every page.
Redirects to login page in every request (existent pages).
'''
class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'login' in request.path:
            return None
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return None

'''
Login page view
'''
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

def home(request):
    user = User.objects.get(user=request.user)
    return render(request, 'home.html', {
        'user': user,
        'projects': Project.objects.all()
    })

def older_publication(request, project, publication):
    user = User.objects.get(user=request.user)
    project = get_object_or_404(Project, acronym=project)
    publication = get_object_or_404(Publication, id=publication)
    try:
        return render(request, 'publication.html', {
            'user': user,
            'publication': project.publication_set.filter(pub_date__lt=publication.pub_date)[0],
        })
    except:
        Http404('Errow')

def newer_publication(request, project, publication):
    user = User.objects.get(user=request.user)
    project = get_object_or_404(Project, acronym=project)
    publication = get_object_or_404(Publication, id=publication)
    try:
        return render(request, 'publication.html', {
            'user': user,
            'publication': project.publication_set.filter(pub_date__gt=publication.pub_date)[0],
        })
    except:
        Http404('Errow')

def newest_publication(request, project):
    user = User.objects.get(user=request.user)
    project = get_object_or_404(Project, acronym=project)
    try:
        return render(request, 'publication.html', {
            'user': user,
            'publication': project.publication_set.all()[0],
        })
    except:
        Http404('Errow')

def publication(request, acronym, pub):
    user = User.objects.get(user=request.user)
    project = get_object_or_404(Project, acronym=acronym);
    try:
        return render(request, 'publication.html', {
            'user': user,
            'publication': project.publication_set.all()[int(pub)],
        })
    except:
        return HttpResponseForbidden('sai fora')

# def publication(request, pub_id):
#     publication = get_object_or_404(Publication, id=pub_id)
#     publications = Publication.objects.filter(id=pub_id)
#     return render(request, 'project.html', {
#         'user': User.objects.get(user=request.user),
#         'project': project,
#         'publications': publications,
#         'all_tags': Tag.objects.all(),
#     })

'''
Following views for CRUD in debate posts.
Remove, update and delete objects requires logged in user to own it.
'''
def debate(request, debate_id):
    user = User.objects.get(user=request.user)
    if request.method == 'POST':
        comment = Comment(
            user = user,
            debate = Debate.objects.get(pk=debate_id),
            text = request.POST['text'],
        )
        comment.save()
        return render(request, 'publication/debate/comment.html', {
            'user': user,
            'comment': comment,
        })

def comment(request, comment_id):
    user = User.objects.get(user=request.user)
    if request.method == 'POST':
        reply = Reply(
            user = user,
            comment = Comment.objects.get(pk=comment_id),
            text = request.POST['text'],
        )
        reply.save()
        return render(request, 'publication/debate/reply.html', {
            'user': user,
            'reply': reply,
        })
    elif request.method == 'DELETE':
        comment = Comment.objects.get(pk=comment_id)
        if user != comment.user:
            return HttpResponseForbidden('User does not own this comment to delete it.')
        else:
            comment.delete()
            return HttpResponse('Successfully deleted comment.')
    elif request.method == 'PUT':
        text = request.POST['text']
        comment = Comment.objects.get(pk=comment_id)
        if user != comment.user:
            return HttpResponseForbidden('User does not own this comment to edit it.')
        elif(text != comment.text):
            comment.text = text
            comment.save()
            return render(request, 'publication/debate/comment.html', {
                'user': user,
                'comment': comment,
            })
        else:
            return HttpResponseForbidden('No changes in comment')

def comment_update(request, comment_id):
    user = User.objects.get(user=request.user)
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment.objects.get(pk=comment_id)
        if user != comment.user:
            return HttpResponseForbidden('User does not own this comment to edit it.')
        elif(text != comment.text):
            comment.text = text
            comment.save()
            return render(request, 'publication/debate/comment.html', {
                'user': user,
                'comment': comment,
            })

def reply(request, reply_id):
    user = User.objects.get(user=request.user)
    if request.method == 'DELETE':
        reply = Reply.objects.get(pk=reply_id)
        if user != reply.user:
            return HttpResponseForbidden('User does not own this reply to delete it.')
        reply.delete()
        return HttpResponse('Successfully deleted reply.')

def project(request, acronym):
    Question.objects.all().delete()
    print 'ok'
    project = get_object_or_404(Project, acronym=acronym)

    #define etapa:
    etapas = []
    for idx in range(1,6):
        if int(project.etapa) == idx:
            etapas.append("actual")
        if int(project.etapa) > idx:            
            etapas.append("past")        
        if int(project.etapa) < idx:          
            etapas.append("future")
    return render(request, 'project.html', {
        
        'user': User.objects.get(user=request.user),
        'project': project,
        'publications': project.publication_set.all(),
        'all_tags': Tag.objects.all(),
        'etapas': etapas,
        'etapas_txt': get_object_or_404(project.etapas_set , etapa=project.etapa)
        
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
        return HttpResponse('Vote registered.')
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

############################################################################################################


def vote(request, question_id):
  
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:participe'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:participe'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:participe'))

def vote_iframe(request, question_id):

  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:home'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:home'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:home'))

def vote_initial(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))

def vote_timeline(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))