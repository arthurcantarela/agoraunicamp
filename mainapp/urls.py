from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.signin, name='sigin'),
    url(r'^(?P<question_id>\d+)$', views.vote, name='question')
]
