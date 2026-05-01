from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Abastecimento, Alerta, Despesa, Documento, Motorista, Ocorrencia, UsoVeiculo, Veiculo


class VeiculoModelTests(TestCase):
    def setUp(self):
        self.veiculo = Veiculo.objects.create(
            placa="ABC1D23",
            modelo="Onix",
            marca="Chevrolet",
            status="ativo",
        )
        self.motorista = Motorista.objects.create(
            nome="Maria Silva",
            cnh="12345678901",
            ativo=True,
        )

    def test_uso_veiculo_calcula_km_rodados_quando_km_final_existe(self):
        uso = UsoVeiculo.objects.create(
            veiculo=self.veiculo,
            motorista=self.motorista,
            data_inicio=timezone.now().date(),
            km_inicial=1000,
            km_final=1250,
        )

        self.assertEqual(uso.km_rodados, 250)

    def test_uso_veiculo_km_rodados_retorna_none_sem_km_final(self):
        uso = UsoVeiculo.objects.create(
            veiculo=self.veiculo,
            motorista=self.motorista,
            data_inicio=timezone.now().date(),
            km_inicial=1000,
        )

        self.assertIsNone(uso.km_rodados)

    def test_abastecimento_recalcula_valor_total_ao_salvar(self):
        abastecimento = Abastecimento.objects.create(
            veiculo=self.veiculo,
            km=1000,
            litros=Decimal("40.00"),
            valor_litro=Decimal("5.50"),
            valor_total=Decimal("1.00"),
            tipo_combustivel="gasolina",
            data=timezone.now().date(),
        )

        self.assertEqual(abastecimento.valor_total, Decimal("220.00"))

    def test_documento_status_validade_indica_vencido(self):
        documento = Documento.objects.create(
            veiculo=self.veiculo,
            tipo="crlv",
            numero="DOC-1",
            data_validade=timezone.now().date() - timezone.timedelta(days=1),
        )

        self.assertEqual(documento.status_validade, "vencido")

    def test_ocorrencia_usa_campo_criado_em(self):
        ocorrencia = Ocorrencia.objects.create(
            veiculo=self.veiculo,
            motorista=self.motorista,
            tipo="acidente",
            data=timezone.now().date(),
            status="aberto",
        )

        self.assertIsNotNone(ocorrencia.criado_em)


class VeiculoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
        )
        self.client.force_login(self.admin_user)
        self.veiculo = Veiculo.objects.create(
            placa="XYZ9K88",
            modelo="Strada",
            marca="Fiat",
            status="ativo",
        )
        Veiculo.objects.create(
            placa="DEF4G56",
            modelo="Argo",
            marca="Fiat",
            status="manutencao",
        )
        self.documento = Documento.objects.create(
            veiculo=self.veiculo,
            tipo="crlv",
            numero="DOC-XYZ",
            data_validade=timezone.now().date() + timezone.timedelta(days=30),
        )
        self.despesa = Despesa.objects.create(
            veiculo=self.veiculo,
            tipo="seguro",
            valor=Decimal("350.00"),
            data=timezone.now().date(),
            status="pago",
        )
        self.alerta = Alerta.objects.create(
            veiculo=self.veiculo,
            mensagem="Seguro vence em breve",
            tipo="seguro",
            data_alerta=timezone.now().date(),
            status="pendente",
        )

    def test_api_busca_veiculo_retorna_vazio_com_termo_curto(self):
        response = self.client.get(reverse("api_busca_veiculo"), {"q": "x"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results": []})

    def test_api_busca_veiculo_retorna_resultados_com_termo_valido(self):
        response = self.client.get(reverse("api_busca_veiculo"), {"q": "XY"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], self.veiculo.id)
        self.assertIn(self.veiculo.placa, data["results"][0]["text"])

    def test_veiculo_list_filtra_por_status(self):
        response = self.client.get(reverse("veiculo_list"), {"status": "ativo"})

        self.assertEqual(response.status_code, 200)
        page_items = list(response.context["page_obj"])
        self.assertEqual(len(page_items), 1)
        self.assertEqual(page_items[0].placa, "XYZ9K88")

    def test_dashboard_renderiza_com_contexto_principal(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("total_veiculos", response.context)
        self.assertIn("veiculos_ativos", response.context)

    def test_veiculo_list_post_cria_veiculo_via_form(self):
        response = self.client.post(
            reverse("veiculo_list"),
            {
                "placa": "QWE1R23",
                "modelo": "HB20",
                "marca": "Hyundai",
                "ano": 2024,
                "tipo": "carro",
                "cor": "Prata",
                "chassi": "123456789",
                "status": "ativo",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Veiculo.objects.filter(placa="QWE1R23").exists())

    def test_veiculo_list_post_invalido_nao_cria_registro(self):
        total_antes = Veiculo.objects.count()

        response = self.client.post(
            reverse("veiculo_list"),
            {
                "placa": "XYZ9K88",
                "modelo": "Duplicado",
                "status": "ativo",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Veiculo.objects.count(), total_antes)

    def test_motorista_list_post_cria_motorista_via_form(self):
        response = self.client.post(
            reverse("motorista_list"),
            {
                "nome": "Carlos Souza",
                "cnh": "99887766554",
                "telefone": "11999999999",
                "email": "carlos@example.com",
                "ativo": "on",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Motorista.objects.filter(cnh="99887766554").exists())

    def test_motorista_list_post_invalido_nao_cria_registro(self):
        total_antes = Motorista.objects.count()
        Motorista.objects.create(nome="Base", cnh="11122233344", ativo=True)

        response = self.client.post(
            reverse("motorista_list"),
            {
                "nome": "Duplicado",
                "cnh": "11122233344",
                "ativo": "on",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Motorista.objects.count(), total_antes + 1)

    def test_documento_list_renderiza_com_filtros(self):
        response = self.client.get(reverse("documento_list"), {"tipo": "crlv"})

        self.assertEqual(response.status_code, 200)
        page_items = list(response.context["page_obj"])
        self.assertEqual(len(page_items), 1)
        self.assertEqual(page_items[0].numero, "DOC-XYZ")

    def test_documento_list_post_cria_documento(self):
        response = self.client.post(
            reverse("documento_create"),
            {
                "veiculo": self.veiculo.pk,
                "tipo": "seguro",
                "numero": "SEG-123",
                "data_validade": timezone.now().date() + timezone.timedelta(days=60),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Documento.objects.filter(numero="SEG-123").exists())

    def test_despesa_list_renderiza_com_filtros(self):
        response = self.client.get(reverse("despesa_list"), {"tipo": "seguro", "status": "pago"})

        self.assertEqual(response.status_code, 200)
        page_items = list(response.context["page_obj"])
        self.assertEqual(len(page_items), 1)
        self.assertEqual(page_items[0].tipo, "seguro")

    def test_despesa_create_cria_registro(self):
        response = self.client.post(
            reverse("despesa_create"),
            {
                "veiculo": self.veiculo.pk,
                "tipo": "ipva",
                "valor": "900.00",
                "data": timezone.now().date(),
                "status": "pago",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Despesa.objects.filter(tipo="ipva", valor="900.00", status="pago").exists())

    def test_motorista_veiculo_detail_liberado_apenas_para_veiculo_padrao(self):
        motorista_user = User.objects.create_user(username="motorista", password="motorista123")
        group, _ = Group.objects.get_or_create(name="Motorista")
        motorista_user.groups.add(group)
        motorista = Motorista.objects.create(
            nome="João Motorista",
            cnh="55667788990",
            ativo=True,
            usuario=motorista_user,
            veiculo_padrao=self.veiculo,
        )
        self.client.logout()
        self.client.force_login(motorista_user)

        response = self.client.get(reverse("veiculo_detail", args=[self.veiculo.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["veiculo"].pk, motorista.veiculo_padrao.pk)

    def test_login_rejeita_usuario_com_perfis_mistos(self):
        mixed_user = User.objects.create_superuser(
            username="misto",
            password="misto123",
            email="misto@example.com",
        )
        motorista_group, _ = Group.objects.get_or_create(name="Motorista")
        mixed_user.groups.add(motorista_group)
        Motorista.objects.create(
            nome="Usuário Misto",
            cnh="22334455667",
            ativo=True,
            usuario=mixed_user,
            veiculo_padrao=self.veiculo,
        )

        client = Client()
        response = client.post(
            reverse("login"),
            {
                "username": "misto",
                "password": "misto123",
                "perfil": "admin",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Este usuário deve ser exclusivo do perfil de administrador.",
        )

        response = client.post(
            reverse("login"),
            {
                "username": "misto",
                "password": "misto123",
                "perfil": "motorista",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Este usuário deve ser exclusivo do perfil de motorista.",
        )

    def test_alerta_list_renderiza_com_filtros(self):
        response = self.client.get(reverse("alerta_list"), {"status": "pendente"})

        self.assertEqual(response.status_code, 200)
        page_items = list(response.context["page_obj"])
        self.assertEqual(len(page_items), 1)
        self.assertEqual(page_items[0].mensagem, "Seguro vence em breve")

    def test_alerta_create_cria_registro(self):
        response = self.client.post(
            reverse("alerta_create"),
            {
                "veiculo": self.veiculo.pk,
                "mensagem": "IPVA em aberto",
                "tipo": "ipva",
                "data_alerta": timezone.now().date(),
                "status": "pendente",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Alerta.objects.filter(mensagem="IPVA em aberto").exists())
