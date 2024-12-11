# Generated by Django 5.1.2 on 2024-12-09 05:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompteBancaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types_compte', models.CharField(max_length=30)),
                ('numero_compte', models.CharField(max_length=20, unique=True)),
                ('phone', models.CharField(max_length=13)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=20)),
                ('devise', models.CharField(default='USD', max_length=3)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_mise_a_jour', models.DateTimeField(auto_now=True)),
                ('code_pin', models.CharField(max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionClient',
            fields=[
                ('id_transaction', models.AutoField(primary_key=True, serialize=False)),
                ('type_transaction', models.CharField(choices=[('depot', 'Depôt'), ('retrait', 'Retrait')], max_length=30)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('devise', models.CharField(default='USD', max_length=3)),
                ('date_heure', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('statut', models.CharField(max_length=20, verbose_name=[('e_attente', 'En attente'), ('Completee', 'Complétée'), ('annulee', 'Annulée')])),
                ('compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.comptebancaire')),
            ],
        ),
        migrations.CreateModel(
            name='TransfertExterne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compte_destination', models.CharField(max_length=200)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=150)),
                ('devise', models.CharField(default='USD', max_length=3)),
                ('date_heure', models.DateTimeField(auto_now_add=True)),
                ('compte_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.comptebancaire')),
            ],
        ),
        migrations.CreateModel(
            name='TransfertInterne',
            fields=[
                ('id_transfert', models.AutoField(primary_key=True, serialize=False)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('devise', models.CharField(default='USD', max_length=3)),
                ('date_heure', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('statut', models.CharField(max_length=10)),
                ('compte_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfert_destination', to='shop.comptebancaire')),
                ('compte_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transafert_source', to='shop.comptebancaire')),
            ],
        ),
    ]
