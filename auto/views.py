from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from .models import Auto, Prenotazione
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def catalogo(request):

    auto = Auto.objects.all()

    ritiro = None
    riconsegna = None

    if request.method == "POST":
        ritiro = parse_datetime(
            request.POST["ritiro"]
        )

        riconsegna = parse_datetime(
            request.POST["riconsegna"]
        )


    lista_auto = []

    for macchina in auto:

        occupata = False

        if ritiro and riconsegna:

            occupata = Prenotazione.objects.filter(
                auto=macchina,
                ritiro__lt=riconsegna,
                riconsegna__gt=ritiro
            ).exists()


        lista_auto.append({
            "auto": macchina,
            "occupata": occupata
        })


    return render(
        request,
        "catalogo.html",
        {
            "auto": lista_auto
        }
    )

def prenota(request, id_auto):

    auto = get_object_or_404(
        Auto,
        id=id_auto
    )

    errore = None


    if request.method == "POST":

        nome = request.POST["nome"]
        cognome = request.POST["cognome"]
        email = request.POST["email"]
        telefono = request.POST["telefono"]
        patente = request.POST["patente"]
        documento = request.POST["documento"]

        ritiro = request.POST["ritiro"]
        riconsegna = request.POST["riconsegna"]


        occupata = Prenotazione.objects.filter(
            auto=auto,
            ritiro__lt=riconsegna,
            riconsegna__gt=ritiro
        ).exists()


        if occupata:

            errore = "Questa auto è già prenotata in queste date."


        else:

            Prenotazione.objects.create(

                nome=nome,
                cognome=cognome,
                email=email,
                telefono=telefono,
                patente=patente,
                documento=documento,

                auto=auto,

                ritiro=ritiro,
                riconsegna=riconsegna
            )

        send_mail(

    "Conferma prenotazione auto",

    f"""
Gentile {nome} {cognome},

la tua prenotazione è stata confermata.

AUTO:
{auto.marca} {auto.modello}

Ritiro:
{ritiro}

Riconsegna:
{riconsegna}


Grazie per aver scelto il nostro servizio.
""",

    "noreply@noleggioauto.it",

         [email],

)   

        return redirect("/")


    return render(
        request,
        "prenota.html",
        {
            "auto": auto,
            "errore": errore
        }
    )

@login_required
def calendario(request):

    oggi = date.today()

    giorni = []

    for i in range(30):
        giorni.append(
            oggi + timedelta(days=i)
        )


    auto = Auto.objects.all()


    calendario = []


    for macchina in auto:

        giorni_auto = []


        for giorno in giorni:


            prenotazione = Prenotazione.objects.filter(

                auto=macchina,

                ritiro__date__lte=giorno,

                riconsegna__date__gte=giorno

            ).first()



            giorni_auto.append({

                "giorno": giorno,

                "prenotazione": prenotazione

            })


        calendario.append({

            "auto": macchina,

            "giorni": giorni_auto

        })



    return render(

        request,

        "calendario.html",

        {

            "giorni": giorni,

            "calendario": calendario

        }

    )

def calendario_eventi(request):

    eventi = []

    prenotazioni = Prenotazione.objects.select_related(
        "auto"
    ).all()


    colori = {}


    for p in prenotazioni:

        if p.auto.id not in colori:
            colori[p.auto.id] = "#" + ("%06x" % (
                0x100000 + p.auto.id * 123456
            ))[1:]


        eventi.append({

            "title": (
                f"{p.auto.marca} {p.auto.modello}"
            ),

            "start": p.ritiro.isoformat(),

            "end": p.riconsegna.isoformat(),

            "backgroundColor":
                colori[p.auto.id],

            "borderColor":
                colori[p.auto.id],

            "extendedProps": {

                "cliente":
                    f"{p.nome} {p.cognome}",

                "telefono":
                    p.telefono,

                "email":
                    p.email,

                "patente":
                    p.patente,

                "documento":
                    p.documento

            }

        })


    return JsonResponse(
        eventi,
        safe=False
    )