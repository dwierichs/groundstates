# groundstates

Let's get this going!

# Wie geht dieses Django?

A.
Django installieren (via pip) - Apache und mod_wsgi benutzen wir noch nicht.

B.
1. repo clonen
2. ins repo navigieren und "python3 manage.py runserver" ausführen.
3. website im browser unter localhost:8000 aufrufen
4. hoffen, dass es geht :p
5. bei Bedarf mit deinem Vornamen und dem reponamen als pw einloggen 
   -> Adminbereich (PW bitte ändern)
   -> Models hinzufügen, wenn du experimentieren möchtest

C. 
Im code sind folgende  layer erst einmal interessant:
1. groundstates/core/models.py enthält die model Klassen; energy_models.py enthält die Subklassen wie besprochen
2. groundstates/core/views.py enthält die view Klassen, die die Logik hinter einer einzelnen Seite managen (z.B. HomeView für die Startseite)
3. groundstates/core/templates/core/ enthält die html templates, die mit Hilfe der views gerendered werden. Alle templates extenden das base.html template (weil wir das immer in jedes html reinschreiben, nicht automatisch)
4. groundstates/core/urls.py enthält die registrierten Seiten der Webpage und ihre urls. Hier werden die templates und die views mit der url gelinkt.
5. groundstates/groundstates/settings.py enthält allgemeinere Einstellungen, die erst einmal weniger relevant sein sollten. 

# 12.11.2019
Ich habe die besprochenen models implementiert und es gibt einen ersten HomeView (die Startseite sozusagen) und den SystemDetailView um später die Energie-Abfragen zu implementieren (Zeigt derzeit crap)

