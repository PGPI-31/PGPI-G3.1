from django.http import HttpResponse, request
from django.contrib.auth.models import User
from mail.api.views import send_user_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login/')
def test_send_mail_view(request):
    # Example user
    user = User(username=request.user.username, first_name="Test", email=request.user.email)


    try:
        send_user_mail(user)
        return HttpResponse("Correo enviado exitosamente")
    except Exception as e:
        return HttpResponse(f"Error al enviar correo: {e}")