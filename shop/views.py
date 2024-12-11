

from django.shortcuts import render, redirect
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from _decimal import Decimal
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from .models import CompteBancaire, TransactionClient, TransfertInterne, TransfertExterne
import string
import random
from random import randint
from random import choice
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

from twilio.rest import Client
# fonncion pour envoyer des sms pour chaque transaction
def sms(num, message) :
    account_sid ="ACde378833334f8b52104df369df56f601"
    auth_token = "a8896d9a96c8c780457c5a1114ff1182"
    twilio_number = "+14177390346"
    try :
        client = Client(account_sid, auth_token)
        client = client.messages.create(
            body=message, 
            from_= twilio_number,
            to=num
        )
    except Exception as e :
        print(e)
# fonction pour faire la validation de numero


# fonction pour generer le numero de compte bancaire
def generer_numero_compte() :
    prefix_nombre = "155"
    suffix_nombre = "".join([str(random.randint(0, 9)) for char in range(10)])
    code_final = prefix_nombre + suffix_nombre
    return code_final

# fonction pour acceder à la page d'acceuil
login_required(login_url="connexion")
def home(request) :
    return render(request, "shop/home.html")

@login_required(login_url="connexion")
def creationCompte(request) :
    message = ""
    if request.method == "POST" :
        types_compte = request.POST.get("types_compte")
        numero_compte = generer_numero_compte()
        phone = request.POST.get("phone")
        solde = request.POST.get("solde")
        devise = request.POST.get("devise")
        code_pin = request.POST.get("code_pin")
        if types_compte is None or numero_compte is None or numero_compte is None or phone is None or solde is None or devise is None or devise is None or code_pin is None :
            message_all = "tous les champs sont obligatoires !"
            return render(request, "shop/creationCompteBancaire.html", context={'message_all':message_all})
        if len(code_pin) > 5 or len(code_pin)< 4:
            message = "le code pin doit avoir 4 chiffres !"
            return render(request, "shop/creationCompteBancaire.html", context={'message':message})
        if any(char.isalpha() for char in code_pin) :
            message = "le code pin doit avoir que que de chiffres et non de lettre !"
            return render(request, "shop/creationCompteBancaire.html", context={'message':message})
        try :
            message =""
            phone_number = str(phone)
            parsed_number = phonenumbers.parse(phone_number, None)
            print(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)
            if not is_possible :
                message = "le numero n'est pas posible"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            is_vali = phonenumbers.is_valid_number(parsed_number)
            if not is_vali:
                message = "le numero n'est pas valide"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            region = geocoder.region_code_for_number(parsed_number)
            if not region :
                message = "le numero n'a pas de region"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            localisation = geocoder.description_for_number(parsed_number, "fr")
            if not localisation:
                message = "le numero n'est pas localisable"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            number_type = phonenumbers.number_type(parsed_number)
            if not number_type :
                message = "le numero est faux"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            operator = carrier.name_for_number(parsed_number, 'fr')
            if not  operator:
                message = "nous n'avons pas trouver l'operateur"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            time_zone = timezone.time_zones_for_number(parsed_number)
            if CompteBancaire.objects.filter(numero_compte=numero_compte).exists() :
                message = "le numero de compte existe déjà !"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            solde_decimal = Decimal(solde)
            print(numero_compte)
            
            
            cache.set( f"account_data_{numero_compte}", {
                "user" :request.user,
                "types_compte" :types_compte,
                "numero_compte" : numero_compte,
                "phone" :parsed_number,
                "solde"  : solde_decimal,
                "devise" : devise,
                "code_pin" : code_pin}, timeout=300 # 5 minutes
            )
            message = f"Bonjour {request.user}. \n voici le code de votre compte bancaire : {numero_compte}. \n Vous devez le confirmer sur notre plateforme pour confirmer le compte."
            sms(parsed_number, message=message)
            return redirect("confirmationCompte", numero_compte=numero_compte)
        except Exception as e  :
            message = f"problème du sytème ! {e}"
            return render(request,"shop/creationCompteBancaire.html", context={'message':message})
    return render(request, "shop/creationCompteBancaire.html", context={'message':message})        

# fonction pour confirmer le numero de compte envoyé par sms
login_required(login_url='connexion')
def confirmationCompte(request, numero_compte) :
    if request.method == "POST" :
        number_confirm = request.POST.get("confirmation_number")
        if number_confirm is None :
            message = "le champ est obligatoire"
            return render(request, "shop/confirmationCompte.html", context={"message" : message})
        else :
            if  number_confirm  != numero_compte :
                message = "code de confirmation est incorrect !" 
                return render(request, "shop/confirmationCompte.html", context={"message" : message})
            else :
                account_data = cache.get(f"account_data_{numero_compte}") # get datas in cache memory
                if account_data :
                    compte = CompteBancaire.objects.create( # create and save the account data
                    user = account_data["user"], 
                    types_compte = account_data["types_compte"], 
                    numero_compte= account_data["numero_compte"], 
                    phone = account_data["phone"], 
                    solde = account_data["solde"], 
                    devise = account_data["devise"], 
                    code_pin = account_data["code_pin"], 
                    )
                    compte.save()
                    return redirect("home")
                else :
                    message = "les delai est expiré, veuillez recommencer la procedure de la creation du compte bancaire"
                    return render(request, "shop/confirmationCompte.html", context={"messages" : message})
    return render(request, "shop/confirmationCompte.html")


@login_required(login_url="connexion")
def clotureCompte(request, id_compte) :
    try :
        compte = CompteBancaire.objects.get(id=id_compte,user = request.user )
        compte.est_actif = False
        compte.save()
        return redirect("home")
    except compte.DoesNotExist:
        return redirect("list_comptes")

@login_required(login_url="connexion")
def Transaction(request) :
    compte = ""
    message_nulle = ""
    message_depot = ""
    message_retrait =""
    user_comptes = CompteBancaire.objects.filter(user=request.user)
    
    if request.method == "POST":
        compte_id = request.POST.get("compte_id")
        type_transaction = request.POST.get("type_transaction")
        montant = request.POST.get("montant")
        code_pin = request.POST.get("code_pin")
        description =  request.POST.get("description", '')
       
        try :
            montant = Decimal(montant)
            compte = CompteBancaire.objects.get(id=compte_id, user=request.user, code_pin=code_pin)
            if type_transaction == "depot" :
                
                if montant < compte.solde :
                    if code_pin != compte.code_pin :
                        message_code_pin = "code pin incorrect !"
                        return render(request, "shop/transaction.html", context={"message_code_pin":message_code_pin})
                        
                    else :
                        
                            compte.solde += montant
                            compte.save()
                            TransactionClient.objects.create(compte=compte, 
                                                            type_transaction = type_transaction, 
                                                            montant = montant, 
                                                            description =description,
                                                            statut = "completee"
                                                                )
                            return redirect("home")
                        
                else :
                    message_depot = "le montant saisi est supérieur à 1000 USD ! "
                    return render(request, "shop/transaction.html", context={"message_depot":message_depot})
            elif type_transaction == "retrait" :
                compte = CompteBancaire.objects.get(id=compte_id, user=request.user)
                if montant < compte.solde :
                    compte.solde -= montant
                    compte.save()
                    TransactionClient.objects.create(compte=compte,
                                                      type_transaction = type_transaction,
                                                        montant = montant, 
                                                        description =description,
                                                         statut = "completee" 
                                                         )
                    return redirect("home")
                else :
                    message_retrait = "le montant saisi est supérieur à 1000 USD"
                    return render(request, "shop/transaction.html", context={"message_retrait":message_retrait})
        except CompteBancaire.DoesNotExist :
            message_compte = "Problème de compte  ! ou le code pin inccorect ! "
            return render(request, "shop/transaction.html", context={"message_compte": message_compte})


    return render(request, "shop/transaction.html", context={"user_comptes":user_comptes})
# fonction pour afficher l'historique du type DEPOT ET RETRAIT 
@login_required(login_url='connexion')
def historique_transaction(request):
    # je recupere tous les comptes bancaires de user connecté
    comptes = CompteBancaire.objects.filter(user=request.user)
    # j'initialise un dictionnaire qui stockera les transactions par compte de user
    transaction_par_compte = {}
    for compte in comptes :
         # je recupere toutes les transactions du compte bancaire de user connecté
        transaction = TransactionClient.objects.filter(compte=compte).order_by("date_heure")
        transaction_par_compte[compte] = transaction
        context = {
            "compte" : compte,
            'transaction_par_compte' : transaction_par_compte,
        }
        return render(request, 'shop/historique.html', context)
    
# fonction pour transfer les comptes bancaires d'un seul user qui est connecté
@login_required(login_url="connexion")
def Transfert_Interne(request):
    user_comptes = CompteBancaire.objects.filter(user = request.user)
    
    if request.method == "POST" :
        compte_source_id = request.POST.get("compte_source_id")
        compte_destination = request.POST.get("compte_destination_id")
        montant = request.POST.get("montant")
        description = request.POST.get("description")
        try :
            compte_source = CompteBancaire.objects.get(id=compte_source_id, user=request.user)
            compte_destination = CompteBancaire.objects.get(id=compte_destination)
            montant = Decimal(montant)
            if compte_source != compte_destination :
                if montant <= compte_source.solde :
                    compte_source.solde -= montant
                    compte_destination.solde += montant
                    compte_source.save()
                    compte_destination.save()
                    TransfertInterne.objects.create(
                        compte_source = compte_source,
                        compte_destination = compte_destination,
                        montant = montant,
                        description = description,
                        statut = "completee"
                    )
                    return redirect("home")
                else :
                    message_montant = f"le montant {montant} est supérieur à votre solde !"
                    
                    return render(request, "shop/Transfert_Interne.html", context={"message_montant":message_montant})

            else :
                    message = f"vous ne pouvez pas envoyer l'argent sur le meme compte !"
                    return render(request, "shop/Transfert_Interne.html", context={"message":message})
        except CompteBancaire.DoesNotExist:
            message_compteçbancaire = f"le compte est {compte_source} n'existe pas "
            return render(request, "shop/Transfert_Interne.html", context={"message_compteçbancaire":message_compteçbancaire})
            
    return render(request, "shop/Transfert_Interne.html", context={"user_comptes":user_comptes})

# cette fonction affiche les transactions du type DEPO ET RETRAIT de user connecté 
login_required(login_url="connexion")
def graphique(request):
    transactions = TransactionClient.objects.all()
    data = {"type_transaction" : [t.type_transaction for t in transactions],
            "montant " : [Decimal(m.montant) for m in transactions]}
    plt.figure(figsize=(10, 6)) # je designe la surface grace à matplotlib.pyplot
    sns.barplot(x="type_transaction", y=1, data=data) # je choisis le modele de graphique Barre grace à seaborn
    plt.title("Montant de transaction par type") # le titre de graphique 
    plt.xlabel('type de transaction') # le type sera en x
    plt.ylabel("montant") # montant en y


    buffer =   BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64decode(image_png).decode("utf-8")
    context = {"graphique" : image_base64}
    return render(request, "shop/graphique.html", context)
    


# fonction pour transferer l'argent entre users

login_required(login_url="connexion")
def transfert_entre_user(request) :
    e =""
    user_comptes = CompteBancaire.objects.filter(user=request.user)
    if request.method == 'POST' :
        compte_source_id = request.POST.get("compte_source_id")
        num_compte_destination = request.POST.get("num_compte_destination")
        montant = request.POST.get("montant")
        description = request.POST.get("description")
        code_pin = request.POST.get("code_pin")
        try :
            montant = Decimal(montant)
            source_compte = CompteBancaire.objects.get(id=compte_source_id, user=request.user)
            destination = CompteBancaire.objects.get(numero_compte=num_compte_destination)
            if destination.numero_compte == num_compte_destination :
                if montant < source_compte.solde :
                    if code_pin == source_compte.code_pin :
                        source_compte.solde -= montant
                        destination.solde+= montant
                        source_compte.save()
                        destination.save()
                        
                        TransfertExterne.objects.create(
                            compte_source = source_compte,
                            compte_destination = destination,
                            montant = montant,
                            devise = "USD",
                            description=description
                        )
                        return redirect("home")
                    else :
                        message_code_pin = "le code pin est incorrect !"
                        return render(request, "shop/transfert_entre_user.html", context={"message_code_pin":message_code_pin})
                else :
                    message_montant = "la transaction a échouée pour la raison : le solde de votre compte est insuffisant "
                    return render(request, "shop/transfert_entre_user.html", context={"message_montant":message_montant})
            else :
                message_numero_compte = "Aucun compte ne correspond à ce numero de compte !"
                return render(request, "shop/transfert_entre_user.html", context={"message_numero_compte":message_numero_compte})

        except  CompteBancaire.DoesNotExist as e:
            return render(request, "shop/transfert_entre_user.html", context={"e":e})
    return render(request, "shop/transfert_entre_user.html", context={"comptes":user_comptes})
# fonction pour consulter les comptes bancaires d'un user
login_required(login_url="connexion")
def consultation_compte_user(request) :
    user_comptes = CompteBancaire.objects.filter(user=request.user)
    return render(request, "shop/consultation_compte.html", context={"user_comptes":user_comptes})


login_required(login_url="connexion")
def historique_transfert_user(request):
     # je recupere tous les comptes bancaires de user connecté
    comptes = CompteBancaire.objects.filter(user=request.user)
    # j'initialise un dictionnaire qui stockera les transactions par compte de user
    transaction_par_compte = {}
    for compte in comptes :
         # je recupere toutes les transactions du compte bancaire de user connecté
        transaction = TransactionClient.objects.filter(compte=compte).order_by("date_heure")
        transaction_par_compte[compte] = transaction
        context = {
            "compte" : compte,
            'transaction_par_compte' : transaction_par_compte,
        }
    transferts = TransfertExterne.objects.filter(user=request.user)
    return render(request, "shop/historique_transfert_user.html", context={"transferts":transferts})

# fonction pour modifier le compte
"""
dans cette fonction, user ne peut que modifier 
son code pin, numero de telephone et le type de compte 
"""
@login_required(login_url='connexion')
def MofifierCompte(request, id) :
    compte = get_object_or_404(CompteBancaire, id=id)
    if request.method == "POST":
        change_code_pin = request.POST.get("code_pin")
        change_phone = request.POST.get("phone")
        change_type_compte = request.POST.get("types_compte")
        if change_code_pin is None or change_phone is None or change_type_compte is None :
            message = "tous les champs sont obligatoires !"
            return render(request, "shop/modificationCompte.html", context={"messages" : message})
        else :
            if len(change_code_pin) < 4 or len(change_code_pin) > 4 :
                message = "le copin doit avoir que 4 chiffres !"
                return render(request, "shop/modificationCompte.html", context={"messages" : message})
            elif any(char.isalpha() for char in change_code_pin) :
                message = "le code pin ne prend pas en charge les lettres !"
                return render(request, "shop/modificationCompte.html", context={"messages" : message})
            else :
                parsed_number = phonenumbers.parse(change_phone, None)
            print(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)
            if not is_possible :
                message = "le numero n'est pas posible"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            is_vali = phonenumbers.is_valid_number(parsed_number)
            if not is_vali:
                message = "le numero n'est pas valide"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            region = geocoder.region_code_for_number(parsed_number)
            if not region :
                message = "le numero n'a pas de region"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            localisation = geocoder.description_for_number(parsed_number, "fr")
            if not localisation:
                message = "le numero n'est pas localisable"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            number_type = phonenumbers.number_type(parsed_number)
            if not number_type :
                message = "le numero est faux"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            operator = carrier.name_for_number(parsed_number, 'fr')
            if not  operator:
                message = "nous n'avons pas trouver l'operateur"
                return render(request, "shop/creationCompteBancaire.html", context={"message":message})
            time_zone = timezone.time_zones_for_number(parsed_number)
            compte.phone = parsed_number
            compte.types_compte = change_type_compte
            compte.code_pin = change_code_pin
            compte.save()
            return redirect("home")
    return render(request, "shop/modificationCompte.html")

# fonction pour supprimer le compte bancaire
@login_required(login_url="connexion")
def supprimer_compte(request, id):
    compte = get_object_or_404(CompteBancaire, id=id)
    if request.method == "POST":
        oui = request.POST.get("oui")
        non = request.POST.get("non")
        if non:
            print(non)
            return redirect("consultation_compte_user")
        elif oui :
            return redirect("confirmationSuppression", id)
        elif oui and non :
            message = "nous devez nous envoyer qu'un seule infromation à la fois !"
            return render(request, "shop/suppressionCompte.html", context={"message":message})
        else :
            message = 'selectionner un champs '
            return render(request, "shop/suppressionCompte.html", context={"message":message})

    return render(request, "shop/suppressionCompte.html")
@login_required(login_url="connexion")
def confirmationSuppression(request, id) :
    compte = get_object_or_404(CompteBancaire, id=id)
    if request.method == "POST" :
        un = request.POST.get("un")
        deux = request.POST.get("deux")
        trois = request.POST.get("trois")
        quatre = request.POST.get("quatre")
        if un or deux or trois or quatre :
            return redirect('supprimer_ou_non', id)
    return render(request, "shop/supForm.html")
@login_required(login_url="connexion")
def supprimer_ou_non(request, id) :
    compte = get_object_or_404(CompteBancaire, id=id)
    if request.method == "POST":
        compte.delete()
        return redirect('home')
    return render(request, "shop/oui_non.html")