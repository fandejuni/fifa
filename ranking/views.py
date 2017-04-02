from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    context = {
        'simple_ranking': Joueur.objects.order_by('-simple_score').all(),
        'double_ranking': Joueur.objects.order_by('-double_score').all(),
        'simple_matchs': MatchSimple.objects.order_by('-date').all(),
        'double_matchs': MatchDouble.objects.order_by('-date').all(),
    }
    return render(request, 'index.html', context)

def detail_joueur(request, joueur_id):
    joueur = get_object_or_404(Joueur, pk=joueur_id)
    context = {
        'joueur': joueur,
    }
    return render(request, 'joueur.html', context)

def recalculate(request):
    for j in Joueur.objects.all():

        j.simple_score = 500
        j.simple_victoires = 0
        j.simple_nuls = 0
        j.simple_defaites = 0
        j.simple_buts_pour = 0
        j.simple_buts_contre = 0

        j.double_score = 500
        j.double_victoires = 0
        j.double_nuls = 0
        j.double_defaites = 0
        j.double_buts_pour = 0
        j.double_buts_contre = 0

        j.save()

    for m  in MatchSimple.objects.all():

        j1 = m.domicile
        j2 = m.exterieur

        j1.simple_buts_pour += m.buts_domicile
        j1.simple_buts_contre += m.buts_exterieur

        j2.simple_buts_pour += m.buts_exterieur
        j2.simple_buts_contre += m.buts_domicile

        W = 0.5 # 0.5 pour nul, 1 victoire j1, 0 victoire j2

        if m.buts_domicile > m.buts_exterieur:
            j1.simple_victoires +=1
            j2.simple_defaites += 1
            W = 1.

        elif m.buts_domicile < m.buts_exterieur:
            j2.simple_victoires += 1
            j1.simple_defaites += 1
            W = 0.

        elif m.buts_domicile == m.buts_exterieur:
            j2.simple_nuls += 1
            j1.simple_nuls += 1
            W = 0.5

        D = j1.simple_score - j2.simple_score
        p = 1. / (1. + 10**(-D/400.))
        points = 20 * (W - p)

        m.points = points
        m.save()

        j1.simple_score += points
        j2.simple_score -= points

        j1.save()
        j2.save()

    return index(request)
