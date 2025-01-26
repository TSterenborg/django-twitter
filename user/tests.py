from django.test import TestCase
from django.test import Client

from .models import CustomUser
from django.http.response import *

# Deze Classe test:
# - Of een gebruiker kan inloggen
# - Of een gebruiker kan registreren.
# - Of een gebruiker kan uitloggen.
class TestUsers(TestCase):

    c = Client()

    password = "adwwadadwadwadwadwadwdwdwdgegerytrhrtbfbWF231"

    
    def test_can_user_register(self):
        # Stuur een post request naar de register pagina met de correcte registeer informatie.
        response = self.c.post("/register", {"display_name": "Bob", "username": "bob2", "email": "bob@email.com", "password1": self.password, "password2": self.password})
        
        #Kijk of de registeer pagina ons accepteerd.
        self.assertEqual(response.status_code, 302)

        #Kijk of wij nu op de login pagina zitten (wat we moeten automatisch doorgestuurd worden).
        self.assertEqual(response.url, "/login")

        # Stuur een post request met foute informatie.
        incorrect_response = self.c.post("/register", {"display_name": "Bob", "username": "bob2", "email": "bob@email.com", "password1": "100fwguegwguewguyW0", "password2": "100fwguegwguewguyW0222"})
        
        #Kijk of de registeer pagina on weigerd.
        self.assertEqual(incorrect_response.status_code, 200)


    def test_can_user_log_in(self):
        # Stuur een nieuwe registreer request.
        self.c.post("/register", {"display_name": "Bob", "username": "bob2", "email": "bob@email.com", "password1": self.password, "password2": self.password})
        
        #NOTE: het maakt niet uit of de register 302 of 200 is omdat het alleen nodig is om de juiste info in de database te krijgen.
        #Stuur dan een login request met de juiste info.
        response = self.c.post("/login", {"email": "bob@email.com", "password": self.password})

        #Kijken of de status_code klopt en of we worden doorgestuurd naar de home pagina.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_can_user_log_out(self):
        # Stuur een nieuwe registreer request.
        self.c.post("/register", {"display_name": "Bob", "username": "bob2", "email": "bob@email.com", "password1": self.password, "password2": self.password})
        
        #NOTE: het maakt niet uit of de register 302 of 200 is omdat het alleen nodig is om de juiste info in de database te krijgen.
        #Stuur dan een login request met de juiste info.
        response = self.c.post("/login", {"email": "bob@email.com", "password": self.password})

        # Kijk of we nu op de home pagina zitten.
        self.assertEqual(response.url, "/")
        # Ga naar de logout view om uit te loggen.
        response = self.c.get("/logout")

        # Kijk of we doorgestuurd worden naar de login pagina.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login")
        self.assertEqual(type(response), HttpResponseRedirect)