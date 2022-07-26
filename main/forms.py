import array
from secrets import choice
from tokenize import group
from django import forms
from django.forms import ModelForm,  inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Administrateur, Candidat,Etablissement, Evaluateur, Groupe, Module, Question, Questionnaire,Reponse, Test
from main import models
from django.contrib.admin import widgets






class AdministrateurForm(ModelForm):
    class Meta:
        model = Administrateur
        fields = ('etablissement','isValide')
        widgets = { 
            'etablissement': forms.Select(attrs={'class': 'form-control col-sm-2'}),
             'isValide': forms.CheckboxInput
    
        }

class EtablissementForm(ModelForm):
    class Meta:
        model = Etablissement
        fields = ('nom',)
        widgets = { 
            'nom' : forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
        }



class CreateUserForm(UserCreationForm):
    

    choix_staff=(
        ('admin', 'admin'),
        ('evaluateur', 'evaluateur'),
        ('candidat','candidat')
    )

    myquery = queryset=Etablissement.objects.values_list('id',flat=True)
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Repeat Password'}))
    groups = forms.MultipleChoiceField( 
    widget=forms.SelectMultiple(attrs={'class':'form-control','id':'type','name':'type'}), required=True, choices = choix_staff)

    etablissement = forms.ModelChoiceField(queryset=Etablissement.objects.all(),to_field_name='nom',required=False,
        widget=forms.Select(attrs={'class':'form-control','id' : 'etab', 'name' : 'etab'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2','groups','etablissement','first_name','last_name']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control form-control-user','placeholder': 'Username'}),
            'email' : forms.TextInput(attrs={'class':'form-control form-control-user','placeholder': 'Email Address'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control form-control-user','placeholder': 'Nom'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control form-control-user','placeholder': 'Prenom'}),

        }
        
   



class EvaluateurForm(ModelForm):
    class Meta:
        model = Evaluateur
        fields = ('isValide',)
        widgets = { 
         
            'isValide': forms.CheckboxInput
            
        }

class CandidatForm(ModelForm):
    class Meta:
        model = Candidat
        fields = ('groupe','isValide')
        widgets = { 
          
            'groupe': forms.Select(attrs={'class': 'form-control col-sm-2'}),
            'isValide': forms.CheckboxInput


            
        }

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ('nom','evaluateur','groupes')
        widgets = { 
            'nom': forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'evaluateur': forms.Select(attrs={'class': 'form-control col-sm-2'}),
            'groupes': forms.SelectMultiple(attrs={'class': 'form-control col-sm-2'}),
        }
    def __init__(self, *args,user=None,**kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        if user is not None:
            print(user)
            etab = Etablissement.objects.filter(id = user.administrateur.etablissement.id)
            
                    
            self.fields['groupes'].queryset = models.Groupe.objects.filter(etablissement__in = etab)
            self.fields['evaluateur'].queryset = models.Evaluateur.objects.filter(etablissement__in = etab)



class GroupeForm(ModelForm):
    class Meta:
        model = Groupe
        fields = ('nom',)
        widgets = { 
            'nom': forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'etablissement': forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),

        }
    def __init__(self, *args,user=None,pk=None,**kwargs):
        super(GroupeForm, self).__init__(*args, **kwargs)
        if user is not None:
            print("h")
            
      
        

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('contenu','module')
        widgets = { 
            'contenu': forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'module': forms.Select(attrs={'class': 'form-control col-sm-2'}),
        }
    def __init__(self, *args,user=None,**kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['module'].queryset = Module.objects.filter(evaluateur=user.evaluateur)
    
class QuestionForm2(ModelForm):
    class Meta:
        model = Question
        fields = ('contenu',)
        widget = { 
            'contenu': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),
        }
    def __init__(self, *args,user=None,pk=None,**kwargs):
        super(QuestionForm2, self).__init__(*args, **kwargs)
        if user is not None:
            print("a")
            
            
            

class QuestionnaireForm(ModelForm):

    class Meta:
        model = Questionnaire
        fields = ('nom','questions',)
        widgets = { 
            'nom': forms.TextInput(attrs={'class': 'form-control col-sm-2 col-form-label'}),
            'questions': forms.SelectMultiple(attrs={'class': 'form-control col-sm-2 col-form-label'}), 
 
        }
    def __init__(self, *args,user=None,pk=None,**kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['questions'].queryset = Question.objects.filter(module=pk)
    


class ReponseForm(ModelForm):
    class Meta:
        model = Reponse
        fields = ('contenurep','isTrue','valeur','question')
        widgets = { 
            'contenurep': forms.TextInput(attrs={'class': 'form-control' 'form-control-user col-sm-2'}),
            'isTrue': forms.CheckboxInput(attrs={'class': 'form-control' 'form-control-user col-sm-2'}),
            'valeur': forms.NumberInput(attrs={'class': 'form-control' 'form-control-user col-sm-2'}),
            'question': forms.Select(attrs={'class': 'form-control' 'form-control-user col-sm-2'}),

     }

ReponseFormSet = inlineformset_factory(Question, Reponse, fields=('contenurep','isTrue','valeur','question',))



class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ('nom','DateDeb','DateFin','questionnaire')
        widgets = { 
            'nom': forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'DateDeb': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'class':'form-control col-sm-2','type': 'datetime-local'}),
            'DateFin': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'class':'form-control col-sm-2','type': 'datetime-local'}),
            'questionnaire': forms.Select(attrs={'class': 'form-control col-sm-2'}),
     }
    def __init__(self, *args,user=None,pk=None,**kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        if user is not None:
            question_list = Question.objects.filter(module=pk)
            questionnaire_list = Questionnaire.objects.filter(questions__in=question_list)
            self.fields['questionnaire'].queryset = Questionnaire.objects.filter(id__in=questionnaire_list)


class AccepterInvitForm(ModelForm):
    class Meta:
        fields = {'code'}

    
         


