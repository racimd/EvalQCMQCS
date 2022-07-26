import code
from email.policy import default
from random import choices
from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Etablissement(models.Model) :
    nom = models.CharField(max_length=50,null=False)
    def __str__(self) -> str:
        return self.nom
    def nbeffectif(self):
        return self.administrateur_set.all().count() + self.evaluateur_set.all().count() + self.candidat_set.all().count()
    
    def get_users(self):
        users = []
        for i in self.administrateur_set.all():
            users.append(i)
        for i in self.evaluateur_set.all():
            users.append(i)
        for i in self.candidat_set.all():
            users.append(i)

        return users
        

class Administrateur(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    etablissement = models.ForeignKey(Etablissement,on_delete = models.CASCADE, null= False)
    isValide = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True,default='undraw_profile.svg',blank=True)

    def __str__(self) -> str:
        return self.user.username

class Evaluateur(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    etablissement = models.ForeignKey(Etablissement,on_delete = models.CASCADE, null= False)
    isValide = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True,default='undraw_profile.svg',blank=True)

    def __str__(self) -> str:
        return self.user.username

class Groupe(models.Model):
    nom = models.CharField(max_length=50,null=False)  
    etablissement = models.ForeignKey(Etablissement,on_delete = models.CASCADE, null= True)

    def __str__(self) -> str:
        return self.nom
    def get_candidats(self):
        return self.candidat_set.all()
    

class Module(models.Model):
    nom = models.CharField(max_length=50,null=False)
    evaluateur = models.ForeignKey(Evaluateur,on_delete= models.CASCADE,null= True,blank=True)
    groupes = models.ManyToManyField(Groupe,blank=True)
    etablissement = models.ForeignKey(Etablissement,on_delete = models.CASCADE,null=True)


    def __str__(self) -> str:
        return self.nom

class Candidat(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    groupe = models.ForeignKey(Groupe,on_delete = models.CASCADE, null= True,blank=True)
    etablissement = models.ForeignKey(Etablissement,on_delete = models.CASCADE,null=True)
    isValide = models.BooleanField(default=False)
    profile_pic = models.ImageField(null=True,default='undraw_profile.svg',blank=True)


    def __str__(self) -> str:
        return self.user.username
    
    

class Question(models.Model):
    contenu = models.CharField(max_length=100)
    module = models.ForeignKey(Module,on_delete = models.CASCADE, null= False, blank=True)
    tag = models.CharField(max_length=100, null=True,blank=True)
    CHOICES = (
        ('QCM', 'QCM'),
        ('QCS', 'QCS'),     
    )    
    type = models.CharField(max_length=100, choices = CHOICES,default='QCM',blank=False)


    def __str__(self) -> str:
        return self.contenu
    
    def get_reponses(self):
        return self.reponse_set.all()

class Reponse(models.Model):
    contenurep = models.CharField(max_length=100)
    isTrue = models.BooleanField()
    valeur = models.IntegerField()
    question = models.ForeignKey(Question,on_delete = models.CASCADE, null= False)
    def __str__(self) -> str:
        return self.contenurep


class Questionnaire(models.Model):
    nom = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question)
    def __str__(self) -> str:
        return self.nom
    def get_tests(self):
        return self.test_set.all()
    def get_module(self):
        list_questions = self.questions.all()
        if(len(list_questions)!=0):
            return list_questions[0].module
        else:
            return 'ERROR'
    


class Test(models.Model):
    nom = models.CharField(max_length=100)
    DateDeb = models.DateTimeField()
    DateFin = models.DateTimeField()
    questionnaire = models.ForeignKey(Questionnaire,on_delete = models.CASCADE, null= False)
    def __str__(self) -> str:
        return self.nom

    def get_invitation(self,user):
        return self.invitation_set.get(candidat=user.candidat)
    def get_invitationcount(self):
        return self.invitation_set.all().count()
    

    
    

class Resultat(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    score = models.FloatField()
    copie = models.JSONField(null = True)

    def __str__(self):
        return str(self.test) + " " + str(self.candidat) + " " + str(self.score)

class Invitation(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE,null= True)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, null= True)
    code = models.CharField(max_length=100,blank= True,null=True)
    status = models.IntegerField(blank= True,null=True)

    def __str__(self):
        return str(self.test.nom) + " " + str(self.candidat)












