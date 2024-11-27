from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Importa el modelo de usuario activo
from .models import BoatModel, BoatInstance, BoatType, Port
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

        # Crear datos de prueba
        cls.boat_type = BoatType.objects.create(name="Velero", description="Un velero clásico")
        cls.port = Port.objects.create(name="Puerto Principal", address="123 Calle Marítima")

        # Archivo de imagen de prueba
        cls.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x01',  # Contenido binario de ejemplo
            content_type='image/jpeg'
        )

        # Crear modelo de barco con imagen
        cls.boat_model = BoatModel.objects.create(
            boat_type=cls.boat_type,
            name="Modelo X",
            capacity=8,
            brand="Marca Y",
            price_per_day=100.00,
            release_date=datetime.date(2020, 1, 1),
            image=cls.test_image
        )

        # Crear instancia de barco
        cls.boat_instance = BoatInstance.objects.create(
            model=cls.boat_model,
            name="Barco 1",
            port=cls.port,
            available=True,
        )

    def setUp(self):
        # Crear cliente para las pruebas
        self.client = Client()

    # Aquí seguirán los tests ya definidos en tu código


    def test_create_boat_instance_as_superuser(self):
        self.client.login(email='superadmin@test.com', password='superpassword')

        data = {
            'model': self.boat_model.id,
            'name': 'Barco 2',
            'port': self.port.id,
            'available': True,
            'price_per_day': 200.00,
        }
        response = self.client.post(reverse('crear_productos'), data)

        # Verifica redirección después de la creación
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('listar_productos'))

        # Verifica que la instancia fue creada
        self.assertEqual(BoatInstance.objects.count(), 2)
        new_instance = BoatInstance.objects.last()
        self.assertEqual(new_instance.name, 'Barco 2')

    def test_superuser_can_view_create_page(self):
        self.client.login(email='superadmin@test.com', password='superpassword')

        response = self.client.get(reverse('crear_productos'))

        # Verifica que la página de creación carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/create_boat_instance.html')

    def test_list_boats_as_superuser(self):
        self.client.login(email='superadmin@test.com', password='superpassword')

        response = self.client.get(reverse('listar_productos'))

        # Verifica que la lista de productos carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_instancias.html')

        # Verifica que el producto está en el contexto
        productos = response.context['productos']
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0], self.boat_instance)

    def test_list_models_as_superuser(self):
        self.client.login(email='superadmin@test.com', password='superpassword')

        response = self.client.get(reverse('listar_modelos'))

        # Verifica que la lista de modelos carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_modelos.html')

        # Verifica que el modelo está en el contexto
        modelos = response.context['modelos']
        self.assertEqual(len(modelos), 1)
        self.assertEqual(modelos[0], self.boat_model)
