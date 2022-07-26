from dataclasses import fields
from django import forms
import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ModuleFilter(django_filters.FilterSet):
    nom = CharFilter(field_name='nom',lookup_expr='icontains',label="",widget=forms.TextInput(attrs={'class': 'form-control bg-light border-0 small','placeholder':'Search for...','aria-label':'Search',
            'aria-describedby':'basic-addon2' }))
    class Meta:
        model = Module
        fields = ('nom',)
        
        exclude = []

class QuestionFilter(django_filters.FilterSet):
    tag = CharFilter(field_name='tag',lookup_expr='icontains',label="",widget=forms.TextInput(attrs={'class': 'form-control bg-light border-0 small','placeholder':'Search by tag...','aria-label':'Search',
            'aria-describedby':'basic-addon2' }))
    class Meta:
        model = Question
        fields = ('tag',)
        
        exclude = []
