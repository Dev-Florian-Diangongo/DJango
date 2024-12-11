

# from django import forms
# from .models import CompteBancaire

# class FormulaireCreationCompteBancaire(forms.ModelForm) :
#     class Meta :
#         model = CompteBancaire
#         fields = ["numero_compte", 
#                   "types_compte", 
#                   "solde",
#                   "phone",
#                     "devise",
#                   "limite_retrait",
#                   "limite_depot",
#                   "info_bank",
#                   "code_pin",
#                   "titulaire_secondaire",
#                   "notes" ]
#         widget = {
#             "numero_compte" : forms.TextInput(attrs={"class":"form-control"}),
#             "types_compte" : forms.Select(attrs={"class" : "form-control"}),
#             "solde" : forms.NumberInput(attrs={"class":'form-control'}),
#             "phone" : forms.TextInput(attrs={"class":"form-control"}),
#             "devise" : forms.TextInput(attrs={"class":"form-control"}),
#             "limite_retrait" : forms.NumberInput(attrs={"class":"form-control"}),
#             "limite_depot" : forms.NumberInput(attrs={"class":"form-control"}),
#             "info_bank" : forms.Textarea(attrs={"class":"form-control"}),
#             "code_pin":forms.NumberInput(attrs={"class":"form-control"}),
#             "titulaire_secondaire" : forms.Select(attrs={"class":"form-control"}),
#             "notes" : forms.Textarea(attrs={"class":"form-control"})

#         }