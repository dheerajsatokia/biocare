# Generated by Django 3.0.4 on 2020-03-25 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('PT', 'Patient'), ('DC', 'Doctor'), ('CH', 'Chemist'), ('LA', 'Lab Operator'), ('SA', 'Super Admin')], default='PT', max_length=2),
        ),
    ]
