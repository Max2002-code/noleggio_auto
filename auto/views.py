from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from .models import Auto, Prenotazione,Cliente
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def catalogo(request):

    print(request.user, request.user.is_authenticated)

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

@login_required
def prenota(request, id_auto):

    auto = get_object_or_404(
        Auto,
        id=id_auto
    )

    clienti = Cliente.objects.all()

    errore = None


    if request.method == "POST":

        cliente_id = request.POST["cliente"]

        cliente = get_object_or_404(
            Cliente,
            id=cliente_id
        )


        ritiro = request.POST["ritiro"]
        riconsegna = request.POST["riconsegna"]


        occupata = Prenotazione.objects.filter(
            auto=auto,
            ritiro__lt=riconsegna,
            riconsegna__gt=ritiro
        ).exists()


        if occupata:

            errore = "Questa auto è già prenotata."

        else:

            Prenotazione.objects.create(
                cliente=cliente,
                auto=auto,
                ritiro=ritiro,
                riconsegna=riconsegna
            )

            return redirect("/")


    return render(
        request,
        "prenota.html",
        {
            "auto": auto,
            "clienti": clienti,
            "errore": errore
        }
    )

@login_required
def calendario(request):

    oggi = date.today()

    # calendario dei prossimi 365 giorni
    giorni = []

    for i in range(365):

        giorni.append(
            oggi + timedelta(days=i)
        )


    auto = Auto.objects.all()


    calendario = []


    for macchina in auto:


        giorni_auto = []


        for giorno in giorni:


            prenotazioni = Prenotazione.objects.filter(

                auto=macchina,

                ritiro__date__lte=giorno,

                riconsegna__date__gte=giorno

            ).order_by(
                "ritiro"
            )


            fasce = []


            for prenotazione in prenotazioni:


                fasce.append({

                    "id":
                    prenotazione.id,


                    "ritiro":
                    prenotazione.ritiro.strftime(
                        "%d/%m/%Y %H:%M"
                    ),


                    "riconsegna":
                    prenotazione.riconsegna.strftime(
                        "%d/%m/%Y %H:%M"
                    ),


                    "cliente":
                        prenotazione.cliente.nome + " " + prenotazione.cliente.cognome,


                    "telefono":
                    prenotazione.cliente.telefono,


                    "email":
                    prenotazione.cliente.email,


                    "patente":
                    prenotazione.cliente.patente,


                    "documento":
                    prenotazione.cliente.documento

                })



            giorni_auto.append({

                "giorno":
                giorno,


                "fasce":
                fasce

            })



        calendario.append({

            "auto":
            macchina,


            "giorni":
            giorni_auto

        })



    return render(

        request,

        "calendario.html",

        {

            "giorni":
            giorni,


            "calendario":
            calendario

        }

    )

@login_required
def api_calendario(request):

    prenotazioni = Prenotazione.objects.all()

    eventi = []


    for p in prenotazioni:

        eventi.append({

            "title":
            f"🚗 {p.auto.marca} {p.auto.modello} - {p.cliente.nome} {p.cliente.cognome}",


            "start":
            p.ritiro.isoformat(),


            "end":
            p.riconsegna.isoformat(),


            "color":
            "#dc3545",


            "extendedProps": {

                "auto":
                f"{p.auto.marca} {p.auto.modello}",


                "cliente":
                f"{p.cliente.nome} {p.cliente.cognome}",


                "telefono":
                p.cliente.telefono,


                "email":
                p.cliente.email,


                "patente":
                p.cliente.patente,


                "documento":
                p.cliente.documento

            }

        })


    return JsonResponse(
        eventi,
        safe=False
    )