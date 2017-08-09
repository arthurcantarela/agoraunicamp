from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^project/(?P<acronym>[A-Za-z]+)$', views.project, name='project'),
    # url(r'^project/(?P<acronym>[A-Za-z]+)/(?P<pub>\d+)$', views.publication, name='publication'),
    url(r'^project/(?P<project>[A-Za-z]+)/(?P<publication>\d+)/newer$', views.newer_publication, name='newer_publication'),
    url(r'^project/(?P<project>[A-Za-z]+)/(?P<publication>\d+)/older$', views.older_publication, name='older_publication'),
    url(r'^project/(?P<project>[A-Za-z]+)/newest$', views.newest_publication, name='newest_publication'),
    # url(r'^publication/(?P<pub_id>\d+)$', views.publication, name='publication'),
    url(r'^question/choice/(?P<question_id>[0-9]+)$', views.vote, name='vote'),
    url(r'^question/proposal/(?P<question_id>[0-9]+)$', views.proposal, name='proposal'),
    url(r'^debate/(?P<debate_id>[0-9]+)$', views.debate, name='debate'),
    url(r'^comment/(?P<comment_id>[0-9]+)$', views.comment, name='comment'),
    url(r'^comment_update/(?P<comment_id>[0-9]+)$', views.comment_update, name='comment_update'),
    url(r'^reply/(?P<reply_id>[0-9]+)$', views.reply, name='reply'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
