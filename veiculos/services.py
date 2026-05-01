from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Abastecimento, Alerta, Despesa, Documento, Manutencao, Motorista, Veiculo


def get_dashboard_context():
    mes_atual = timezone.now().month
    ano_atual = timezone.now().year
    hoje = timezone.now().date()

    return {
        "total_veiculos": Veiculo.objects.count(),
        "veiculos_ativos": Veiculo.objects.filter(status="ativo").count(),
        "veiculos_manutencao": Veiculo.objects.filter(status="manutencao").count(),
        "total_motoristas": Motorista.objects.filter(ativo=True).count(),
        "gastos_mes": (
            Despesa.objects.filter(
                data__month=mes_atual,
                data__year=ano_atual,
                pago=True,
            ).aggregate(total=Sum("valor"))["total"]
            or 0
        ),
        "manutencoes_mes": (
            Manutencao.objects.filter(
                data_manutencao__month=mes_atual,
                data_manutencao__year=ano_atual,
            ).aggregate(total=Sum("valor"))["total"]
            or 0
        ),
        "alertas_pendentes": Alerta.objects.filter(
            data_alerta__lte=hoje,
            status="pendente",
        ).count(),
        "docs_vencidos": Documento.objects.filter(data_validade__lt=hoje).count(),
        "ultimos_veiculos": Veiculo.objects.order_by("-criado_em")[:5],
    }


def get_veiculos_filtrados(status=None, tipo=None, busca=None):
    queryset = Veiculo.objects.all()

    if status:
        queryset = queryset.filter(status=status)
    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if busca:
        queryset = queryset.filter(
            Q(placa__icontains=busca)
            | Q(modelo__icontains=busca)
            | Q(marca__icontains=busca)
        )

    return queryset


def paginate_queryset(queryset, page_number, per_page):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def get_abastecimentos_filtrados(mes=None, ano=None, veiculo_id=None):
    queryset = Abastecimento.objects.select_related("veiculo").all()

    if mes and ano:
        queryset = queryset.filter(data__month=int(mes), data__year=int(ano))
    elif veiculo_id:
        queryset = queryset.filter(veiculo_id=veiculo_id)

    return queryset


def get_abastecimento_context(mes=None, ano=None, veiculo_id=None, page_number=None):
    queryset = get_abastecimentos_filtrados(mes=mes, ano=ano, veiculo_id=veiculo_id)
    return {
        "page_obj": paginate_queryset(queryset, page_number, 15),
        "total_litros": queryset.aggregate(total=Sum("litros"))["total"] or 0,
        "total_valor": queryset.aggregate(total=Sum("valor_total"))["total"] or 0,
    }


def get_manutencoes_filtradas(tipo=None, veiculo_id=None):
    queryset = Manutencao.objects.select_related("veiculo").all()

    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if veiculo_id:
        queryset = queryset.filter(veiculo_id=veiculo_id)

    return queryset


def get_manutencao_context(tipo=None, veiculo_id=None, page_number=None):
    queryset = get_manutencoes_filtradas(tipo=tipo, veiculo_id=veiculo_id)
    return {
        "page_obj": paginate_queryset(queryset, page_number, 15),
        "total_gasto": queryset.aggregate(total=Sum("valor"))["total"] or 0,
    }


def get_documentos_filtrados(tipo=None, veiculo_id=None, status_validade=None):
    queryset = Documento.objects.select_related("veiculo").all()

    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if veiculo_id:
        queryset = queryset.filter(veiculo_id=veiculo_id)

    hoje = timezone.now().date()
    if status_validade == "vencido":
        queryset = queryset.filter(data_validade__lt=hoje)
    elif status_validade == "valido":
        queryset = queryset.filter(data_validade__gte=hoje)

    return queryset


def get_documento_context(tipo=None, veiculo_id=None, status_validade=None, page_number=None):
    queryset = get_documentos_filtrados(
        tipo=tipo,
        veiculo_id=veiculo_id,
        status_validade=status_validade,
    )
    hoje = timezone.now().date()
    return {
        "page_obj": paginate_queryset(queryset, page_number, 15),
        "documentos_vencidos": queryset.filter(data_validade__lt=hoje).count(),
        "documentos_validos": queryset.filter(data_validade__gte=hoje).count(),
    }


def get_despesas_filtradas(tipo=None, veiculo_id=None, status=None):
    queryset = Despesa.objects.select_related("veiculo").all()

    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if veiculo_id:
        queryset = queryset.filter(veiculo_id=veiculo_id)
    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_despesa_context(tipo=None, veiculo_id=None, status=None, page_number=None):
    queryset = get_despesas_filtradas(tipo=tipo, veiculo_id=veiculo_id, status=status)
    return {
        "page_obj": paginate_queryset(queryset, page_number, 15),
        "total_despesas": queryset.aggregate(total=Sum("valor"))["total"] or 0,
        "despesas_pagas": queryset.filter(status="pago").count(),
        "despesas_pendentes": queryset.filter(status="pendente").count(),
        "despesas_em_analise": queryset.filter(status="analise").count(),
    }


def get_alertas_filtrados(tipo=None, veiculo_id=None, status=None):
    queryset = Alerta.objects.select_related("veiculo").all()

    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if veiculo_id:
        queryset = queryset.filter(veiculo_id=veiculo_id)
    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_alerta_context(tipo=None, veiculo_id=None, status=None, page_number=None):
    queryset = get_alertas_filtrados(tipo=tipo, veiculo_id=veiculo_id, status=status)
    return {
        "page_obj": paginate_queryset(queryset, page_number, 15),
        "alertas_pendentes": queryset.filter(status="pendente").count(),
        "alertas_enviados": queryset.filter(status="enviado").count(),
        "alertas_concluidos": queryset.filter(status="concluido").count(),
    }


def get_relatorio_financeiro_context(ano=None):
    ano_referencia = ano or timezone.now().year
    despesas_mensais = (
        Despesa.objects.filter(data__year=ano_referencia)
        .annotate(mes=TruncMonth("data"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )
    manutencoes_mensais = (
        Manutencao.objects.filter(data_manutencao__year=ano_referencia)
        .annotate(mes=TruncMonth("data_manutencao"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )

    return {
        "despesas_mensais": list(despesas_mensais),
        "manutencoes_mensais": list(manutencoes_mensais),
        "ano": ano_referencia,
    }


def get_relatorio_veiculos_queryset():
    return Veiculo.objects.annotate(
        total_manutencoes=Count("manutencoes"),
        total_abastecimentos=Count("abastecimentos"),
        custo_manutencao=Sum("manutencoes__valor"),
        custo_abastecimento=Sum("abastecimentos__valor_total"),
    ).order_by("-custo_manutencao")


def buscar_veiculos_para_select(termo):
    if len(termo) < 2:
        return []

    queryset = Veiculo.objects.filter(
        Q(placa__icontains=termo) | Q(modelo__icontains=termo)
    )[:10]
    return [{"id": veiculo.id, "text": f"{veiculo.placa} - {veiculo.modelo}"} for veiculo in queryset]


def get_kpis_payload(ano=None):
    ano_referencia = ano or timezone.now().year
    custos_mensais = list(
        Manutencao.objects.filter(data_manutencao__year=ano_referencia)
        .annotate(mes=TruncMonth("data_manutencao"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )
    return {
        "custo_mensal": custos_mensais,
        "custo_total": sum(item["total"] or 0 for item in custos_mensais),
        "veiculos_ativos": Veiculo.objects.filter(status="ativo").count(),
    }
