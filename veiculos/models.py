from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings


class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('manutencao', 'Manutenção'),
        ('inativo', 'Inativo'),
    ]

    TIPO_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('caminhao', 'Caminhão'),
        ('van', 'Van'),
        ('outro', 'Outro'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, null=True)
    ano = models.IntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year + 1)]
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    chassi = models.CharField(max_length=50, blank=True, null=True)
    renavam = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['-criado_em']


class Motorista(models.Model):
    nome = models.CharField(max_length=150)
    cnh = models.CharField(max_length=20, unique=True)
    validade_cnh = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='perfil_motorista',
    )
    veiculo_padrao = models.ForeignKey(
        'Veiculo',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='motoristas_padrao',
    )
    foto = models.ImageField(upload_to='motoristas/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']


class UsoVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='usos')
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name='usos')
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    km_inicial = models.IntegerField(validators=[MinValueValidator(0)])
    km_final = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo} - {self.motorista}"

    @property
    def km_rodados(self):
        if self.km_final:
            return self.km_final - self.km_inicial
        return None

    class Meta:
        verbose_name = "Uso de Veículo"
        verbose_name_plural = "Uso de Veículos"
        ordering = ['-data_inicio']


class Abastecimento(models.Model):
    COMBUSTIVEL_CHOICES = [
        ('gasolina', 'Gasolina'),
        ('etanol', 'Etanol'),
        ('diesel', 'Diesel'),
        ('gnv', 'GNV'),
        ('eletrico', 'Elétrico'),
        ('flex', 'Flex'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='abastecimentos')
    km = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    litros = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valor_litro = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipo_combustivel = models.CharField(max_length=50, choices=COMBUSTIVEL_CHOICES)
    posto = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo} - {self.data}"

    def save(self, *args, **kwargs):
        self.valor_total = self.litros * self.valor_litro
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Abastecimento"
        verbose_name_plural = "Abastecimentos"
        ordering = ['-data']


class Manutencao(models.Model):
    TIPO_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('corretiva', 'Corretiva'),
        ('trocaoleo', 'Troca de Óleo'),
        ('freios', 'Freios'),
        ('pneus', 'Pneus'),
        ('revisao', 'Revisão'),
        ('outro', 'Outro'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='manutencoes')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    oficina = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    km_veiculo = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    data_manutencao = models.DateField()
    data_proxima = models.DateField(blank=True, null=True)
    km_proxima = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo} - {self.tipo}"

    class Meta:
        verbose_name = "Manutenção"
        verbose_name_plural = "Manutenções"
        ordering = ['-data_manutencao']


class Despesa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('analise', 'Em análise'),
        ('pago', 'Pago'),
    ]

    TIPO_CHOICES = [
        ('ipva', 'IPVA'),
        ('seguro', 'Seguro'),
        ('multa', 'Multa'),
        ('pedagio', 'Pedágio'),
        ('estacionamento', 'Estacionamento'),
        ('licenciamento', 'Licenciamento'),
        ('outro', 'Outro'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='despesas')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    data = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo} - {self.tipo} - R$ {self.valor}"

    def save(self, *args, **kwargs):
        if self.status == 'pago' or self.pago:
            self.status = 'pago'
            self.pago = True
        elif self.status == 'analise':
            self.pago = False
        else:
            self.status = 'pendente'
            self.pago = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ['-data']


class Documento(models.Model):
    TIPO_CHOICES = [
        ('crlv', 'CRLV'),
        ('seguro', 'Seguro Obrigatório'),
        ('ipva', 'IPVA'),
        ('licenciamento', 'Licenciamento Anual'),
        ('outro', 'Outro'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=100)
    data_emissao = models.DateField(blank=True, null=True)
    data_validade = models.DateField()
    documento_file = models.FileField(upload_to='documentos/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo} - {self.tipo} - {self.data_validade}"

    @property
    def status_validade(self):
        if self.data_validade < timezone.now().date():
            return 'vencido'
        return 'valido'

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['data_validade']


class Ocorrencia(models.Model):
    TIPO_CHOICES = [
        ('acidente', 'Acidente'),
        ('multa', 'Multa'),
        ('furto', 'Furto/Roubo'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='ocorrencias')
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=200, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    data = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} - {self.veiculo} - {self.status}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        ordering = ['-data']


class Alerta(models.Model):
    TIPO_CHOICES = [
        ('cnh', 'CNH Vencida'),
        ('ipva', 'IPVA Vencido'),
        ('seguro', 'Seguro Vencido'),
        ('manutencao', 'Manutenção Programada'),
        ('revisao', 'Revisão'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('concluido', 'Concluído'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, blank=True, null=True)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    data_alerta = models.DateField()
    enviado = models.BooleanField(default=False)
    data_envio = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.data_alerta}"

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ['data_alerta']
