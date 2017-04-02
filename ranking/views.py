from django.shortcuts import render, get_object_or_404, redirect
from .models import *

def annuler_match(request, match_id):
    m = get_object_or_404(MatchSimple, pk=match_id)
    joueur = request.user.joueur
    if joueur == m.domicile:
        m.delete()
        calculate()
        return redirect('joueur', joueur.id)
    else:
        return redirect('index')

def index(request):
    n_matchs = 10
    context = {
        'simple_ranking': Joueur.objects.order_by('-simple_score').all(),
        'double_ranking': Joueur.objects.order_by('-double_score').all(),
        'simple_matchs': MatchSimple.objects.order_by('-date').all()[:n_matchs],
        'double_matchs': MatchDouble.objects.order_by('-date').all()[:n_matchs],
    }
    return render(request, 'index.html', context)

def all_matchs(request):
    context = {
        'simple_matchs': MatchSimple.objects.order_by('-date').all(),
        'double_matchs': MatchDouble.objects.order_by('-date').all(),
    }
    return render(request, 'all_matchs.html', context)

def detail_joueur(request, joueur_id):
    simples_1 = MatchSimple.objects.filter(domicile__id = joueur_id)
    simples_2 = MatchSimple.objects.filter(exterieur__id = joueur_id)
    simples = simples_1 | simples_2
    context = {
        'joueur': get_object_or_404(Joueur, pk=joueur_id),
        'simple_matchs': simples.order_by('-date').all(),
    }
    return render(request, 'joueur.html', context)

def traiter_match(request):
    if request.user.is_authenticated:
        j1 = request.user.joueur
        j2 = get_object_or_404(Joueur, pk=request.POST['adv'])
        s1 = int(request.POST['score_1'])
        s2 = int(request.POST['score_2'])
        if j1.id != j2.id and 0 <= s1 <= 30 and 0 <= s2 <= 30:
            m = MatchSimple(domicile=j1, exterieur=j2, buts_domicile=s1, buts_exterieur=s2)
            m.save()
            calculate()
    return redirect('index')

def recalculate(request):
    calculate()
    return redirect('index')

def calculate():
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

    for m  in MatchSimple.objects.order_by('date').all():

        j1 = m.domicile
        j2 = m.exterieur

        j1.simple_buts_pour += m.buts_domicile
        j1.simple_buts_contre += m.buts_exterieur

        j2.simple_buts_pour += m.buts_exterieur
        j2.simple_buts_contre += m.buts_domicile

        W = m.winner

        if W == 1:
            j1.simple_victoires +=1
            j2.simple_defaites += 1

        elif W == 0:
            j2.simple_victoires += 1
            j1.simple_defaites += 1

        else:
            j2.simple_nuls += 1
            j1.simple_nuls += 1

        D = j1.simple_score - j2.simple_score
        p = 1. / (1. + 10**(-D/400.))
        points = 20 * (W - p)

        m.points = points
        m.save()

        j1.simple_score += points
        j2.simple_score -= points

        j1.save()
        j2.save()
