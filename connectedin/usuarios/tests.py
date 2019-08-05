from django.test import TestCase
from django.urls import resolve
from usuarios.views import RegistrarUsuarioView
from django.http import HttpRequest


# Create your tests here.

class TesteCreateUsuario(TestCase):
    def teste_create(self):
        found = resolve('/registrar/')
        self.assertEqual(found.func, RegistrarUsuarioView.as_view())
