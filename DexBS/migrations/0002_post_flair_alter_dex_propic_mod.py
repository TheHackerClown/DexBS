# Generated by Django 5.0.3 on 2024-03-26 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DexBS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dex',
            name='propic',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DexBS.dex')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DexBS.user')),
            ],
            options={
                'unique_together': {('user', 'dex')},
            },
        ),
    ]
