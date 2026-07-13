from django.contrib import admin
from .models import Auto, Prenotazione


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):

    list_display = (
        "marca",
        "modello",
        "anno",
        "targa",
    )



@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "cognome",
        "email",
        "auto",
        "ritiro",
        "riconsegna",
    )

    list_filter = (
        "auto",
        "ritiro",
    )