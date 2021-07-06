from django.db import models


class Curator(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True, null=True)

    def data_to_dict(self):
        """
        Возвращает словарь в котором ключь название поля
        :return:
        """
        return {'id': self.id, 'name': self.name}

    def __str__(self):
        return f'Пользователь: {self.name} (id{self.id})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Procedures(models.Model):
    root_element = models.CharField(max_length=100, blank=True, null=True)
    data_purchase_number = models.CharField(max_length=100, blank=True, null=True)
    data_doc_publish_date = models.DateField(blank=True, null=True)
    data_purchase_object_info = models.TextField(max_length=1000, blank=True, null=True)
    responsible_org_reg_num = models.CharField(max_length=100, blank=True, null=True)
    responsible_org_full_name = models.CharField(max_length=200, blank=True, null=True)
    lot_max_price = models.CharField(max_length=100, blank=True, null=True)
    curator = models.ForeignKey(Curator, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return f'Процедура: {self.root_element}'

    def data_to_dict(self):
        """
        Возвращает словарь в котором ключь название поля
        :return:
        """
        return {'id': self.id,
                'root_element': self.root_element,
                'data_purchase_number': self.data_purchase_number,
                'data_doc_publish_date': self.data_doc_publish_date.strftime('%Y-%m-%d'),
                'data_purchase_object_info': self.data_purchase_object_info,
                'responsible_org_reg_num': self.responsible_org_reg_num,
                'responsible_org_full_name': self.responsible_org_full_name,
                'lot_max_price': self.lot_max_price,
                'curator': self.curator.data_to_dict() if self.curator else None
                }

    class Meta:
        verbose_name = 'Процедура'
        verbose_name_plural = 'Процедуры'

