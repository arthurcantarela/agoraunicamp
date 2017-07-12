from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^project/(?P<acronym>[A-Za-z]+)$', views.project, name='project'),
    url(r'^question/choice/(?P<question_id>[0-9]+)$', views.vote, name='vote'),
    url(r'^question/proposal/(?P<question_id>[0-9]+)$', views.proposal, name='proposal'),
    url(r'^test/(?P<question_id>[0-9]+)$', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
