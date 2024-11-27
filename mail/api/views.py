from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_user_mail(user):
    """
    Envía un correo electrónico a un usuario.
    :param user: Objeto de usuario con los campos `email` y cualquier dato necesario para la plantilla.
    """
    subject = 'Bienvenido a SafePort'
    template = get_template('send_mail.html')  # Asegúrate que esta ruta sea correcta
    content = template.render({
        'user': user,  # Datos del usuario para renderizar la plantilla
    })

    # Configuración del correo
    message = EmailMultiAlternatives(
        subject,  # Asunto del correo
        '',  # Cuerpo del texto plano (opcional)
        settings.EMAIL_HOST_USER,  # Remitente
        [user.email]  # Destinatarios
    )

    # Adjuntar contenido HTML
    message.attach_alternative(content, 'text/html')
    message.send()
