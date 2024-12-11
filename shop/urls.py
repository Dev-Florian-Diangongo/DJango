

from django.urls import path
from .views import *
urlpatterns = [
    path('creer/', creationCompte, name="creationCompte"),
    path('confirmationCompte/<str:numero_compte>/', confirmationCompte, name="confirmationCompte"),
    path('home', home, name="home"),
    path('clotureCompte/<int:id_compte>/', clotureCompte, name="clotureCompte"),
    path('Transaction/', Transaction, name="Transaction"),
    path('historique_transaction/', historique_transaction, name="historique_transaction"),
    path('Transfert_Interne/', Transfert_Interne, name="Transfert_Interne"),
    path('graphique/', graphique, name="graphique"),
    path('transfert_entre_user/', transfert_entre_user, name="transfert_entre_user"),
    path('consultation_compte_user/', consultation_compte_user, name="consultation_compte_user"),
    path('historique_transfert_user/', historique_transfert_user, name="historique_transfert_user"),
    path('modification_du_compte/<int:id>/', MofifierCompte, name="modification_du_compte"),
    path('suppression_du_compte/<int:id>/', supprimer_compte, name="suppression_du_compte"),
    path('confirmationSuppression/<int:id>/', confirmationSuppression, name="confirmationSuppression"),
    path('supprimer_ou_non/<int:id>/', supprimer_ou_non, name="supprimer_ou_non"),
    

   
]
