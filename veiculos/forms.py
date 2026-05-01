from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from .models import (
    Veiculo, Motorista, UsoVeiculo, Abastecimento,
    Manutencao, Despesa, Documento, Ocorrencia, Alerta
)


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234',
                'maxlength': '10'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Onix'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Chevrolet'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': timezone.now().year + 1
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Prata'
            }),
            'chassi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'N do chassi'
            }),
            'renavam': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'N do RENAVAM'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'cnh': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'N da CNH'
            }),
            'validade_cnh': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class UsoVeiculoForm(forms.ModelForm):
    class Meta:
        model = UsoVeiculo
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_fim': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'km_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        exclude = ['valor_total']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'km': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.001'
            }),
            'litros': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'valor_litro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'tipo_combustivel': forms.Select(attrs={'class': 'form-select'}),
            'posto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do posto'
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do serviço...'
            }),
            'oficina': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da oficina'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'km_veiculo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'data_manutencao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_proxima': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'km_proxima': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['veiculo', 'tipo', 'descricao', 'valor', 'data', 'status', 'data_pagamento']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_pagamento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'data_emissao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_validade': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'documento_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local da ocorrência'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Mensagem do alerta...'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data_alerta': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class RegistroMotoristaForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário para login'
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha de acesso'
        })
    )
    password_confirm = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    )
    nome = forms.CharField(
        label="Nome Completo",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo'
        })
    )
    cnh = forms.CharField(
        label="CNH",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número da CNH'
        })
    )
    validade_cnh = forms.DateField(
        label="Validade da CNH",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    telefone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000'
        })
    )
    email = forms.EmailField(
        label="E-mail",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )

    def clean_username(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuário já existe.")
        return username

    def clean_cnh(self):
        cnh = self.cleaned_data.get('cnh')
        if cnh:
            from .models import Motorista
            if Motorista.objects.filter(cnh=cnh).exists():
                raise forms.ValidationError("Esta CNH já está cadastrada.")
        return cnh

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não conferem.")

        return cleaned_data
