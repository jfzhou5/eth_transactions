from django.db import models


# Create your models here.
class IPO(models.Model):
    stock_id = models.AutoField(max_length=6, verbose_name='股票ID', primary_key=True)
    company_name = models.CharField(max_length=20, null=False, verbose_name='公司名称')
    ipo_price = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='发行价格')
    ipo_count = models.IntegerField(verbose_name='发行数量')
    ipo_date = models.DateField(auto_now_add=True, null=True)
    content = models.TextField(verbose_name='募集资金的运用', default=' ')
    content2 = models.TextField(verbose_name='股权分配', default=' ')

    class Meta:
        db_table = 'IPO'
