from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Veiculo, Motorista, UsoVeiculo, Abastecimento,
    Manutencao, Despesa, Documento, Ocorrencia, Alerta
)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'marca', 'tipo', 'ano', 'status', 'criado_em')
    list_filter = ('status', 'tipo', 'marca', 'ano')
    search_fields = ('placa', 'modelo', 'marca', 'chassi', 'renavam')
    list_editable = ('status',)
    ordering = ('-criado_em',)
    readonly_fields = ('criado_em', 'atualizado_em', 'imagem_thumbnail')
    fieldsets = (
        ('Dados Principais', {
            'fields': ('placa', 'modelo', 'marca', 'ano', 'tipo', 'cor')
        }),
        ('Identificacao', {
            'fields': ('chassi', 'renavam', 'observacoes')
        }),
        ('Multimedia', {
            'fields': ('imagem', 'imagem_thumbnail')
        }),
        ('Status', {
            'fields': ('status', 'criado_em', 'atualizado_em')
        }),
    )

    def status_badge(self, obj):
        cores = {'ativo': '#28a745', 'manutencao': '#ffc107', 'inativo': '#dc3545'}
        return format_html(
            '<span style="color: white; padding: 4px 8px; border-radius: 4px; background: {};">{}</span>',
            cores.get(obj.status, '#6c757d'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def imagem_thumbnail(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 4px;">', obj.imagem.url)
        return '-'
    imagem_thumbnail.short_description = 'Imagem'


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnh', 'telefone', 'email', 'ativo', 'validade_cnh', 'usuario', 'veiculo_padrao')
    list_filter = ('ativo', 'veiculo_padrao')
    search_fields = ('nome', 'cnh', 'telefone', 'email', 'usuario__username', 'veiculo_padrao__placa')
    list_editable = ('ativo',)
    ordering = ('nome',)
    readonly_fields = ('criado_em', 'atualizado_em')


@admin.register(UsoVeiculo)
class UsoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'motorista', 'data_inicio', 'data_fim', 'km_inicial', 'km_final', 'km_rodados')
    list_filter = ('veiculo', 'motorista')
    search_fields = ('veiculo__placa', 'motorista__nome')
    ordering = ('-data_inicio',)
    date_hierarchy = 'data_inicio'

    def km_rodados(self, obj):
        if obj.km_rodados:
            return f"{obj.km_rodados:,} km"
        return '-'
    km_rodados.short_description = 'Km Rodados'


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data', 'km', 'litros', 'valor_total', 'tipo_combustivel', 'posto')
    list_filter = ('tipo_combustivel', 'data')
    search_fields = ('veiculo__placa', 'posto')
    ordering = ('-data',)
    date_hierarchy = 'data'
    readonly_fields = ('valor_total', 'criado_em')


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'tipo', 'data_manutencao', 'valor', 'oficina', 'proxima')
    list_filter = ('tipo', 'data_manutencao')
    search_fields = ('veiculo__placa', 'oficina', 'descricao')
    ordering = ('-data_manutencao',)
    date_hierarchy = 'data_manutencao'

    def proxima(self, obj):
        if obj.data_proxima:
            dias = (obj.data_proxima - timezone.now().date()).days
            if dias < 0:
                return format_html('<span style="color: #dc3545;">{} atrasado</span>', obj.data_proxima)
            return obj.data_proxima
        return '-'
    proxima.short_description = 'Proxima Revisao'


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'tipo', 'valor', 'data', 'status', 'pago')
    list_filter = ('tipo', 'status', 'pago', 'data')
    search_fields = ('veiculo__placa', 'descricao')
    list_editable = ('status',)
    ordering = ('-data',)
    date_hierarchy = 'data'


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'tipo', 'numero', 'data_validade', 'status_valido')
    list_filter = ('tipo',)
    search_fields = ('veiculo__placa', 'numero')
    ordering = ('data_validade',)
    readonly_fields = ('status_valido',)

    def status_valido(self, obj):
        status = obj.status_validade
        if status == 'vencido':
            return format_html('<span style="color: #dc3545;">⚠ Vencido</span>')
        return format_html('<span style="color: #28a745;">✓ Válido</span>')
    status_valido.short_description = 'Status'


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'tipo', 'data', 'status_badge', 'valor')
    list_filter = ('tipo', 'status', 'data')
    search_fields = ('veiculo__placa', 'descricao', 'local')
    ordering = ('-data',)
    date_hierarchy = 'data'

    def status_badge(self, obj):
        cores = {'aberto': '#dc3545', 'em_andamento': '#ffc107', 'finalizado': '#28a745'}
        return format_html(
            '<span style="color: white; padding: 4px 8px; border-radius: 4px; background: {};">{}</span>',
            cores.get(obj.status, '#6c757d'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'mensagem', 'data_alerta', 'status_flag', 'veiculo')
    list_filter = ('tipo', 'status', 'data_alerta')
    search_fields = ('mensagem', 'veiculo__placa')
    ordering = ('data_alerta',)
    readonly_fields = ('criado_em',)

    def status_flag(self, obj):
        cores = {'pendente': '#ffc107', 'enviado': '#17a2b8', 'concluido': '#28a745'}
        return format_html(
            '<span style="color: white; padding: 4px 8px; border-radius: 4px; background: {};">{}</span>',
            cores.get(obj.status, '#6c757d'), obj.get_status_display()
        )
    status_flag.short_description = 'Status'
