from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from  .models import User
User = get_user_model()


# inscription
def inscription(request):
    if request.method == "POST" :
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if password == password_confirm :
            if not any(char.isdigit() for char in password) :
                message_number = "le mot de passe doit contenir au moins un chiffre !"
                return render(request, "accounts/inscription.html",context={"message_chiffre":message_number})
            elif len(password) < 6 :
                message_len = "le mot de passe doir avoir au moins 8 caractères !"
                return render(request, 'accounts/inscription.html', context={"message_len":message_len})
            elif not any(char.isalpha() for char in password) :
                message_letter = "le mot de passe doir contenir au moins une lettre !"
                return render(request, 'accounts/inscription.html', context={"message_letter":message_letter})
            elif User.objects.filter(email=email).exists() :
                message_email = "Cet Email existe déjà dans notre système ! connectez-vous"
                return render(request, 'accounts/inscription.html', context={"message_email":message_email})
            else :
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    email=email,
                    username=username,
                    password=password
                )
                if user :
                    login(request, user)
                    return redirect("connexion")
                else :
                    message_error = "désolé ! on a pas pu vous inscrire"
                    return render(request, "accounts/inscription.html", context={"message_error":message_error})
        else :
            message_password = "le mot de passe ne correspond pas !"
            return render(request, "accounts/inscription.html", context={"message_password":message_password})

    return render(request, "accounts/inscription.html")
# connexion user
def connexion(request) :
    if request.method == "POST" :
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user :
            login(request, user)
            return redirect("home") 
        else:
            message_error = "le mot de passe ou Nom d'utilisateur incorrect !"
            return render(request, "accounts/connexion.html", context={"message_error":message_error})    
    return render(request, "accounts/connexion.html")
    # deconnexion
def deconnexion(request) :
    request.user
    logout(request)
    return redirect("connexion")

    # verification de l'e-mail
def verificationEmail(request) :
    message = ""
    if request.method == 'POST':
            email = request.POST.get("email")
            if not email:
                  message = "veuillez rentrer une adresse valide "
                  return render(request, 'accounts/verificationEmail.html', {"message":message})
            
            if User.objects.filter(email=email).first :
                  return redirect("edit_mot_de_passe", email) # email sera accompagné a la page redirigée 
            else :
                  messageEmail = "cet email n'est pas reconnu dans notre système ! "
                  return render(request, 'accounts/verificationEmail.html', {"messageEmail":messageEmail})


    return render(request, 'accounts/verificationEmail.html')

# changement de mot de passe
def edit_mot_de_passe(request,email) :
    message = ""
    try :
          user = User.objects.get(email=email)
    except User.DoesNotExist:
          message = "l'utilisateur est introuvable "
          return redirect("connexion")
    
    if request.method == 'POST':
        password = request.POST.get("password")

        password_confirmation = request.POST.get("password_confirm")

        if password == password_confirmation:
              if len(password) < 6:  
                message_len = "le mot de passe doit avoir ua moins 6 caractères !"
                return render(request, "accounts/edit_password.html", context={"message_len":message_len})
              elif not any(char.isdigit() for char in password) :
                   message_digit = "le mot de passe doit avoir au moins un chiffre pour être valide !"
                   return render(request, "accounts/edit_password.html", context={"message_digit":message_digit})
              elif not any(char.isalpha() for char in password):
                    messaage_alpha = " le mot de passe doit avoir au moins une lettre !"
                    return render(request, "accounts/edit_password.html", context={"messaage_alpha":messaage_alpha})
              else :
                user.set_password(password) # changer le mot de passe 
                user.save()
                message = "mot de passe recuperé avec success "
                return redirect("connexion")
        else :
              message = "ne correspond pas "
    context = {"email":email,
               'message_not_edited':message}
    return render(request, 'accounts/edit_password.html', context)