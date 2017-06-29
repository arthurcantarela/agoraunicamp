# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as AuthUser

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

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __unicode__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    project = models.ForeignKey(Project, verbose_name='Projeto')
    title = models.CharField('Título', max_length=200, blank=True)
    pub_date = models.DateField('Data de publicação')

    class Meta:
        ordering = ('pub_date', )

    def __unicode__(self):
        return self.title

class Article(Post):
    source = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'

class Question(Post):
    question_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __unicode__(self):
        return self.answer
