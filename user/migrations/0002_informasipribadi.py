# Generated by Django 4.2.5 on 2023-10-09 01:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformasiPribadi',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('nama_informasi', models.CharField(max_length=255)),
                ('isi_informasi', models.CharField(max_length=255)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]