from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Importa el modelo de usuario activo
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class BoatManagementViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        # Crear superusuario
        cls.superuser = User.objects.create_superuser(
            email='superadmin@test.com',
            name='Super',
            surname='Admin',
            telephone='123456789',
            address='Superuser Address',
            dni='12345678A',
            birthdate='1980-01-01',
            password='superpassword'
        )

    def setUp(self):
        # Crear cliente para las pruebas
        self.client = Client()

    # Aquí seguirán los tests ya definidos en tu código


    def test_create_boat_instance_as_superuser(self):
        self.client.login(email='superadmin@test.com', password='superpassword')

        response = self.client.post(reverse('test_send_mail'))

        # Verifica redirección después de la creación
        self.assertEqual(response.status_code, 200)