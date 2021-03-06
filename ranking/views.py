from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import random

def decima(x):
    return '{0:.2f}'.format(x)

def reglement(request):
    return render(request, 'reglement.html')

def annuler_match(request, match_id):
    m = get_object_or_404(MatchSimple, pk=match_id)
    joueur = request.user.joueur
    if joueur == m.domicile:
        m.delete()
        calculate()
        return redirect('joueur', joueur.id)
    else:
        return redirect('index')

def annuler_match_double(request, match_id):
    m = get_object_or_404(MatchDouble, pk=match_id)
    joueur = request.user.joueur
    print(joueur)
    print(m.domicile_1)
    if joueur.id == m.domicile_1.id:
        m.delete()
        calculate()
        return redirect('joueur', joueur.id)
    else:
        return redirect('index')

def index(request):
    n_matchs = 10
    context = {
        'simple_ranking': Joueur.objects.order_by('simple_rang').all(),
        'double_ranking': Joueur.objects.order_by('double_rang').all(),
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

    doubles_1 = MatchDouble.objects.filter(domicile_1__id = joueur_id)
    doubles_2 = MatchDouble.objects.filter(domicile_2__id = joueur_id)
    doubles_3 = MatchDouble.objects.filter(exterieur_1__id = joueur_id)
    doubles_4 = MatchDouble.objects.filter(exterieur_2__id = joueur_id)
    doubles = doubles_1 | doubles_2 | doubles_3 | doubles_4

    context = {
        'joueur': get_object_or_404(Joueur, pk=joueur_id),
        'simple_matchs': simples.order_by('-date').all(),
        'double_matchs': doubles.order_by('-date').all(),
    }
    return render(request, 'joueur.html', context)

def traiter_match(request):
    if request.user.is_authenticated:
        j1 = request.user.joueur
        j2 = get_object_or_404(Joueur, pk=request.POST['adv'])
        s1 = int(request.POST['score_1'])
        s2 = int(request.POST['score_2'])
        if j1 != j2 and 0 <= s1 <= 30 and 0 <= s2 <= 30:
            m = MatchSimple(domicile=j1, exterieur=j2, buts_domicile=s1, buts_exterieur=s2)
            m.save()
            update_simple(m)
	    update_ranking()
    return redirect('index')

def team(request):
    P = request.POST
    context = {
        'players': Joueur.objects.order_by('double_rang').all(),
    }
    if 'adv1' in P and 'adv2' in P and 'adv3' in P and 'adv4' in P:
        s = set([P['adv1'], P['adv2'], P['adv3'], P['adv4']])
        if len(s) == 4:
            dom = set(random.sample(s, 2))
            exte = s - dom

            d1 = get_object_or_404(Joueur, pk=dom.pop())
            d2 = get_object_or_404(Joueur, pk=dom.pop())
            e1 = get_object_or_404(Joueur, pk=exte.pop())
            e2 = get_object_or_404(Joueur, pk=exte.pop())

            D = (d1.double_score + d2.double_score) - (e1.double_score + e2.double_score)
            p = 1. / (1. + 10**(-D/400.))

            context = {
                'players': Joueur.objects.order_by('double_rang').all(),
                'd1' : d1,
                'd2' : d2,
                'e1' : e1,
                'e2' : e2,
                'c1' : int(round(p * 100, 0)),
                'c2' : int(round((1 - p) * 100, 0)),
            }
    return render(request, 'team.html', context)

def traiter_match_double(request):
    if request.user.is_authenticated:
        j1 = request.user.joueur
        j2 = get_object_or_404(Joueur, pk=request.POST['co'])
        j3 = get_object_or_404(Joueur, pk=request.POST['adv_1'])
        j4 = get_object_or_404(Joueur, pk=request.POST['adv_2'])
        s1 = int(request.POST['score_1'])
        s2 = int(request.POST['score_2'])
        b = True
        b = b and j1 != j2
        b = b and j1 != j3
        b = b and j1 != j4
        b = b and j2 != j3
        b = b and j2 != j4
        b = b and j3 != j4
        b = b and 0 <= s1 <= 30
        b = b and 0 <= s2 <= 30
        if b:
            m = MatchDouble(domicile_1=j1, domicile_2=j2, exterieur_1 = j3, exterieur_2 = j4, buts_domicile=s1, buts_exterieur=s2)
            m.save()
            update_double(m)
	    update_ranking()
    return redirect('index')


def recalculate(request):
    calculate()
    return redirect('index')

def update_simple(m):

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
    p = 1. / (1. + 10**(-D/200.))
    points = 20 * (W - p)
    
    m.points = points
    m.save()
    
    j1.simple_score += points
    j2.simple_score -= points
    
    j1.save()
    j2.save()

def update_double(m):

    j1 = m.domicile_1
    j2 = m.domicile_2
    j3 = m.exterieur_1
    j4 = m.exterieur_2
    
    j1.double_buts_pour += m.buts_domicile
    j2.double_buts_pour += m.buts_domicile
    j1.double_buts_contre += m.buts_exterieur
    j2.double_buts_contre += m.buts_exterieur
    
    j3.double_buts_pour += m.buts_exterieur
    j4.double_buts_pour += m.buts_exterieur
    j3.double_buts_contre += m.buts_domicile
    j4.double_buts_contre += m.buts_domicile
    
    W = m.winner
    
    if W == 1:
        j1.double_victoires +=1
        j2.double_victoires +=1
        j3.double_defaites += 1
        j4.double_defaites += 1
    
    elif W == 0:
        j3.double_victoires += 1
        j4.double_victoires += 1
        j1.double_defaites += 1
        j2.double_defaites += 1
    
    else:
        j1.double_nuls += 1
        j2.double_nuls += 1
        j3.double_nuls += 1
        j4.double_nuls += 1
    
    D = (j1.double_score + j2.double_score) - (j3.double_score + j4.double_score)
    p = 1. / (1. + 10**(-D/400.)) # 800 car on "divise" D par 2
    points = 20 * (W - p)
    
    m.points = points
    m.save()
    
    j1.double_score += points
    j2.double_score += points
    j3.double_score -= points
    j4.double_score -= points
    
    j1.save()
    j2.save()
    j3.save()
    j4.save()

def calculate():

    for j in Joueur.objects.all():

        j.simple_score = 100
        j.simple_victoires = 0
        j.simple_nuls = 0
        j.simple_defaites = 0
        j.simple_buts_pour = 0
        j.simple_buts_contre = 0

        j.double_score = 100
        j.double_victoires = 0
        j.double_nuls = 0
        j.double_defaites = 0
        j.double_buts_pour = 0
        j.double_buts_contre = 0

        j.save()

    for m in MatchSimple.objects.order_by('date').all():
	update_simple(m)

    for m in MatchDouble.objects.order_by('date').all():
	update_double(m)
	
    update_ranking()

def update_ranking():

    i = 1
    for j in Joueur.objects.order_by('-simple_score').all():
        j.simple_rang = i
        j.save()
        i += 1

    i = 1
    for j in Joueur.objects.order_by('-double_score').all():
        j.double_rang = i
        j.save()
        i += 1
