# -*- coding: utf-8 -*-

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
    # phase =

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __unicode__(self):
        return self.title

class Publication(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    project = models.ForeignKey(Project, verbose_name='Projeto')
    title = models.CharField('Título', max_length=200, blank=True)
    pub_date = models.DateField('Data de publicação')

    class Meta:
        ordering = ('pub_date', )

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    label = models.CharField(max_length=40, unique=True)
    publications = models.ManyToManyField(Publication)

    def __unicode__(self):
        return self.label

class Article(Publication):
    source = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'

# Questions
class ChoiceQuestion(Publication):
    question_text = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

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
