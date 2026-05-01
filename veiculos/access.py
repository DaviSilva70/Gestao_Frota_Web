from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django import forms
from django.urls import reverse

from .models import Motorista


def usuario_tem_perfil_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.is_staff or user.groups.filter(name__iexact="Administrador").exists() or user.groups.filter(
        name__iexact="Admin"
    ).exists()


def usuario_tem_perfil_motorista(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__iexact="Motorista").exists() or Motorista.objects.filter(usuario=user).exists()


def usuario_eh_admin(user):
    return usuario_tem_perfil_admin(user) and not usuario_tem_perfil_motorista(user)


def usuario_eh_motorista(user):
    return usuario_tem_perfil_motorista(user) and not usuario_tem_perfil_admin(user)


def get_motorista_usuario(user):
    if not user.is_authenticated:
        return None
    return Motorista.objects.select_related("veiculo_padrao").filter(usuario=user).first()


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped


def motorista_ou_admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped


class RoleAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Seu usuário",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Sua senha",
        }),
    )
    perfil = forms.ChoiceField(
        label="Entrar como",
        choices=(
            ("admin", "Administrador"),
            ("motorista", "Motorista"),
        ),
        widget=forms.RadioSelect(attrs={"class": "role-choice"}),
        initial="admin",
    )

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        perfil = cleaned_data.get("perfil")

        if perfil == "admin" and not (usuario_tem_perfil_admin(user) and not usuario_tem_perfil_motorista(user)):
            raise forms.ValidationError("Este usuário deve ser exclusivo do perfil de administrador.")

        if perfil == "motorista" and not (usuario_tem_perfil_motorista(user) and not usuario_tem_perfil_admin(user)):
            raise forms.ValidationError("Este usuário deve ser exclusivo do perfil de motorista.")

        return cleaned_data


class RoleLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = RoleAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if usuario_eh_motorista(self.request.user):
            motorista = get_motorista_usuario(self.request.user)
            if motorista and motorista.veiculo_padrao_id:
                return reverse("veiculo_detail", args=[motorista.veiculo_padrao_id])
            return reverse("abastecimento_list")
        return reverse("dashboard")
