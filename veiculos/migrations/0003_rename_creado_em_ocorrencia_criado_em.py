from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("veiculos", "0002_motorista_foto"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ocorrencia",
            old_name="creado_em",
            new_name="criado_em",
        ),
    ]
