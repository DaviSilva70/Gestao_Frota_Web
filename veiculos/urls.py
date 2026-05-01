from django.urls import path
from . import views

urlpatterns = [
    # Cadastro
    path('cadastro/', views.cadastro_motorista, name='cadastro_motorista'),
    
    path('', views.dashboard, name='dashboard'),
    
    # Veiculos
    path('veiculos/', views.veiculo_list, name='veiculo_list'),
    path('veiculos/<int:pk>/', views.veiculo_detail, name='veiculo_detail'),
    path('veiculos/criar/', views.veiculo_create, name='veiculo_create'),
    path('veiculos/<int:pk>/editar/', views.veiculo_update, name='veiculo_update'),
    path('veiculos/<int:pk>/upload/', views.veiculo_upload_imagem, name='veiculo_upload_imagem'),
    path('veiculos/<int:pk>/excluir/', views.veiculo_delete, name='veiculo_delete'),
    
    # Motoristas
    path('motoristas/', views.motoristalist, name='motorista_list'),
    path('motoristas/<int:pk>/', views.motoristadetail, name='motorista_detail'),
    path('motoristas/<int:pk>/upload/', views.motorista_upload_foto, name='motorista_upload_foto'),

    # Documentos
    path('documentos/', views.documento_list, name='documento_list'),
    path('documentos/criar/', views.documento_create, name='documento_create'),

    # Despesas
    path('despesas/', views.despesa_list, name='despesa_list'),
    path('despesas/criar/', views.despesa_create, name='despesa_create'),

    # Alertas
    path('alertas/', views.alerta_list, name='alerta_list'),
    path('alertas/criar/', views.alerta_create, name='alerta_create'),
    
    # Abastecimentos
    path('abastecimentos/', views.abastecimento_list, name='abastecimento_list'),
    path('abastecimentos/criar/', views.abastecimento_create, name='abastecimento_create'),
    
    # Manutencoes
    path('manutencoes/', views.manutencao_list, name='manutencao_list'),
    path('manutencoes/criar/', views.manutencao_create, name='manutencao_create'),
    
    # Relatorios
    path('relatorios/financeiro/', views.relatorio_financeiro, name='relatorio_financeiro'),
    path('relatorios/veiculos/', views.relatorio_veiculos, name='relatorio_veiculos'),
    
    # API HTMX
    path('api/busca-veiculo/', views.api_busca_veiculo, name='api_busca_veiculo'),
    path('api/kpis/', views.api_kpis, name='api_kpis'),
]
