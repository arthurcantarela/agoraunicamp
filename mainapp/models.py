# -*- coding: utf-8 -*-
from django.conf import settings
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User as AuthUser
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

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
    title = models.CharField('Nome do Projeto', max_length=200, blank=True)
    acronym = models.CharField('Sigla', max_length=10, blank=True)
    etapa = models.CharField("Etapa", max_length=1, default='1')

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __unicode__(self):
        return self.title

class Etapas(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Projeto')
    etapa = models.CharField("Etapa", max_length=1, default='1')
    name = models.CharField("Nome da etapa", max_length=100, default='Ideias')
    header_txt = models.TextField("Cabeçalho", default='null')
    objetivo_txt = models.TextField("Objetivo", default='null')
    participar_txt = models.TextField("Como participar", default='null')
    resultado_txt = models.TextField("Resultado", default='null')

# class Publication(models.Model):
#             author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
#     project = models.ForeignKey(Project, verbose_name='Projeto')
#     title = models.CharField('Título', max_length=200, blank=True)
#     pub_date = models.DateTimeField(
#         auto_now_add=True,
#         blank =True,
#         verbose_name = 'Data de publicação',
#     )
#     tags = TaggableManager()

#     class Meta:
#         ordering = ('-pub_date', )

#     def __unicode__(self):
#         return self.title

# class Article(Publication):
#     source = models.CharField(max_length=200, blank=True, default='')
#     content = RichTextUploadingField('ckeditor')

#     class Meta:
#         verbose_name = 'Artigo'
#         verbose_name_plural = 'Artigos'
#class Question(Publication):
#    class Meta:
#        verbose_name = 'Questão'
#        verbose_name_plural = 'Questões'


####################
class Question(models.Model):
    STATUS_CHOICES = (
        ('n', 'Não publicado'), # unpublished
        ('p', 'Publicado'),     # published
    )

    EXP_TIME = (
        (1, '1 dia'),           # a day
        (7, '1 semana'),        # a week
        (30, '1 mês'),          # a month
        (365, '1 ano'),         # a year
        (3650, 'Indeterminado') # undetermined
    )

    QUESTION_TYPE = (
        ('1', 'One choice'),
        ('2', 'Multipla Escolha'),
        ('3', 'Texto'),
    )

    projeto = models.ForeignKey('Project')
    question_type = models.CharField('Tipo', max_length=1, choices = QUESTION_TYPE)
    question_text = models.CharField('Título da Questão',max_length=200)
    publ_date = models.DateTimeField('Data de publicação')
    exp_date = models.DateTimeField('Data de expiração')
    days = models.IntegerField('Tempo para expirar', choices=EXP_TIME, default=3650)
    question_status = models.CharField('Estado da questão', max_length=1, choices=STATUS_CHOICES, default = 'n')
    answer_status = models.CharField('Estado da resposta', max_length=1, choices=STATUS_CHOICES, default = 'n')
    image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)
    tags = TaggableManager()
    address = models.CharField('Endereço',max_length=200)
    permissao = models.IntegerField(default=0)
    resultado = models.CharField(max_length=1, choices=STATUS_CHOICES , default = 'n')


    def __str__(self):
        if self.id:
            return "#{id} - {question}".format(id=self.id, question=self.question_text.encode('utf8'))
        else:
            return self.question_text.encode('utf8')

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.publ_date = timezone.now()
        self.update_expiration_time()
        super(Question, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/participe/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
        return super(Question, self).save(*args, **kwargs)

    def update_expiration_time(self):
        self.exp_date = self.publ_date + timedelta(days=self.days)

    def is_question_expired(self):
        return self.exp_date <= timezone.now()

    def is_question_published(self):
        if self.is_question_expired():
            self.question_status = 'n'
        if self.question_status == 'p':
            return True
        else:
            return False

    is_question_published.boolean = True
    is_question_published.short_description = 'Questão publicada?'

    def is_answer_published(self):
        if self.answer_status == 'p':
            return True
        else:
            return False

    is_answer_published.boolean = True
    is_answer_published.short_description = 'Resposta publicada?'

    class Meta:
        verbose_name = 'questão'
        verbose_name_plural = 'questões'

#projeto-foregnkey
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text.encode('utf8')

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'

#class ProposalQuestion(Question):
#    question_text = models.CharField(max_length=200)

#class Proposal(models.Model):
#    proposal_text = models.CharField(max_length=200)
#    question = models.ForeignKey(ProposalQuestion)
#    proponent = models.ForeignKey(User, blank=True)

    #class Meta:
    #    verbose_name = 'Proposta'
    #    verbose_name_plural = 'Propostas'

    #def __unicode__(self):
    #    return self.proposal_text

# class Dissertation(models.Model):
#     answer = models.CharField(max_length=2000)

# # class Debate(Publication):
# #     about = models.CharField(max_length=200)

# class Comment(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete = models.CASCADE,
#         related_name='comment',
#     )
#     debate = models.ForeignKey(
#         Debate,
#         on_delete = models.CASCADE,
#         related_name = 'comment',
#     )
#     text = models.CharField(max_length=200)
#     added = models.DateTimeField(auto_now_add=True, blank =True)
#     updated = models.DateTimeField(auto_now=True, blank=True)

#     def __unicode__(self):
#         return self.text

#     def save(self, *args, **kwargs):
#         super(Comment, self).save(*args, **kwargs)
#         if(self.history.count() == 0 or self.history.last().text != self.text):
#             comment_history = CommentHistory(
#                 comment = self,
#                 text = self.text,
#                 updated = self.updated,
#             )
#             comment_history.save()

# class CommentHistory(models.Model):
#     comment = models.ForeignKey(
#         Comment,
#         on_delete = models.CASCADE,
#         related_name = 'history',
#     )
#     text = models.CharField(max_length=200)
#     updated = models.DateTimeField()

# class Reply(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete = models.CASCADE,
#         related_name='reply',
#     )
#     comment = models.ForeignKey(
#         Comment,
#         on_delete = models.CASCADE,
#         related_name = 'reply',
#     )
#     text = models.CharField(max_length=200)
#     added = models.DateTimeField(auto_now_add=True, blank =True)
#     updated = models.DateTimeField(auto_now=True, blank=True)

#     def __unicode__(self):
#         return self.text

#     def save(self, *args, **kwargs):
#         super(Reply, self).save(*args, **kwargs)
#         if(self.history.count() == 0 or self.history.last().text != self.text):
#             reply_history = ReplyHistory(
#                 reply = self,
#                 text = self.text,
#                 updated = self.updated,
#             )
#             reply_history.save()

# class ReplyHistory(models.Model):
#     reply = models.ForeignKey(
#         Reply,
#         on_delete = models.CASCADE,
#         related_name = 'history',
#     )
#     text = models.CharField(max_length=200)
#     updated = models.DateTimeField()

#lass Result(Publication):
#    about = models.CharField(max_length=200)
#    choice_question = models.ForeignKey(
#        ChoiceQuestion,
#        on_delete = models.CASCADE,
#        related_name = 'result',
#    )
