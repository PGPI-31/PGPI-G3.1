from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User


class AuthenticationTests(TestCase):
    def setUp(self):
        # Cliente para las pruebas
        self.client = Client()

    def test_superuser_logout(self):
        """Verifica que un superusuario existente pueda cerrar sesión correctamente."""
        # Iniciar sesión primero
        self.client.login(email='ivan1@gmail.com', password='27112001')

        # Cerrar sesión
        response = self.client.get(reverse('logout'))

        # Verificar que la redirección después del logout es correcta
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_superuser_access_protected_view(self):
        """Verifica que un superusuario existente pueda acceder a vistas protegidas."""
        self.client.login(email='ivan1@gmail.com', password='27112001')

        # Reemplaza 'protected_view' con el nombre de una vista protegida en tu aplicación
        response = self.client.get(reverse('listar_productos'))  # Ejemplo de vista protegida

        # Verificar que la vista se carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_instancias.html')