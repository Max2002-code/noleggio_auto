from django.contrib import admin
from .models import Auto, Prenotazione, Cliente


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):

    list_display = (
        "marca",
        "modello",
        "anno",
        "targa",
    )



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "cognome",
        "email",
        "telefono",
    )



@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):

    list_display = (
        "cliente",
        "auto",
        "ritiro",
        "riconsegna",
    )