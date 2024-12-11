
from django.urls import path, include

from accounts.views import connexion, inscription,verificationEmail, edit_mot_de_passe, deconnexion

urlpatterns = [
    path('', inscription, name="inscription"),
    path('connexion/', connexion, name="connexion"),
    path('deconnexion/', deconnexion, name="deconnexion"),
    path('verificationEmail/', verificationEmail, name="verificationEmail"),
    path('edit_mot_de_passe/<str:email>/', edit_mot_de_passe, name="edit_mot_de_passe"),
]
