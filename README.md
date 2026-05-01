# 🚗 Gestão de Frota Web

Sistema web completo para gestão de frota de veículos com controle de combustível, manutenção, despesas e documentos.

---

## 📋 Índice

- [Stack Técnica](#stack-técnica)
- [Funcionalidades](#funcionalidades)
- [Modelos de Dados](#modelos-de-dados)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🛠 Stack Técnica

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3.13+ / Django 5.0.2 |
| **API** | Django REST Framework |
| **Banco** | MySQL 8.x |
| **Frontend** | Bootstrap 5.3, HTMX, jQuery, Select2 |
| **Relatórios** | Pandas, Openpyxl, Reportlab |
| **Estilo** | CSS customizado + Google Fonts Manrope |

---

## ✨ Funcionalidades

### Módulos Principais
- 📊 **Dashboard** - KPIs e resumões da frota
- 🚗 **Veículos** - Cadastro completo com foto, status e histórico
- 👤 **Motoristas** - Controle de CNH, vínculo com usuário
- ⛽ **Abastecimentos** - Registro de combustível com km (3 casas decimais)
- 🔧 **Manutenções** - Controle de preventivas e corretivas
- 💰 **Despesas** - IPVA, seguro, multas, pedágios
- 📄 **Documentos** - CRLV, seguro, licenciamento
- 🔔 **Alertas** - lembretes programados
- 📈 **Relatórios** - Financeiro e por veículo

### Autenticação e Autorização
- Login com seleção de perfil (Admin/Motorista)
- Cadastro de novos motoristas
- Controle de acesso por grupo

---

## 🗂 Modelos de Dados

```
Veiculo ───> Abastecimento
     └──> Manutencao
     └──> Despesa
     └──> Documento
     └──> Ocorrencia
     └──> Alerta
     └──> UsoVeiculo

Motorista ───> UsoVeiculo
         └──> Ocorrencia
         └──> Usuario (Django User)
```

---

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/DaviSilva70/Gestao_Frota_Web.git
cd Gestao_Frota_Web
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
Crie o banco MySQL:
```sql
CREATE DATABASE gestao_frota CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Edite `gestao_frota/settings.py` com suas credenciais:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestao_frota',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um usuário admin
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor
```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

---

## ⚙️ Configuração

### Variáveis de Ambiente (opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=gestao_frota
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### Upload de Arquivos
O diretório `media/` armazena imagens de veículos e motoristas. Em produção, configure um serviço de armazenamento (AWS S3, Google Cloud Storage, etc.).

---

## 🧪 Testes

Execute os testes automatizados:
```bash
python manage.py test veiculos
```

**Resultado:** 21 testes passando

### Cobertura de Testes
- ✅ Testes de Modelo (5)
- ✅ Testes de View (16)
- ✅ Validação de formulários
- ✅ API HTMX

---

## 📁 Estrutura do Projeto

```
gestao_frota/
├── manage.py
├── requirements.txt
├── gestao_frota/          # Configuração do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── veiculos/             # App principal
│   ├── models.py         # 9 entidades
│   ├── views.py          # Lógica de apresentação
│   ├── forms.py          # Validação
│   ├── services.py       # Queries
│   ├── access.py         # Autenticação
│   ├── urls.py           # Rotas
│   ├── admin.py          # Admin Django
│   └── tests.py          # Testes
├── templates/            # Templates HTML
├── static/css/           # CSS customizado
└── media/                # Uploads
```

---

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar super usuário
python manage.py createsuperuser

# executar testes
python manage.py test veiculos

# Verificar código
python manage.py check
```

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Desenvolvido por

**Davi Silva** - [GitHub](https://github.com/DaviSilva70)

---

*Última atualização: 01/05/2026*