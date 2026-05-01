# Projeto: Gestão de Frota Web

## Stack Técnica

| Camada | Tecnologia |
|--------|------------|
| **Linguagem** | Python 3.13+ |
| **Framework** | Django 5.0.2 |
| **API** | Django REST Framework (instalado) |
| **Banco** | MySQL 8.x (`gestao_frota`) |
| **Relatórios** | Pandas 3.0+, Openpyxl 3.1.2, Reportlab 4.0.4 |
| **Frontend** | Bootstrap 5.3, HTMX, Select2, jQuery |
| **Tipografia** | Google Fonts `Manrope` |
| **Estilo** | CSS próprio em `static/css/app.css` |

---

## Arquitetura do Projeto

```
gestao_frota/
├── manage.py
├── requirements.txt
├── gestao_frota/
│   ├── settings.py          # Configurações globais
│   ├── urls.py              # Rotas raiz
│   ├── asgi.py
│   └── wsgi.py
├── veiculos/                # App principal (DOMÍNIO REAL)
│   ├── models.py            # 9 entidades ORM
│   ├── forms.py             # Validação de formulários
│   ├── views.py             # Lógica de apresentação
│   ├── urls.py              # Rotas do app
│   ├── services.py          # Queries e agregações
│   ├── access.py            # Autenticação/autorização
│   ├── admin.py             # Admin Django
│   ├── tests.py             # Testes automatizados
│   └── migrations/          # 5 migrações
├── combustivel/             # App scaffold (não utilizado)
├── manutencao/              # App scaffold (não utilizado)
├── financeiro/              # App scaffold (não utilizado)
├── templates/
│   ├── base.html
│   ├── registration/
│   │   ├── login.html
│   │   └── cadastro_motorista.html
│   └── veiculos/
├── static/css/app.css
└── media/
```

---

## Modelos de Dados (Entidades)

| Modelo | Descrição | Campos Principais |
|--------|-----------|-------------------|
| **Veiculo** | Cadastro de veículos | placa(unique), modelo, marca, ano, tipo, status |
| **Motorista** | Cadastro de motoristas | nome, cnh(unique), usuario(FK User), veiculo_padrao |
| **UsoVeiculo** | Controle de uso | veiculo, motorist, km_inicial, km_final |
| **Abastecimento** | Registro de combustíveis | veiculo, km(Decimal 3 casas), litros, valor_litro |
| **Manutencao** | Registro de manutenções | veiculo, tipo, valor, data_manutencao |
| **Despesa** | Despesas do veículo | veiculo, tipo, valor, status, pago |
| **Documento** | Documentos do veículo | veiculo, tipo, numero, data_validade |
| **Ocorrencia** | Ocorrências | veiculo, motorist, tipo, status |
| **Alerta** | Alertas programados | veiculo, mensagem, tipo, data_alerta |

---

## Sistema de Autenticação e Autorização

### Estrutura de Acesso (`veiculos/access.py`)

| Função | Descrição |
|--------|-----------|
| `usuario_tem_perfil_admin()` | Retorna True se admin (is_superuser/is_staff/grupo) |
| `usuario_tem_perfil_motorista()` | Retorna True se motorist (grupo + vínculo) |
| `@admin_required` | Decorator para rotas de admin |
| `@motorista_ou_admin_required` | Decorator para rotas compartilhadas |

### Fluxo de Login

1. **URL:** `/login/` → `RoleLoginView`
2. **Form:** `RoleAuthenticationForm` com seleção de perfil (Admin/Motorista)
3. **Sucesso Admin:** → Dashboard
4. **Sucesso Motorista:** → Abastecimentos ou Veículo padrão

### Cadastro de Motorista

- **URL:** `/cadastro/`
- **View:** `cadastro_motorista`
- **Form:** `RegistroMotoristaForm`
- **Fluxo:** Cria User → vincula ao grupo "Motorista" → cria Motorista → redireciona para login

---

## URLs do Sistema

| URL | View | Descrição |
|-----|------|-----------|
| `/` | dashboard | Dashboard principal |
| `/login/` | RoleLoginView | Login com seleção de perfil |
| `/logout/` | LogoutView | Logout |
| `/cadastro/` | cadastro_motorista | Cadastro de novo motorista |
| `/veiculos/` | veiculo_list | Lista/cadastra veículos |
| `/veiculos/<pk>/` | veiculo_detail | Detalhes do veículo |
| `/motoristas/` | motorista_list | Lista/cadastra motoristas |
| `/motoristas/<pk>/` | motoristadetail | Detalhes do motorista |
| `/abastecimentos/` | abastecimento_list | Lista/cadastra abastecimentos |
| `/manutencoes/` | manutencao_list | Lista/cadastra manutenções |
| `/despesas/` | despesa_list | Lista/cadastra despesas |
| `/documentos/` | documento_list | Lista/cadastra documentos |
| `/alertas/` | alerta_list | Lista/cadastra alertas |
| `/relatorios/financeiro/` | relatorio_financeiro | Relatório financeiro |
| `/relatorios/veiculos/` | relatorio_veiculos | Relatório por veículo |
| `/api/busca-veiculo/` | api_busca_veiculo | API HTMX para busca |
| `/api/kpis/` | api_kpis | API para KPIs |

---

## Modificações e Correções Aplicadas

### Autenticação e Acesso

- **Corrigido**: Sistema de login com validação de perfil (Admin/Motorista)
- **Corrigido**: View de cadastro de motorista (`/cadastro/`)
- **Corrigido**: Template de login com design profissional
- **Corrigido**: Link "Cadastre-se aqui" na tela de login
- **Corrigido**: Topbar mostra nome do motorista logado
- **Corrigido**: Formulário `RegistroMotoristaForm` com validação de CNH duplicada
- **Corrigido**: Grupo "Motorista" e "Administrador" criados no banco
- **Corrigido**: Admin vinculado ao grupo "Administrador"
- **Corrigido**: Removidas restrições de acesso - todos usuários autenticados acessam todas telas

### Banco de Dados

- **Corrigido**: Placa inválida `SHJ12J50` → `SHJ-1234`
- **Corrigido**: Campo `km` do `Abastecimento` alterado para Decimal com 3 casas decimais
- **Criada**: Migration `0005_alter_abastecimento_km`

### Interface (CSS/UI)

Melhorias globais no `static/css/app.css`:

- **Variáveis CSS**: Cores, transições, espaçamentos padronizados
- **Tipografia**: Antialiasing, estilos de títulos, selection
- **Animações**: Transições suaves (fast, normal, slow)
- **Cards**: Hover com escala e animação de pulse
- **Tabelas**: Hover com gradiente, transform translate
- **Formulários**: Estados hover/focus, shadows, placeholders estilizados
- **Botões**: Gradientes, hover com lift e shadow

### Correções de Código

- **Removido**: Restrições de PermissionDenied em views (todas abertas)
- **Simplificado**: Views de abastecimento e manutenção
- **Adicionado**: Validação de CNH no formulário de cadastro
- **Corrigido**: Uso de variáveis indefinidas em views

---

## Testes Automatizados

### Suíte atual: 21 testes

```bash
python manage.py test veiculos
```

### Testes de Modelo (5)

- `test_abastecimento_recalcula_valor_total_ao_salvar`
- `test_documento_status_validade_indica_vencido`
- `test_ocorrencia_usa_campo_criado_em`
- `test_uso_veiculo_calcula_km_rodados_quando_km_final_existe`
- `test_uso_veiculo_km_rodados_retorna_none_sem_km_final`

### Testes de View (16)

- Dashboard renderiza
- CRUD Veículos (create, list, filtro, create inválido)
- CRUD Motoristas (create, list, create inválido)
- CRUD Despesas (create, list, filtros)
- CRUD Documentos (create, list, post)
- CRUD Alertas (create, list)
- API busca_veiculo
- Login com validação de perfis

---

## Configurações Importantes

### Segurança

```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = False  # desenvolvimento
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

### Banco

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestao_frota',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Autenticação

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
AUTH_PASSWORD_VALIDATORS = [...]  # validators padrão Django
```

---

## Documentação Arquitetural (Reversa)

Artefatos gerados em `_reversa_sdd/`:

| Artefato | Descrição |
|----------|-----------|
| `architecture.md` | Visão geral arquitetural |
| `c4-context.md` | Diagrama C4 Contexto |
| `c4-containers.md` | Diagrama C4 Containers |
| `c4-components.md` | Diagrama C4 Componentes |
| `erd-complete.md` | ERD completo com cardinalidades |
| `traceability/spec-impact-matrix.md` | Matriz de impacto |

---

## Estado Atual do Projeto

| Item | Status |
|------|--------|
| Banco MySQL configurado | ✅ |
| Migrations aplicadas | ✅ (5 migrações) |
| Dashboard funcional | ✅ |
| CRUD Veículos | ✅ |
| CRUD Motoristas | ✅ |
| CRUD Abastecimentos | ✅ |
| CRUD Manutenções | ✅ |
| CRUD Despesas | ✅ |
| CRUD Documentos | ✅ |
| CRUD Alertas | ✅ |
| Relatórios | ✅ |
| Login com perfil | ✅ |
| Cadastro de Motorista | ✅ |
| Interface profissional | ✅ |
| Testes automatizados | ✅ (21 testes) |
| Documentação Reversa | ✅ |

---

## Próximos Passos Recomendados

1. Adicionar módulos de Ocorrências e UsoVeiculo
2. Criar API REST completa com DRF
3. Adicionar OpenAPI/Swagger
4. Ampliar testes覆盖率
5. Separar domínios em apps distintos (futuro)

---

## Observações Importantes

- **Monólito Django**: O domínio real está concentrado em `veiculos`
- **Apps scaffold**: `combustivel`, `manutencao`, `financeiro` existem mas não carregam lógica
- **Acesso**: Todos usuários autenticados podem acessar todas as telas
- **Testes**: Sempre executar `python manage.py test veiculos` antes de alterações significativas

---

## Agentes e Frameworks

- **Reversa**: Framework de engenharia reversa instalado (`.agents/skills/reversa/`)
- **Skills disponíveis**: reversa-scout, reversa-archaeologist, reversa-detective, reversa-architect, reversa-writer, reversa-reviewer, reversa-visor, reversa-data-master, reversa-design-system, reversa-reconstructor

---

*Última atualização: 01/05/2026*