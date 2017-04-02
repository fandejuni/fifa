from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    context = {
        'simple_ranking': Joueur.objects.order_by('-simple_score').all(),
        'double_ranking': Joueur.objects.order_by('-double_score').all(),
    }
    return render(request, 'index.html', context)

def detail_joueur(request, joueur_id):
    joueur = get_object_or_404(Joueur, pk=joueur_id)
    context = {
        'joueur': joueur,
    }
    return render(request, 'joueur.html', context)
