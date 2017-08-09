# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User as AuthUser
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class User(models.Model):
    user = models.OneToOneField(
        AuthUser,
        primary_key=True,
        parent_link=True,
        on_delete=models.CASCADE
    )

    STAFF_TYPE = (
        ('1', 'Professor'),
        ('2', 'Funcionario'),
        ('3', 'Aluno-Graduacao'),
        ('4', 'Aluno-Mestrado'),
        ('5', 'Aluno-Doutorado'),
        ('6', 'Aluno-Especial'),
        ('7', 'Aluno-Lato'),
        ('8', 'Outro'),
    )

    avatar = models.ImageField(
        upload_to = 'media/img/',
        default = 'media/img/no-avatar.jpg',
    )
    first_name =  models.CharField('Nome', max_length=40, blank=True)
    last_name =  models.CharField('Sobrenome', max_length=100, blank=True)
    staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)
    institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto')
    academic_registry = models.IntegerField('Registro acadêmico',default='9999')
    email = models.EmailField('Email', blank=True)
    nickname = models.CharField('Apelido', max_length=40, blank=True, null=True)

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return '{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        nome = self.user.user
        return super(User, self).save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(max_length=200, blank=True)
    acronym = models.CharField('Sigla', max_length=10, blank=True)

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __unicode__(self):
        return self.title

class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    project = models.ForeignKey(Project, verbose_name='Projeto')
    title = models.CharField('Título', max_length=200, blank=True)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank =True,
        verbose_name = 'Data de publicação',
    )
    tags = TaggableManager()

    class Meta:
        ordering = ('-pub_date', )

    def __unicode__(self):
        return self.title

class Article(Publication):
    source = models.CharField(max_length=200, blank=True, default='')
    content = RichTextUploadingField('ckeditor')

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'

class Question(Publication):
    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

class ChoiceQuestion(Question):
    question_text = models.CharField(max_length=200)

    # def save(self, *args, **kwargs):
    #     super(Choice, self).save(*args, **kwargs)


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(ChoiceQuestion)

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __unicode__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(ChoiceQuestion)
    selected_choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        unique_together = (
            ('question', 'user')
        )

    def __unicode__(self):
        return self.selected_choice.choice_text

class ProposalQuestion(Question):
    question_text = models.CharField(max_length=200)

class Proposal(models.Model):
    proposal_text = models.CharField(max_length=200)
    question = models.ForeignKey(ProposalQuestion)
    proponent = models.ForeignKey(User, blank=True)

    class Meta:
        verbose_name = 'Proposta'
        verbose_name_plural = 'Propostas'

    def __unicode__(self):
        return self.proposal_text

class Dissertation(models.Model):
    answer = models.CharField(max_length=2000)

class Debate(Publication):
    about = models.CharField(max_length=200)

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name='comment',
    )
    debate = models.ForeignKey(
        Debate,
        on_delete = models.CASCADE,
        related_name = 'comment',
    )
    text = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True, blank =True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        if(self.history.count() == 0 or self.history.last().text != self.text):
            comment_history = CommentHistory(
                comment = self,
                text = self.text,
                updated = self.updated,
            )
            comment_history.save()

class CommentHistory(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        related_name = 'history',
    )
    text = models.CharField(max_length=200)
    updated = models.DateTimeField()

class Reply(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name='reply',
    )
    comment = models.ForeignKey(
        Comment,
        on_delete = models.CASCADE,
        related_name = 'reply',
    )
    text = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True, blank =True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        super(Reply, self).save(*args, **kwargs)
        if(self.history.count() == 0 or self.history.last().text != self.text):
            reply_history = ReplyHistory(
                reply = self,
                text = self.text,
                updated = self.updated,
            )
            reply_history.save()

class ReplyHistory(models.Model):
    reply = models.ForeignKey(
        Reply,
        on_delete = models.CASCADE,
        related_name = 'history',
    )
    text = models.CharField(max_length=200)
    updated = models.DateTimeField()

# class Result(Publication):
#     about = models.CharField(max_length=200)
#     question = models.ForeignKey(
#         ChoiceQuestion,
#         on_delete = models.CASCADE,
#         related_name = 'result',
#     )
