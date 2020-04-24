# Generated by Django 2.0.6 on 2020-04-22 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20, verbose_name='公司名称')),
                ('stock_id', models.CharField(max_length=6, verbose_name='股票ID')),
                ('ipo_price', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='发行价格')),
                ('ipo_count', models.IntegerField(verbose_name='发行数量')),
                ('content', models.TextField(verbose_name='募集资金的运用')),
                ('content2', models.TextField(verbose_name='股权分配')),
            ],
            options={
                'db_table': 'IPO',
            },
        ),
    ]
