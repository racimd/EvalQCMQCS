from dataclasses import field
from datetime import datetime, timedelta, timezone
from http.client import HTTPResponse
from multiprocessing import context
from pickle import NEWOBJ_EX
import random
import string
from webbrowser import get
from xml.etree.ElementTree import tostring
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import CheckboxInput, NumberInput, TextInput, Textarea, inlineformset_factory, modelformset_factory
from django.urls import reverse
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.mail import send_mail

from project import settings
from .filters import ModuleFilter, QuestionFilter

from main.models import Administrateur, Candidat, Etablissement, Evaluateur, Groupe, Invitation, Module, Question, Questionnaire,Reponse, Resultat, Test
from .forms import AccepterInvitForm, AdministrateurForm, CandidatForm, EtablissementForm, GroupeForm, ModuleForm, QuestionForm, QuestionForm2, QuestionnaireForm, ReponseForm, TestForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.models import Group
from main.decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages
from .forms import EvaluateurForm
from django import template
import json
from django.core import serializers
from django.contrib.auth import get_user_model


from django.contrib.auth.decorators import login_required
# Create your views here.

register = template.Library()

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin'])
def home(request):
    return render(request, 'main/index.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home_admin(request):
    nbeval = Evaluateur.objects.filter(etablissement = request.user.administrateur.etablissement).count()
    nbcandidat = Candidat.objects.filter(etablissement = request.user.administrateur.etablissement).count()
    nbadmin = Administrateur.objects.filter(etablissement = request.user.administrateur.etablissement).count()
    data1 = [nbadmin,nbeval,nbcandidat]
    print("nombre d'evaluateur = ",nbeval)
    print("nombre d'admin = ",nbadmin)
    print("nombre de candidat = ",nbcandidat)


    list_eval =Evaluateur.objects.filter(etablissement = request.user.administrateur.etablissement)
    nbmodule = Module.objects.filter(etablissement=request.user.administrateur.etablissement).count()
    group_list = Groupe.objects.filter(etablissement = request.user.administrateur.etablissement)
    nbgroupe = Groupe.objects.filter(etablissement = request.user.administrateur.etablissement).count()
    print(group_list)
    mylist1 = list(group_list)
    labels = []
    data = []
    for group in group_list:
        labels.append(group.nom)
        nbCandidat = Candidat.objects.filter(groupe=group).count()
        data.append(nbCandidat)
    
    
   
    context ={'nbeval':nbeval,'nbcandidat':nbcandidat,'nbmodule':nbmodule,'groupe_list':group_list,'labels':labels,'data':data,'data1':data1,'nbgroupe':nbgroupe}
    return render(request,'main/Admin/home_admin.html',context)


def base_admin(request):
    return render(request,'main/Admin/baseAdmin.html')




@login_required(login_url='login')
@allowed_users(allowed_roles=['evaluateur'])
def home_Evaluateur(request):    
    user = request.user
    module_list = Module.objects.filter(evaluateur=request.user.evaluateur)
    nbmodule = module_list.count()
    question_list = Question.objects.filter(module__in = module_list).distinct()
    questionnaire_list = Questionnaire.objects.filter(questions__in = question_list).distinct()
    test_list = Test.objects.filter(questionnaire__in = questionnaire_list).distinct()
    nbtest = test_list.count()
    groupe_list = Groupe.objects.filter(module__in=module_list).distinct()
    nbgroupe = groupe_list.count()
    candidat_list = Candidat.objects.filter(groupe__in=groupe_list).distinct()
    nbcandidat = candidat_list.count()
    
    return render(request,'main/Evaluateur/home_evaluateur.html',{'module_list':module_list,'nbmodule':nbmodule,'nbgroupe':nbgroupe,'nbcandidat':nbcandidat,'test_list':test_list,'nbtest':nbtest})

@login_required(login_url='login')
@allowed_users(allowed_roles=['candidat'])
def home_Candidat(request):
    invitation_list = Invitation.objects.filter(candidat=request.user.candidat)

    nbtest = invitation_list.count()


    return render(request,'main/Candidat/home_candidat.html',{'nbtest':nbtest})

@unauthenticated_user
def user_login(request):
    if request.method =='POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    if(request.user.groups.count()!=0):
                        group = request.user.groups.filter(user=request.user)[0]
                        if group.name=="admin":
                            if request.user.administrateur.isValide == True:
                                return redirect('home_admin')
                            else:
                                logout(request)
                                messages.info(request, 'Votre compte est desactivé, contactez un administrateur !')

                        elif group.name=="evaluateur":
                            if request.user.evaluateur.isValide == True:
                                return redirect('home_evaluateur')
                            else:
                                logout(request)
                                messages.info(request, 'Votre compte est desactivé, contactez un administrateur !')
                        elif group.name=="candidat":
                            if request.user.candidat.isValide == True:
                                return redirect('home_candidat')
                            else:
                                logout(request)
                                messages.info(request, 'Votre compte est desactivé, contactez un administrateur !')
                        elif group.name=="superadmin":
                            return redirect('home_superadmin') 
                    else:
                        logout(request)
                        messages.info(request, 'Votre compte est desactivé, contactez un administrateur !')
                else:
                    messages.info(request, 'username or password is incorrect')

    return render(request, 'main/user/login.html')



def add_Admin(request):
    form = AdministrateurForm
    submitted = False
    if request.method =="POST":
        form = AdministrateurForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('registeradmin?submitted=True')
    else:
        form = AdministrateurForm(request.POST)
        if 'submitted' in request.GET:
            submitted = True
    template = 'registeradmin.html'
    return render(request,template, {'form':form, 'submitted':submitted})

@unauthenticated_user
def user_register(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = form.cleaned_data.get('groups')
                for x in group:   
                    group1 = Group.objects.get(name=x)
                    user.groups.add(group1)
    

                
                username = form.cleaned_data.get('username')
                etab_name = form.cleaned_data.get('etablissement')
                etab = Etablissement.objects.get(nom=etab_name)
                if user.groups.filter(name='evaluateur').exists():
                   eval_obj = Evaluateur.objects.create(user=form.save(),etablissement=etab)
                elif user.groups.filter(name='admin').exists():
                    admin_obt = Administrateur.objects.create(user=form.save(),etablissement=etab)
                elif user.groups.filter(name='candidat').exists():
                    candidat_obt = Candidat.objects.create(user=form.save(),etablissement=etab)

                messages.success(request, 'Account was created for ' + username)
                return redirect('login')

                
    context = {'form':form}
    return render(request, 'main/user/register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def Profile_Admin(request):
    user = request.user
    admin = user.administrateur

    context = {'user':user}
    print(request.method)
    if request.method =='POST' and request.POST.get('first_name') is not None:
        nom = request.POST.get('first_name')
        prenom = request.POST.get('last_name')
        email = request.POST.get('email')
        user.last_name = nom
        user.first_name = prenom
        user.email = email
        user.save()
    if request.method == 'POST':
       
        request.FILES.get('avatar')
        if(request.FILES.get('avatar') is not None):
            admin.profile_pic = request.FILES.get('avatar')
            admin.save()
    return render(request, 'main/Admin/profile_admin.html',context)
### Partie Super Admin

def home_superadmin(request):
    nbeval = Evaluateur.objects.all().count()
    nbcandidat = Candidat.objects.all().count()
    nbetab = Etablissement.objects.all().count()
    nbadmin = Administrateur.objects.all().count()
    etablissement_list = Etablissement.objects.all()
    labels = []
    data = []
   
    data1 = [nbadmin,nbeval,nbcandidat]
    for etab in etablissement_list:
        labels.append(etab.nom)
        data.append(etab.nbeffectif())
    
    print(labels)
    print(data)
    data2 = [1,2,3]

    context = {'nbeval':nbeval,'nbcandidat':nbcandidat,'nbetab':nbetab,'nbadmin':nbadmin,'labels':labels,'data':data,'data1':data1}

    return render(request,'main/SuperAdmin/home_superadmin.html',context)

def all_administrateur(request):
    administrateur_list = Administrateur.objects.all()
    return render(request,'main/SuperAdmin/alladmin.html',{'administrateur_list':administrateur_list})

def list_administrateur(request):
    administrateur_list = Administrateur.objects.all()
    return render(request,'main/SuperAdmin/listadmin.html',{'administrateur_list':administrateur_list})

def update_administrateur(request, pk):

    administrateur = Administrateur.objects.get(id=pk)
    form = AdministrateurForm(instance=administrateur)

    if request.method =='POST':
        form = AdministrateurForm(request.POST, instance=administrateur)
        if form.is_valid():
            form.save()
            return redirect('list_administrateur')

    context = {'form':form}
    return render(request,'main/SuperAdmin/default_form.html',context)

def delete_administrateur(request, pk):
    administrateur = Administrateur.objects.get(id=pk)

    if request.method =="POST":
        administrateur.delete()
        return redirect('list_administrateur')

    context = {'item':administrateur}
    return render(request, 'main/SuperAdmin/deleteadmin.html', context)

def list_etablissement(request):
    etablissement_list = Etablissement.objects.all()
    return render(request,'main/SuperAdmin/listetablissement.html',{'etablissement_list':etablissement_list})

def update_etablissement(request, pk):

    etablissement = Etablissement.objects.get(id=pk)
    form = EtablissementForm(instance=etablissement)

    if request.method =='POST':
        form = EtablissementForm(request.POST, instance=etablissement)
        if form.is_valid():
            form.save()
            return redirect('list_etablissement')
        

    context = {'form':form}
    return render(request,'main/SuperAdmin/default_form.html',context)

def delete_etablissement(request, pk):
    etablissement = Etablissement.objects.get(id=pk)

    if request.method =="POST":
        etablissement.delete()
        return redirect('list_etablissement')
    
    context = {'item':etablissement}
    return render(request, 'main/SuperAdmin/deleteetablissement.html', context)
    
    

def CreateEtablissement(request):
    form = EtablissementForm()
    context = {'form':form}
    if request.method == 'POST':
        form = EtablissementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_superadmin')
        else:
            print('form invalide',form.errors)
    return render(request, 'main/SuperAdmin/default_form.html',context)

### Partie Admin



def test_evaluateur(request):
    user = request.user
    etablissement_list = Etablissement.objects.filter(nom = user.administrateur.etablissement)
    evaluateur_list = Evaluateur.objects.filter(etablissement = etablissement_list[0])
    return render(request,'main/Admin/alleval_admin.html',{'evaluateur_list':evaluateur_list})
def CreateEvaluateur(request):
    form = EvaluateurForm()
    context = {'form':form}
    if request.method == 'POST':
        form = EvaluateurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_admin')
        else:
            print('form invalide',form.errors)
    return render(request, 'main/Admin/default_form.html',context)

def update_evaluateur(request, pk):

    evaluateur = Evaluateur.objects.get(id=pk)
    form = EvaluateurForm(instance=evaluateur)

    if request.method =='POST':
        form = EvaluateurForm(request.POST, instance=evaluateur)
        if form.is_valid():
            form.save()
            return redirect('list_eval')

    context = {'form':form}
    return render(request,'main/Admin/default_form.html',context)

def deleteEvaluateur(request, pk):
    evaluateur = Evaluateur.objects.get(id=pk)

    if request.method =="POST":
        evaluateur.delete()
        return redirect('list_eval')

    context = {'item':evaluateur}
    return render(request, 'main/Admin/delete.html', context)

def all_candidat(request):  
    candidat_list = Candidat.objects.filter(etablissement = request.user.administrateur.etablissement)
    return render(request,'main/Admin/allcandidat_admin.html',{'candidat_list':candidat_list})

def list_candidat(request):
    candidat_list = Candidat.objects.filter(etablissement = request.user.administrateur.etablissement)
    return render(request,'main/Admin/listcandidat_admin.html',{'candidat_list':candidat_list})

def update_candidat(request, pk):

    candidat = Candidat.objects.get(id=pk)
    form = CandidatForm(instance=candidat)

    if request.method =='POST':
        form = CandidatForm(request.POST, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('list_candidat')

    context = {'form':form}
    return render(request,'main/Admin/default_form.html',context)

def deleteCandidat(request, pk):
    candidat = Candidat.objects.get(id=pk)

    if request.method =="POST":
        candidat.delete()
        return redirect('list_candidat')

    context = {'item':candidat}
    return render(request, 'main/Admin/deletecandidat.html', context)

def all_module(request):
    user = request.user
    etablissemen = Etablissement.objects.get(id = user.administrateur.etablissement.id)
    module_list = Module.objects.filter(etablissement=etablissemen) 

    return render(request,'main/Admin/allmodule_admin.html',{'module_list':module_list})

def list_module(request):
    user = request.user
    module_list = Module.objects.filter(etablissement=user.administrateur.etablissement)
    myFilter = ModuleFilter(request.GET, queryset=module_list)
    module_list = myFilter.qs
    return render(request,'main/Admin/listmodule_admin.html',{'module_list':module_list,'myFilter':myFilter})

def update_module(request, pk):

    module = Module.objects.get(id=pk)
    form = ModuleForm(user = request.user,instance=module)

    if request.method =='POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('list_module')

    context = {'form':form}
    print(form.errors)
    return render(request,'main/Admin/default_form.html',context)

def deleteModule(request, pk):
    module = Module.objects.get(id=pk)
    if request.method =="POST":
        module.delete()
        return redirect('list_module')
    context = {'item':module}
    return render(request, 'main/Admin/deletemodule.html', context)

def CreateModule(request):
    form = ModuleForm(user = request.user)
    context = {'form':form}
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.instance.etablissement = request.user.administrateur.etablissement
            form.save()
            return redirect('home_admin')
    return render(request, 'main/Admin/default_form.html',context)

## Groupes 
def list_groupe(request):
   
                    
    groupe_list = Groupe.objects.filter(etablissement = request.user.administrateur.etablissement)
    return render(request,'main/Admin/listgroupe_admin.html',{'groupe_list':groupe_list})


def list_module_groupe(request,pk):         
    groupe = Groupe.objects.get(id=pk)
    module_list = Module.objects.filter(groupes = groupe)
    print(module_list)
    return render(request,'main/Admin/module_groupe_admin.html',{'module_list':module_list,'groupe':groupe})

def update_groupe(request, pk):

    groupe = Groupe.objects.get(id=pk)
    form = GroupeForm(user=request.user,instance=groupe)

    if request.method =='POST':
        form = GroupeForm(request.POST, instance=groupe)
        if form.is_valid():
            form.instance.etablissement = Etablissement.objects.get(id=request.user.administrateur.etablissement.id)
            form.save()
            return redirect('list_groupe')

    context = {'form':form}
    return render(request,'main/Admin/default_form.html',context)

def deleteGroupe(request, pk):
    groupe = Groupe.objects.get(id=pk)

    if request.method =="POST":
        groupe.delete()
        return redirect('list_groupe')

    context = {'item':groupe}
    return render(request, 'main/Admin/deletegroupe.html', context)

def CreateGroupe(request):
    form = GroupeForm(user=request.user)
    context = {'form':form}
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.instance.etablissement = Etablissement.objects.get(id=request.user.administrateur.etablissement.id)
            form.save()
            return redirect('list_groupe')
    return render(request, 'main/Admin/default_form.html',context)

def all_groupe(request):
    
    groupe_list = Groupe.objects.filter(etablissement = request.user.administrateur.etablissement)
    return render(request,'main/Admin/allgroupe_admin.html',{'groupe_list':groupe_list})
        
def home_groupe(request,pk):
    groupe = Groupe.objects.get(pk=pk)
    list_candidat = Candidat.objects.filter(groupe=groupe)
    nb_candidat = list_candidat.count()
    nb_module = Module.objects.filter(groupes=groupe).count()
    print(list_module)
    
    return render(request,'main/Admin/homegroupe_admin.html',{'groupe':groupe,'list_candidat':list_candidat,'nb_candidat':nb_candidat,'nb_module':nb_module})

## Partie Evaluateur
## Module

def lobby(request):
    return render(request, 'main/Admin/chat_admin.html')


def Profile_Evaluateur(request):
    user = request.user
    eval = user.evaluateur

    context = {'user':user}
    if request.method == 'POST' and request.POST.get('nom') is not None:
        nom = request.POST.get('nom')
        print("slm")
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        user.last_name = nom
        user.first_name = prenom
        user.email = email
        user.save()
    if request.method == 'POST':
        request.FILES.get('avatar')
        if(request.FILES.get('avatar') is not None):
            eval.profile_pic = request.FILES.get('avatar')
            eval.save()
            print(eval)
        
    return render(request, 'main/Evaluateur/profile_evaluateur.html',context)

def all_moduleEval(request):
    user = request.user
    module_list = Module.objects.filter(evaluateur = request.user.evaluateur)
    

    return render(request,'main/Evaluateur/allmodule_evaluateur.html',{'module_list':module_list})

def list_question(request):
    user = request.user
    module_list = Module.objects.filter(evaluateur = request.user.evaluateur)
    question_list = Question.objects.filter(module__in = module_list)
    return render(request,'main/Evaluateur/listquestion_evaluateur.html',{'question_list':question_list})

def list_question_module(request,pk):
    user = request.user
    module_list = Module.objects.filter(id=pk)
    module = Module.objects.get(id=pk)
    print(module_list)
    question_list = Question.objects.filter(module__in = module_list)
    myFilter = QuestionFilter(request.GET, queryset=question_list)
    question_list = myFilter.qs
    return render(request,'main/Evaluateur/listqmod_evaluateur.html',{'question_list':question_list,'module':module,'myFilter':myFilter})

def list_questionnaire_module(request,pk):
    user = request.user
    module = Module.objects.get(id=pk)
    print(module.id)
    question_list = Question.objects.filter(module = module)
    questionnaire_list = Questionnaire.objects.filter(questions__in = question_list).distinct()
    return render(request,'main/Evaluateur/listqsmod_evaluateur.html',{'questionnaire_list':questionnaire_list,'module':module})

def update_questionnaire(request, pk1,pk):
    
####Pour le redirect
    questionnaire = Questionnaire.objects.get(id=pk1)
    form = QuestionnaireForm(user=request.user,pk=pk,instance=questionnaire)

    if request.method =='POST':
        form = QuestionnaireForm(request.POST, instance=questionnaire)
        if form.is_valid():
            form.save()
            return redirect('listqsmod',pk)
    context = {'form':form}
    return render(request,'main/Evaluateur/default_form.html',context)





def update_question(request, pk1,pk):
    question = Question.objects.get(id=pk)
    module = Module.objects.get(id=pk1).id
    form = QuestionForm(instance=question,user=request.user)
    ReponseFormSet = inlineformset_factory(Question, Reponse, fields=('contenurep','isTrue','valeur',),max_num=4,extra=1,widgets={'contenurep': TextInput(attrs={'class':'form-control col-sm-2','id':'montext'}),'valeur' :NumberInput(attrs={'class' : 'form-control col-sm-2'}) } )
    if request.method == 'POST':
            form = QuestionForm(request.POST, instance = question)
            formset = ReponseFormSet(request.POST, instance = question)
            if formset.is_valid() and form.is_valid():
                form.save()
                formset.save()        
                print("slm")
                return redirect('listqmod',module)
    formset = ReponseFormSet(instance = question)
    return render(request, 'main/Admin/formset.html', {'formset' : formset,'form':form})


def home_module(request,pk):
    module = Module.objects.get(id=pk)
    question_list = Question.objects.filter(module = module).distinct()
    nb_question = Question.objects.filter(module = module).distinct().count()
    questionnaire_list = Questionnaire.objects.filter(questions__in = question_list).distinct()
    nb_questionnaire = questionnaire_list.count()
    test_list = Test.objects.filter(questionnaire__in=questionnaire_list).distinct()
    nb_test = test_list.count()
    print(module.groupes.all())
    nb_groupes = module.groupes.count()
    return render(request,'main/Evaluateur/module_evaluateur.html',{'module':module,'nbquestion':nb_question,'nbquestionnaire':nb_questionnaire,'nbtest':nb_test,'nbgroupe':nb_groupes})

def home_test(request,pk,pk1):
    module = Module.objects.get(id=pk)
    test = Test.objects.get(id=pk1)
    list_groupe = Groupe.objects.filter(module = module)
    list_candidat = Candidat.objects.filter(groupe__in = list_groupe).distinct()
    context = {'test':test,'module':module}
    return render(request,'main/Evaluateur/home_test.html',context)


def CreateQuestion(request):
    form = QuestionForm(user=request.user)
    question = None
    ReponseFormSet = inlineformset_factory(Question, Reponse, fields=('contenurep','isTrue','valeur',),max_num=3,can_delete=False,widgets={'contenurep': TextInput(attrs={'class':'form-control','id':'montext'}),'valeur' :NumberInput(attrs={'class' : 'form-control'}) } )
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            question = Question.objects.get(id=form.instance.id)
            formset = ReponseFormSet(request.POST, instance = question)
            if formset.is_valid():
                formset.save()
                return redirect('home_evaluateur')
    formset = ReponseFormSet(instance= question)
    return render(request, 'main/Admin/formset.html',{'form':form,'formset':formset})

def CreateQuestion2(request,pk):
    
    init = {
        'module': pk
    }
    form = QuestionForm2(user=request.user,pk=pk,initial=init)
    question = None
    module = Module.objects.get(id=pk)
   
    ReponseFormSet = inlineformset_factory(Question, Reponse, fields=('contenurep','isTrue','valeur',),max_num=3,can_delete=False,widgets={'contenurep': TextInput(attrs={'class':'form-control','id':'montext'}),'valeur' :NumberInput(attrs={'class' : 'form-control'}) } )
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.module = module
            form.save()
            question = Question.objects.get(id=form.instance.id)
            formset = ReponseFormSet(request.POST, instance = question)
            if formset.is_valid():
                formset.save()
                return redirect('listqmod',pk)
    formset = ReponseFormSet(instance= question)
    return render(request, 'main/Admin/formset.html',{'form':form,'formset':formset})

def deleteQuestion2(request, pk):
    question = Question.objects.get(id=pk)
    module = Module.objects.get(id=question.module.id)
    id = module.id
    

    if request.method =="POST":
        question.delete()
        return redirect('listqmod',id)

    context = {'item':question,'id':id}
    return render(request, 'main/Evaluateur/deletequestion1.html', context)

def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)

    if request.method =="POST":
        question.delete()
        return redirect('list_question')

    context = {'item':question}
    return render(request, 'main/Evaluateur/deletequestion.html', context)

def CreateQuestionnaire(request,pk):
    form = QuestionnaireForm(user=request.user,pk=pk)
    context = {'form':form}
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listqsmod',pk)
    return render(request, 'main/Evaluateur/default_form.html',context)


def deleteQuestionnaire(request, pk1,pk):
    questionnaire = Questionnaire.objects.get(id=pk1)
    module = Module.objects.get(id=pk)
    if request.method =="POST":
        questionnaire.delete()
        return redirect('listqsmod',pk)

    context = {'item':questionnaire,'module':module}
    return render(request, 'main/Evaluateur/delete_questionnaire.html', context)

def list_test_module(request,pk):
    user = request.user
    module = Module.objects.get(id=pk)
    question_list = Question.objects.filter(module = module)
    questionnaire_list = Questionnaire.objects.filter(questions__in = question_list).distinct()
    test_list = Test.objects.filter(questionnaire__in = questionnaire_list)
    return render(request,'main/Evaluateur/listtestmod_evaluateur.html',{'test_list':test_list,'module':module})

def update_test(request,pk1,pk):
    
    test = Test.objects.get(id=pk1)
    form = TestForm(user=request.user,pk=pk,instance=test)

    if request.method =='POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('listtestmod',pk)
    context = {'form':form}
    return render(request,'main/Evaluateur/default_form.html',context)

def deleteTest(request, pk1,pk):
    test = Test.objects.get(id=pk1)
    module = Module.objects.get(id=pk)

    if request.method =="POST":
        test.delete()
        return redirect('listtestmod',pk)

    context = {'item':test,'module':module}
    return render(request, 'main/Evaluateur/delete_test.html', context)

def CreateTest(request,pk):
    form = TestForm(user=request.user,pk=pk)
    context = {'form':form}
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listtestmod',pk)
    return render(request, 'main/Evaluateur/default_form.html',context)

def PasserTest(request,pk):
    test = Test.objects.get(id=pk)
    questionnaire = Questionnaire.objects.get(id = test.questionnaire.id)
    print(questionnaire.questions.all())
    list_question = questionnaire.questions.all()
    
    list_reponses = Reponse.objects.filter(question__in = list_question)
    context = {'test':test,'questionnaire':questionnaire,'list_question':list_question,'list_reponses':list_reponses}

    return render(request,'main/Candidat/passagetest_candidat.html',context)

class QuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'main/Candidat/main.html'

def Questionnaire_View(request, pk):
    test = Test.objects.get(pk=pk)
   
    questionnaire = Questionnaire.objects.get(id=test.questionnaire.id)
    datefin1 =test.DateFin
    datefin = datefin1.strftime("%Y-%m-%dT%H:%M:%S")
    
    return render(request, 'main/Candidat/quiz.html', {'questionnaire':questionnaire,'datefin':datefin})

def Questionnaire_data_view(request,pk):
    test = Test.objects.get(pk=pk)
    questionnaire = Questionnaire.objects.get(id=test.questionnaire.id)
    questions = []
    questionsqcs = []
    questionsRL = []
    for q in questionnaire.questions.all():
        if(q.type=='QCM'):
            reponses = []
            for r in q.get_reponses():
                reponses.append(r.contenurep)
            questions.append({str(q): reponses})
        elif(q.type=='QCS'):
            reponsesqcs = []
            for r in q.get_reponses():
                reponsesqcs.append(r.contenurep)
            questionsqcs.append({str(q): reponsesqcs})
        
        
        
    
    print(questions)
    return JsonResponse({
        'data': questions,
        'data2':questionsqcs,
        
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def save_quiz_view(request, pk):
    if is_ajax(request=request):
        questions = []
        data= request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        

        for k in data_.keys():
            if(data_[k][0]!=''):   
                size = len(k)
                k = k[:size - 2]
                question = Question.objects.get(contenu=k)
                questions.append(question)
            elif(data_[k][0]==''):
                question = Question.objects.get(contenu=k)
                questions.append(question)


        #Candidat = request.user.candidat
        test = Test.objects.get(pk=pk)
        quiz = Questionnaire.objects.get(id=test.questionnaire.id)

        score = 0
        multiplier = 100 / quiz.questions.all().count()
        results = []
        correct_answer = None

        for q in questions:
            y = q.contenu + '[]'
           
            a_selected = request.POST.getlist(y)
            if a_selected != "":
                questions_answers = Reponse.objects.filter(question=q)
                # Verifier si les réponses sont justes
                for a in questions_answers:
                    for a_s in a_selected:
                        if a_s == a.contenurep:
                            if a.isTrue:
                                score += a.valeur
                                correct_answer = a.contenurep
                            else:
                                if a.isTrue == False:
                                    correct_answer = a.contenurep
                                    score += a.valeur

                results.append({str(q): {'correct_answer': correct_answer,'answered':a_selected}})
            else:
                results.append({str(q): 'not answered'})
        
        score_ = score * multiplier
        print(data_)
        if(Resultat.objects.filter(candidat = request.user.candidat,test=test).exists()):
            #Redirect
            return HttpResponse("Vous avez deja passé ce test !")
        else:
            resultat = Resultat.objects.create(candidat = request.user.candidat, test = test, score = score,copie = data_)
            invit = test.get_invitation(user=request.user)
            invit.status = 2
            invit.save()
            return JsonResponse({
                'success': True,
                'url': reverse('home_candidat', args=[]),})
        if score_ >= 50 :
            return JsonResponse({'passed':True, 'score':score,'results':results})
        else:
            return JsonResponse({'passed':False, 'score':score,'results':results})
    

    return JsonResponse({'text':'works'})       

#Bouton invitation de l'evaluateur
##Fonction pour generer un code alphabétique au hasard
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
##

def Inviter_Candidat(request,pk,pk1):   
   
    module = Module.objects.get(id=pk)
    list_groupes = Groupe.objects.filter(module = module)
    test = Test.objects.get(id=pk1)
    list_candidat = Candidat.objects.filter(groupe__in= list_groupes).distinct()
    print(list_candidat)
    if request.method =="POST":
        for c in list_candidat:
            mdp = str(test.id)+get_random_string(6)
            i = Invitation.objects.create(test = test,candidat=c,code = mdp,status = 0 )
            send_mail(
    'Code de confirmation de test',
    'Bonjour '+c.user.first_name+"\n Ceci est un code d'accès afin de confirmer votre participation au test : "+test.nom+"\n Code d'accès : "+str(i.code),
    settings.EMAIL_HOST_USER,
    [c.user.email],
    fail_silently=False,
)
        return redirect('listtestmod',pk)
    context = {'module':module,'test':test}
    return render(request,'main/Evaluateur/invitation_evaluateur.html', context)

def Delete_Invitation(request,pk,pk1):   
   
    module = Module.objects.get(id=pk)
    list_groupes = Groupe.objects.filter(module = module)
    test = Test.objects.get(id=pk1)
    list_candidat = Candidat.objects.filter(groupe__in= list_groupes).distinct()
    print(list_candidat)
    if request.method =="POST":
        Invitation.objects.filter(test=test).delete()
        return redirect('listtestmod',pk)
    context = {'module':module,'test':test}
    return render(request,'main/Evaluateur/delete_invitation.html', context)

def Resultat_test_Evaluateur(request,pk,pk1):
    module = Module.objects.get(id=pk)
    test = Test.objects.get(id=pk1)
    print(test)
    resultat = Resultat.objects.filter(test=test)
    print(resultat)
    

    context = {'module':module,'test':test,'resultat':resultat}

    return render(request,'main/Evaluateur/resultat_test.html',context)



def ResultatTestCopieEval(request,pk,pk1,pk2):
    module = Module.objects.get(id=pk)
    test = Test.objects.get(id=pk1)
    resultat = Resultat.objects.get(id=pk2)
    note = resultat.score

    questionnaire = Questionnaire.objects.get(id=test.questionnaire.id)
    questions = []
    for q in questionnaire.questions.all():
        reponses = []
        for r in q.get_reponses():
            reponses.append(r.contenurep)
        questions.append({str(q): reponses})
    
    json.dumps(questions)
    context = {'module':module,'test':test,'note':note,'resultat':resultat,'questions':questions}

    return render(request,'main/Evaluateur/copie_candidat.html',context)



## Partie candidat

def Profile_Candidat(request):
    user = request.user

    candidat = user.candidat
    print("slm")
    if request.method =='POST' and request.POST.get('nom') is not None:
        print("ok")
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        print(request.POST)
        user.last_name = nom
        user.first_name = prenom
        user.email = email
        user.save()

    context = {'user':user}
    if request.method == 'POST':
       
        request.FILES.get('avatar')
        if(request.FILES.get('avatar') is not None):
            candidat.profile_pic = request.FILES.get('avatar')
            candidat.save()

    context = {'user':user}


    return render(request, 'main/Candidat/profile_candidat.html',context)


def list_test_candidat(request):

    invitation_list = Invitation.objects.filter(candidat=request.user.candidat)
    
    list_test = []
    for invit in invitation_list:
        list_test.append(Test.objects.get(id=invit.test.id))
        

    context = {'list_test':list_test,'user':request.user}
    return render(request,'main/Candidat/listtest_candidat.html',context)

def Test_AttenteConfirmation(request,pk):
    test = Test.objects.get(id=pk)
    invitation = test.get_invitation(request.user)
    
    mdp = invitation.code
    form = AccepterInvitForm
    message = ''
    if request.method =="POST":
        if(request.POST.get("code")==mdp):
            message = 'Code correct, reservation du test confirmé !'
            invitation.status = 1
            invitation.save()
            return redirect('my_tests')

        else:
            print("mot de passe incorrect")
            message = 'Code incorrect'

    context = {'test':test,'form':form,'message':message}
    return render(request,'main/Candidat/testenAttente.html',context)


def Pret_PasserTest(request,pk):
    test = Test.objects.get(id=pk)
    current_datetime = datetime.now(timezone.utc) + timedelta(hours=1)
    invitation = test.get_invitation(request.user)
    message = ''
    if request.method=="POST":
        if(current_datetime- test.DateDeb > timedelta(seconds=0)):
            print("on peut1")
            if(current_datetime-test.DateFin < timedelta(seconds=0)):
                print("on peu2t")
                return redirect('quiz-view',test.id)
                return HttpResponse('Bienvenue au test')
            else:
                message = 'Le test a expiré !'
        else:
            message = 'Le test n as pas encore commencé !'

                
            
    context = {'test':test,'message':message}
    return render(request,'main/Candidat/pret_passertest.html',context)

def ResultatTest(request,pk):
    test = Test.objects.get(id=pk)
    resultat = Resultat.objects.get(test=test,candidat=request.user.candidat)
    note = resultat.score

    context = {'test':test,'note':note}



    return render(request,'main/Candidat/resultat_test.html',context)


def ResultatTestCopie(request,pk):
    test = Test.objects.get(id=pk)
    resultat = Resultat.objects.get(test=test,candidat=request.user.candidat)
    note = resultat.score

    questionnaire = Questionnaire.objects.get(id=test.questionnaire.id)
    questions = []
    for q in questionnaire.questions.all():
        reponses = []
        for r in q.get_reponses():
            reponses.append(r.contenurep)
        questions.append({str(q): reponses})
    
    json.dumps(questions)
    context = {'test':test,'note':note,'resultat':resultat,'questions':questions}



    return render(request,'main/Candidat/resultat_testcopie.html',context)






def AddQuestion(request,pk):
    module = Module.objects.get(id=pk)
    message = ''

    if(request.method=="POST"):
        print(request.POST)
        x = request.POST.get("valeur")
        type = request.POST.get("type")
        reponses = []
        tab = x.rsplit("\r\n")
        if  len(tab) != 0 and len(tab) != 1:
            quest = tab[0]
            if(type=='QCM'):
                question = Question.objects.create(contenu=quest,module=module,tag = request.POST.get("tag"),type='QCM')
            elif(type=='QCS'):
                question = Question.objects.create(contenu=quest,module=module,tag = request.POST.get("tag"),type='QCS')
            for e in tab:
                if(e[0]=="+"):
                    reponses.append(Reponse.objects.create(contenurep =e[3:],isTrue=True,valeur=int(e[0:2]),question=question))
                elif(e[0]=="-"):
                    reponses.append(Reponse.objects.create(contenurep =e[3:],isTrue=False,valeur=int(e[0:2]),question=question))
            return redirect('listqmod',module.id)
        else:
            message = 'Veuillez remplire le formulaire.'

    context = {'message':message}        




    return render(request,'main/Evaluateur/add_question.html',context)





