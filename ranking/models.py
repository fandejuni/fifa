from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Joueur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pseudo = models.CharField(max_length = 50, default="Pax lambda")

    # Simple
    simple_score = models.IntegerField(default=500)
    simple_rang = models.IntegerField(default=0)

    simple_victoires = models.IntegerField(default=0)
    simple_nuls = models.IntegerField(default=0)
    simple_defaites = models.IntegerField(default=0)

    simple_buts_pour = models.IntegerField(default=0)
    simple_buts_contre = models.IntegerField(default=0)

    # Double
    double_score = models.IntegerField(default=500)
    double_rang = models.IntegerField(default=0)

    double_victoires = models.IntegerField(default=0)
    double_nuls = models.IntegerField(default=0)
    double_defaites = models.IntegerField(default=0)

    double_buts_pour = models.IntegerField(default=0)
    double_buts_contre = models.IntegerField(default=0)

    @property
    def simple_matchs(self):
        return self.simple_nuls + self.simple_victoires + self.simple_defaites

    @property
    def double_matchs(self):
        return self.double_nuls + self.double_victoires + self.double_defaites

    @property
    def simple_diff(self):
        return self.simple_buts_pour - self.simple_buts_contre

    @property
    def double_diff(self):
        return self.double_buts_pour - self.double_buts_contre

    def __str__(self):
        return self.pseudo + " (" + str(self.simple_score) + ", " + str(self.double_score) + ")"

@receiver(post_save, sender=User)
def create_joueur(sender, instance, created, **kwargs):
    if created:
        Joueur.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_joueur(sender, instance, **kwargs):
    instance.joueur.save()

class MatchSimple(models.Model):
    domicile = models.ForeignKey('Joueur', related_name = 'dom')
    exterieur = models.ForeignKey('Joueur', related_name = 'exte')
    date = models.DateTimeField(auto_now=True)
    buts_domicile = models.IntegerField(default=0)
    buts_exterieur = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    @property
    def winner(self):
        if self.buts_domicile > self.buts_exterieur:
            return 1.
        elif self.buts_domicile < self.buts_exterieur:
            return 0.
        else:
            return 0.5

    def __str__(self):
        return self.domicile.pseudo + " " + str(self.buts_domicile) + " - " + str(self.buts_exterieur) + " " + self.exterieur.pseudo

class MatchDouble(models.Model):
    domicile_1 = models.ForeignKey('Joueur', related_name = 'dom1')
    domicile_2 = models.ForeignKey('Joueur', related_name = 'dom2')
    exterieur_1 = models.ForeignKey('Joueur', related_name = 'exte1')
    exterieur_2 = models.ForeignKey('Joueur', related_name = 'exte2')
    date = models.DateTimeField(auto_now=True)
    buts_domicile = models.IntegerField(default=0)
    buts_exterieur = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    @property
    def winner(self):
        if self.buts_domicile > self.buts_exterieur:
            return 1.
        elif self.buts_domicile < self.buts_exterieur:
            return 0.
        else:
            return 0.5

    def __str__(self):
        s = self.domicile_1.pseudo + ", "
        s += self.domicile_2.pseudo + " - "
        s += self.exterieur_1.pseudo + ", "
        s += self.exterieur_2.pseudo
        return s


