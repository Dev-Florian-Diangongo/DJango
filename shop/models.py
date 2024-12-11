from django.db import models
from accounts.models import User
# Create your models here.
class CompteBancaire(models.Model) :
  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    types_compte = models.CharField(max_length=30)  
    numero_compte = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=13)
    solde = models.DecimalField(max_digits=20, decimal_places=2)
    devise = models.CharField(max_length=3, default="USD")
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    code_pin = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.numero_compte} ({self.user.username})"

class TransactionClient(models.Model) :
    TYPES_TRANSACTION = [
        ("depot", "Depôt"),
        ('retrait' , "Retrait"),
    ]
    STATUTS_TRANSACTION = [
        ("e_attente", "En attente"),
        ("Completee", "Complétée"),
        ("annulee","Annulée"),
    ]
    id_transaction = models.AutoField(primary_key = True)
    compte = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE)
    type_transaction = models.CharField(max_length=30, choices=TYPES_TRANSACTION)
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    devise = models.CharField(max_length=3, default='USD')
    date_heure = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    statut = models.CharField(STATUTS_TRANSACTION, max_length=20)
    def __str__(self) :
        return f"Transaction  {self.id_transaction} -- ({self.type_transaction}) -- ({self.montant}) -- ({self.devise})"
    
class TransfertInterne(models.Model) :
    id_transfert = models.AutoField(primary_key=True)
    compte_source = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE, related_name="transafert_source")
    compte_destination = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE, related_name="transfert_destination")
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    devise = models.CharField(max_length=3,default="USD" )
    date_heure = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    statut = models.CharField(max_length=10)
    
    def __str__(self) :
        return f" Transfert {self.id_transfert}-- ({self.montant})--({self.devise})--({self.compte_source}) --({self.compte_destination})"
class TransfertExterne(models.Model) :
    compte_source = models.ForeignKey(CompteBancaire, on_delete=models.CASCADE)
    compte_destination = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    description  = models.CharField(max_length=150)
    devise = models.CharField(max_length=3, default="USD")
    date_heure = models.DateTimeField(auto_now_add=True)