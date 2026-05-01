from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from .models import (
    Veiculo, Motorista, UsoVeiculo, Abastecimento,
    Manutencao, Despesa, Documento, Ocorrencia, Alerta
)
from .forms import (
    AbastecimentoForm,
    AlertaForm,
    DespesaForm,
    DocumentoForm,
    ManutencaoForm,
    MotoristaForm,
    VeiculoForm,
)
from .services import (
    buscar_veiculos_para_select,
    get_abastecimento_context,
    get_alerta_context,
    get_dashboard_context,
    get_despesa_context,
    get_documento_context,
    get_kpis_payload,
    get_manutencao_context,
    get_relatorio_financeiro_context,
    get_relatorio_veiculos_queryset,
    get_veiculos_filtrados,
    paginate_queryset,
)
from .access import (
    admin_required,
    get_motorista_usuario,
    motorista_ou_admin_required,
    usuario_eh_admin,
    usuario_eh_motorista,
)


def _add_form_errors_to_messages(request, form):
    for field_name, errors in form.errors.items():
        label = form.fields.get(field_name).label if field_name in form.fields else field_name
        for error in errors:
            if field_name == "__all__":
                messages.error(request, error)
            else:
                messages.error(request, f'{label}: {error}')


def _veiculo_motorista_logado(request):
    motorista = get_motorista_usuario(request.user)
    return motorista.veiculo_padrao if motorista else None


# Dashboard Principal
@motorista_ou_admin_required
def dashboard(request):
    return render(request, 'veiculos/dashboard.html', get_dashboard_context())


# Lista de Veiculos
@admin_required
def veiculo_list(request):
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    busca = request.GET.get('busca')
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            veiculo = form.save()
            messages.success(request, f'Veículo {veiculo.placa} cadastrado!')
        else:
            _add_form_errors_to_messages(request, form)
        return redirect('veiculo_list')
    
    veiculos_list = get_veiculos_filtrados(status=status, tipo=tipo, busca=busca)
    page_obj = paginate_queryset(veiculos_list, request.GET.get('page'), 10)
    
    return render(request, 'veiculos/veiculo_list.html', {
        'page_obj': page_obj,
        'status_filter': status,
        'tipo_filter': tipo,
        'busca': busca,
        'is_admin_user': usuario_eh_admin(request.user),
    })


@motorista_ou_admin_required
def veiculo_detail(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    abastecimentos = veiculo.abastecimentos.all()[:5]
    manutencoes = veiculo.manutencoes.all()[:5]
    documentos = veiculo.documentos.all()[:5]
    ocorrencias = veiculo.ocorrencias.all()[:5]
    
    return render(request, 'veiculos/veiculo_detail.html', {
        'veiculo': veiculo,
        'abastecimentos': abastecimentos,
        'manutencoes': manutencoes,
        'documentos': documentos,
        'ocorrencias': ocorrencias,
    })


@require_http_methods(["POST"])
@admin_required
def veiculo_create(request):
    from .forms import VeiculoForm
    
    form = VeiculoForm(request.POST, request.FILES)
    if form.is_valid():
        veiculo = form.save()
        messages.success(request, f'Veículo {veiculo.placa} criado com sucesso!')
        return JsonResponse({'success': True, 'redirect': reverse_lazy('veiculo_detail', args=[veiculo.pk])})
    
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@require_http_methods(["POST"])
@admin_required
def veiculo_update(request, pk):
    from .forms import VeiculoForm
    
    veiculo = get_object_or_404(Veiculo, pk=pk)
    form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
    
    if form.is_valid():
        veiculo = form.save()
        messages.success(request, f'Veículo {veiculo.placa} atualizado!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@require_http_methods(["POST"])
@admin_required
def veiculo_delete(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.delete()
    messages.success(request, 'Veículo excluído!')
    return JsonResponse({'success': True})


@admin_required
def veiculo_upload_imagem(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST' and request.FILES.get('imagem'):
        veiculo.imagem = request.FILES['imagem']
        veiculo.save()
        messages.success(request, 'Foto atualizada!')
    
    return redirect('veiculo_detail', pk=pk)


# Motoristas
@admin_required
def motoristalist(request):
    motorist = Motorista.objects.all()
    form = MotoristaForm()
    
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motorista cadastrado!')
            return redirect('motorista_list')
        _add_form_errors_to_messages(request, form)
        return redirect('motorista_list')
    
    return render(request, 'veiculos/motorista_list.html', {
        'motoristas': motorist,
        'form': form
    })


@admin_required
def motoristadetail(request, pk):
    motorista_upload_foto = get_object_or_404(Motorista, pk=pk)
    usos = motorista_upload_foto.usos.all()
    return render(request, 'veiculos/motorista_detail.html', {'motorista': motorista_upload_foto, 'usos': usos})


@admin_required
def motorista_upload_foto(request, pk):
    motorist = get_object_or_404(Motorista, pk=pk)
    
    if request.method == 'POST' and request.FILES.get('foto'):
        motorist.foto = request.FILES['foto']
        motorist.save()
        messages.success(request, 'Foto atualizada!')
    
    return redirect('motorista_detail', pk=pk)


# Documentos
@admin_required
def documento_list(request):
    tipo = request.GET.get('tipo')
    veiculo_id = request.GET.get('veiculo')
    status_validade = request.GET.get('status_validade')
    context = get_documento_context(
        tipo=tipo,
        veiculo_id=veiculo_id,
        status_validade=status_validade,
        page_number=request.GET.get('page'),
    )
    context['form'] = DocumentoForm()
    context['veiculos'] = Veiculo.objects.filter(status='ativo')
    context['tipo_filter'] = tipo
    context['veiculo_filter'] = veiculo_id
    context['status_validade_filter'] = status_validade
    return render(request, 'veiculos/documento_list.html', context)


@require_http_methods(["POST"])
@admin_required
def documento_create(request):
    form = DocumentoForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Documento cadastrado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    else:
        _add_form_errors_to_messages(request, form)
    return redirect('documento_list')


# Despesas
@admin_required
def despesa_list(request):
    tipo = request.GET.get('tipo')
    veiculo_id = request.GET.get('veiculo')
    status = request.GET.get('status')
    if not status:
        pago = request.GET.get('pago')
        if pago in {'sim', 'pago', 'true', '1'}:
            status = 'pago'
        elif pago in {'nao', 'pendente', 'false', '0'}:
            status = 'pendente'
        elif pago == 'analise':
            status = 'analise'
    context = get_despesa_context(
        tipo=tipo,
        veiculo_id=veiculo_id,
        status=status,
        page_number=request.GET.get('page'),
    )
    context['form'] = DespesaForm()
    context['veiculos'] = Veiculo.objects.filter(status='ativo')
    context['tipo_filter'] = tipo
    context['veiculo_filter'] = veiculo_id
    context['status_filter'] = status
    return render(request, 'veiculos/despesa_list.html', context)


@require_http_methods(["POST"])
@admin_required
def despesa_create(request):
    form = DespesaForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Despesa cadastrada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    else:
        _add_form_errors_to_messages(request, form)
    return redirect('despesa_list')


# Alertas
@admin_required
def alerta_list(request):
    tipo = request.GET.get('tipo')
    veiculo_id = request.GET.get('veiculo')
    status = request.GET.get('status')
    context = get_alerta_context(
        tipo=tipo,
        veiculo_id=veiculo_id,
        status=status,
        page_number=request.GET.get('page'),
    )
    context['form'] = AlertaForm()
    context['veiculos'] = Veiculo.objects.filter(status='ativo')
    context['tipo_filter'] = tipo
    context['veiculo_filter'] = veiculo_id
    context['status_filter'] = status
    return render(request, 'veiculos/alerta_list.html', context)


@require_http_methods(["POST"])
@admin_required
def alerta_create(request):
    form = AlertaForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Alerta cadastrado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    else:
        _add_form_errors_to_messages(request, form)
    return redirect('alerta_list')


# Abastecimentos
@motorista_ou_admin_required
def abastecimento_list(request):
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')
    veiculo_id = request.GET.get('veiculo')
    context = get_abastecimento_context(
        mes=mes,
        ano=ano,
        veiculo_id=veiculo_id,
        page_number=request.GET.get('page'),
    )
    context['form'] = AbastecimentoForm()
    context['veiculos'] = Veiculo.objects.filter(status='ativo')
    context['can_create'] = True
    return render(request, 'veiculos/abastecimento_list.html', context)


@require_http_methods(["POST"])
@admin_required
def abastecimento_create(request):
    form = AbastecimentoForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Abastecimento cadastrado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    else:
        _add_form_errors_to_messages(request, form)
    return redirect('abastecimento_list')


# Manutencoes
@motorista_ou_admin_required
def manutencao_list(request):
    tipo = request.GET.get('tipo')
    veiculo_id = request.GET.get('veiculo')
    context = get_manutencao_context(
        tipo=tipo,
        veiculo_id=veiculo_id,
        page_number=request.GET.get('page'),
    )
    context['form'] = ManutencaoForm()
    context['veiculos'] = Veiculo.objects.filter(status='ativo')
    context['can_create'] = True
    return render(request, 'veiculos/manutencao_list.html', context)


@require_http_methods(["POST"])
@admin_required
def manutencao_create(request):
    form = ManutencaoForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Manutenção cadastrada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
    else:
        _add_form_errors_to_messages(request, form)
    return redirect('manutencao_list')


# Relatorios
@admin_required
def relatorio_financeiro(request):
    ano = request.GET.get('ano')
    return render(
        request,
        'veiculos/relatorio_financeiro.html',
        get_relatorio_financeiro_context(ano=ano),
    )


@admin_required
def relatorio_veiculos(request):
    veiculos = get_relatorio_veiculos_queryset()
    return render(request, 'veiculos/relatorio_veiculos.html', {'veiculos': veiculos})


# API HTMX
@require_http_methods(["GET"])
@admin_required
def api_busca_veiculo(request):
    termo = request.GET.get('q', '')
    return JsonResponse({'results': buscar_veiculos_para_select(termo)})


@require_http_methods(["GET"])
@admin_required
def api_kpis(request):
    return JsonResponse(get_kpis_payload())


# Cadastro de Motorista
from .forms import RegistroMotoristaForm


def cadastro_motorista(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroMotoristaForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            nome = form.cleaned_data['nome']
            cnh = form.cleaned_data['cnh']
            validade_cnh = form.cleaned_data.get('validade_cnh')
            telefone = form.cleaned_data.get('telefone')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(username=username, password=password)

            grupo_motorista, _ = Group.objects.get_or_create(name='Motorista')
            user.groups.add(grupo_motorista)

            Motorista.objects.create(
                nome=nome,
                cnh=cnh,
                validade_cnh=validade_cnh,
                telefone=telefone,
                email=email,
                usuario=user,
                ativo=True
            )

            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = RegistroMotoristaForm()

    return render(request, 'registration/cadastro_motorista.html', {'form': form})
