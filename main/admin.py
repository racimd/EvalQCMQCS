from django.contrib import admin

# Register your models here.
from .models import Etablissement,Administrateur,Evaluateur,Groupe, Invitation,Module,Candidat,Question,Questionnaire,Test,Reponse,Resultat



class AnswerAdmin(admin.StackedInline):
  model = Reponse

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]

admin.site.register(Invitation)
admin.site.register(Etablissement)
admin.site.register(Administrateur)
admin.site.register(Evaluateur)
admin.site.register(Groupe)
admin.site.register(Module)
admin.site.register(Candidat)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reponse)
admin.site.register(Questionnaire)
admin.site.register(Test)
admin.site.register(Resultat)
