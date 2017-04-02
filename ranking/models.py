from django.db import models
from django.contrib.auth.models import User

class Joueur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pseudo = models.CharField(max_length = 50, default="Pax lambda")

    simple_score = models.IntegerField(default=1000)
    simple_matchs = models.IntegerField(default=0)
    simple_victoires = models.IntegerField(default=0)
    simple_defaites = models.IntegerField(default=0)
    simple_buts_pour = models.IntegerField(default=0)
    simple_buts_contre = models.IntegerField(default=0)

    double_score = models.IntegerField(default=1000)
    double_matchs = models.IntegerField(default=0)
    double_victoires = models.IntegerField(default=0)
    double_defaites = models.IntegerField(default=0)
    double_buts_pour = models.IntegerField(default=0)
    double_buts_contre = models.IntegerField(default=0)

    @property
    def simple_nuls(self):
        return self.simple_matchs - self.simple_victoires - self.simple_defaites

    @property
    def double_nuls(self):
        return self.double_matchs - self.double_victoires - self.double_defaites

    @property
    def simple_diff(self):
        return self.simple_buts_pour - self.simple_buts_contre

    @property
    def double_diff(self):
        return self.double_buts_pour - self.double_buts_contre

    def __str__(self):
        return self.pseudo + " (" + str(self.score_simple) + ", " + str(self.score_double) + ")"

class MatchSimple(models.Model):
    domicile = models.ForeignKey('Joueur', related_name = 'dom')
    exterieur = models.ForeignKey('Joueur', related_name = 'exte')
    date = models.DateTimeField(auto_now=True)
    buts_domicile = models.IntegerField(default=0)
    buts_exterieurs = models.IntegerField(default=0)
    points_domicile = models.IntegerField(default=0)
    points_exterieur = models.IntegerField(default=0)

    def __str__(self):
        return self.domicile.pseudo + " " + str(self.buts_domicile) + " - " + str(self.buts_exterieurs) + " " + self.exterieur.pseudo

class MatchDouble(models.Model):
    domicile_1 = models.ForeignKey('Joueur', related_name = 'dom1')
    domicile_2 = models.ForeignKey('Joueur', related_name = 'dom2')
    exterieur_1 = models.ForeignKey('Joueur', related_name = 'exte1')
    exterieur_2 = models.ForeignKey('Joueur', related_name = 'exte2')
    date = models.DateTimeField(auto_now=True)
    buts_domicile = models.IntegerField(default=0)
    buts_exterieurs = models.IntegerField(default=0)
    points_domicile = models.IntegerField(default=0)
    points_exterieur = models.IntegerField(default=0)

    def __str__(self):
        return buts_domicile


