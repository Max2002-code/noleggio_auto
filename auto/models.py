from django.db import models


class Cliente(models.Model):

    nome = models.CharField(
        max_length=50
    )

    cognome = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        unique=True
    )

    telefono = models.CharField(
        max_length=30
    )

    patente = models.CharField(
        max_length=50
    )

    documento = models.CharField(
        max_length=100
    )

    creato_il = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.nome} {self.cognome}"



class Auto(models.Model):

    marca = models.CharField(
        max_length=50
    )

    modello = models.CharField(
        max_length=50
    )

    anno = models.IntegerField()

    targa = models.CharField(
        max_length=20,
        unique=True
    )

    immagine = models.ImageField(
        upload_to="auto/",
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.marca} {self.modello}"



class Prenotazione(models.Model):

    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.CASCADE
    )

    auto = models.ForeignKey(
        Auto,
        on_delete=models.CASCADE
    )

    ritiro = models.DateTimeField()

    riconsegna = models.DateTimeField()

    creata_il = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.cliente} - {self.auto}"