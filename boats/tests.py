from django.test import TestCase, Client
from django.urls import reverse
from .models import BoatModel, BoatInstance, BoatType, Port
from django.contrib.auth.models import User


class BoatManagementViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear superusuario como fixture
        cls.superuser = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='pgpi1234',
                telephone='1234567890',
                address='Admin Address',
                dni='12345678A',
                birthdate='2000-01-01',
        )

        # Crear datos de prueba (fixtures)
        cls.boat_type = BoatType.objects.create(name="Velero", description="Un velero clásico")
        cls.port = Port.objects.create(name="Puerto Principal", address="123 Calle Marítima")

        cls.boat_model = BoatModel.objects.create(
            boat_type=cls.boat_type,
            name="Modelo X",
            capacity=8,
            brand="Marca Y",
        )

        cls.boat_instance = BoatInstance.objects.create(
            model=cls.boat_model,
            name="Barco 1",
            port=cls.port,
            available=True,
            price_per_day=150.00,
        )

    def setUp(self):
        # Crear cliente para las pruebas
        self.client = Client()

    def test_create_boat_instance_as_superuser(self):
        """Verifica que el superusuario puede añadir datos a la base de datos."""
        self.client.login(username='admin', password='pgpi1234')

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
        """Verifica que el superusuario puede acceder a la página de creación."""
        self.client.login(username='admin', password='pgpi1234')

        response = self.client.get(reverse('crear_productos'))

        # Verifica que la página de creación carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_boat_instance.html')

    def test_list_boats_as_superuser(self):
        """Verifica que el superusuario puede listar los barcos disponibles."""
        self.client.login(username='admin', password='pgpi1234')

        response = self.client.get(reverse('listar_productos'))

        # Verifica que la lista de productos carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_instancias.html')

        # Verifica que el producto está en el contexto
        productos = response.context['productos']
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0], self.boat_instance)

    def test_list_models_as_superuser(self):
        """Verifica que el superusuario puede listar los modelos disponibles."""
        self.client.login(username='admin', password='pgpi1234')

        response = self.client.get(reverse('listar_modelos'))

        # Verifica que la lista de modelos carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_modelos.html')

        # Verifica que el modelo está en el contexto
        modelos = response.context['modelos']
        self.assertEqual(len(modelos), 1)
        self.assertEqual(modelos[0], self.boat_model)
