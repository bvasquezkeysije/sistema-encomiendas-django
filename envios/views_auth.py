from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect, render


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, "Inicio de sesión correcto.")
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("login")


@login_required
def perfil_view(request):
    return render(request, "accounts/register.html", {"user": request.user})
