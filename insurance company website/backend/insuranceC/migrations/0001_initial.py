# Generated by Django 4.1.4 on 2024-10-28 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('coverage_limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=200)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='posters/')),
            ],
        ),
        migrations.CreateModel(
            name='UserInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('payment_check', models.FileField(upload_to='payment_checks/')),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('verification_response', models.JSONField(blank=True, null=True)),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insuranceC.insurance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_insurances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
