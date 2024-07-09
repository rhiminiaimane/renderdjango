# ETL/models.py
from django.db import models

class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    local = models.BooleanField(default=False)
    machine = models.BooleanField(default=False)

    class Meta:
        db_table = "clients"  # Ensure this matches your actual table name

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Existing models...
class AchatModel(models.Model):
    num = models.BigIntegerField(primary_key=True)
    art_id = models.BigIntegerField()
    qte = models.BigIntegerField()
    date = models.DateField()  # Assuming 'YYYY-MM-DD' format

    class Meta:
        db_table = "achats"  # Ensure this matches your actual table name


class AriclesModel(models.Model):
    art_id = models.AutoField(primary_key=True)
    lib = models.CharField(max_length=100)
    pu = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "articles"  # Ensure this matches your actual table name


class VenteModel(models.Model):
    num = models.BigIntegerField(primary_key=True)
    art_id = models.BigIntegerField()
    qte = models.BigIntegerField()
    date = models.DateField()  # Assuming 'YYYY-MM-DD' format

    class Meta:
        db_table = "ventes"  # Ensure this matches your actual table name


class Bilan(models.Model):
    num = models.AutoField(primary_key=True)
    art_id = models.BigIntegerField()  # Assuming you want to keep a direct integer reference
    qte_actuelle = models.BigIntegerField()

    class Meta:
        db_table = 'Bilan'  # This is the name of the table in your database

    def __str__(self):
        return f"Bilan for Article ID {self.art_id}: Current Quantity - {self.qte_actuelle}"
