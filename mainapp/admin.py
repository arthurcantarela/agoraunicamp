# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import *

admin.site.disable_action('delete_selected')
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'users'

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'acronym', 'etapa']

class EtapasAdmin(admin.ModelAdmin):
    list_display = ['project', 'etapa','name', 'header_txt', 'objetivo_txt','participar_txt','resultado_txt']

class AuthUserAdmin(BaseUserAdmin):
    inlines = (UserInline, )

#class ProposalInline(admin.TabularInline):
#    model = Proposal
#    can_delete = True

#class ProposalQuestionAdmin(admin.ModelAdmin):
##    inlines = (ProposalInline, )

# class CommentInline(admin.TabularInline):
#     model = Comment
#     can_delete = True

# class DebateAdmin(admin.ModelAdmin):
#     inlines = (CommentInline, )

# class ReplyInline(admin.TabularInline):
#     model = Reply
#     can_delete = True

# class CommentAdmin(admin.ModelAdmin):
#     inlines = (ReplyInline, )


class QuestionAdmin(admin.ModelAdmin):
  fields = ['projeto','question_text', 'question_type', 'tags', 'days']
  inlines = [ChoiceInline]
  list_filter = ['publ_date', 'exp_date', 'question_type']
  search_fields = ['question_text']
  list_display = ['projeto', 'question_text', 'id', 'publ_date', 'exp_date', 'question_type', 'is_question_published', 'is_answer_published','address']
  actions = ['publish_question', 'unpublish_question','remover_questao']

  def publish_question(self, request, queryset):
    if queryset.count() != 1:
        message_bit = "Não é possível publicar mais de uma questão por vez."
        self.message_user(request, message_bit)
        return
    else:
        queryset.update(question_status='p')
        message_bit = "Questão publicada"
        queryset.update(publ_date = timezone.now())
        x = Message(kind='4', published='Sim', publ_date=timezone.now())
        for title in queryset:
            t = title.question_text.encode('utf8')
            a = title.address
            p = title.projeto
        x.message="Nova questão inserida: {id}".format(id=t)
        x.address = a
        x.projeto = p
        x.save()
        self.message_user(request, message_bit)
        return
  publish_question.short_description = "Publicar questão"

  def remover_questao(modeladmin, request, queryset):
      if queryset.count() != 1:
          modeladmin.message_user(request, "Não é possível remover mais de uma questão por vez.")
          return
      else:
          for title in queryset:
              e = title.address
          objs = Message.objects.filter(kind = '4')
          for obj in objs:
              if obj.address == e:
                  queryset.delete()
                  obj.delete()
                  modeladmin.message_user(request, "Questão removida com sucesso.")
                  return
      return


  def unpublish_question(modeladmin, request, queryset):
    rows_updated = queryset.update(question_status='n')
    if queryset.count() != 1:
        modeladmin.message_user(request, "Não é possível remover mais de uma questão por vez.")
        return
    else:
        for title in queryset:
            e = title.address
        objs = Message.objects.filter(kind = '4')
        for obj in objs:
            if obj.address == e:
                obj.delete()
                modeladmin.message_user(request, "Questão despublicada com sucesso.")
                return
    return


  unpublish_question.short_description = "Despublicar questão"


admin.site.unregister(AuthUser)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Etapas, EtapasAdmin)
#admin.site.register(ProposalQuestion, ProposalQuestionAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Debate, DebateAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(CommentHistory)
# admin.site.register(Article)
#admin.site.register(Result)
