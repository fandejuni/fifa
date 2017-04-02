from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^joueur/(?P<joueur_id>[0-9]+)/$', views.detail_joueur, name='joueur'),
    url(r'^$', views.index, name='index'),
]

