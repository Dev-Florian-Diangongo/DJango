from django.contrib import admin
from .models import *
# Register your models here.

class AdminCompteBancaire(admin.ModelAdmin) :
    list_display = ["user","types_compte", "numero_compte",
                    "phone","solde",
                    "devise","date_creation","date_mise_a_jour",
                    "code_pin",]
class AdminTransactionClient(admin.ModelAdmin):
    list_display = ["id_transaction","compte","type_transaction",
                    "montant","devise","date_heure",
                    "description","statut"]
class  AdminTransfertInterne(admin.ModelAdmin) :
    list_display = ["id_transfert", "compte_source","compte_destination",
                    "montant","devise","date_heure",
                    "description","statut"]
class AdminTransfertExtern(admin.ModelAdmin) :
    list_display = [
        "compte_source",
        "compte_destination",
        "montant",
        "description",
        "devise",
        "date_heure",
    ]
admin.site.register(TransfertInterne,AdminTransfertInterne )
admin.site.register(CompteBancaire,AdminCompteBancaire)
admin.site.register(TransactionClient, AdminTransactionClient)