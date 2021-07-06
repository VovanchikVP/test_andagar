from .models import Procedures
import json
import re


class DataPageAnalytic:
    """
    Формирует данные для страници аналитики в формате JSON
    """
    def __init__(self):
        self.queryset = Procedures.objects.all()
        self.data_procedures = self._dict_data()
        self._dict_curator_and_date()

    def _dict_data(self):
        """
        Возвращает словаль с данными о процедурах
        ключь id.
        :return:
        """
        return {i.id: i.data_to_dict() for i in self.queryset}

    def _dict_curator_and_date(self):
        """
        Возвращает словарь с данными о кураторах
        ключ id куратора заначение список список id процедур
        И данные о датах
        ключ дата значание список id процедур
        :return:
        """
        self.curator = {}
        self.date = {}
        self.curator_name = {}
        for i in self.data_procedures:
            curator = self.data_procedures[i]['curator']['id'] if self.data_procedures[i]['curator'] else None
            date = self.data_procedures[i]['data_doc_publish_date']
            if curator in self.curator:
                self.curator[curator].append(i)
            else:
                self.curator[curator] = [i]
            if curator not in self.curator_name:
                self.curator_name[curator] = self.data_procedures[i]['curator']['name'] if curator else None
            if date in self.date:
                self.date[date].append(i)
            else:
                self.date[date] = [i]

    def __call__(self):
        """
        Вызов класса как функции
        :return:
        """
        return json.dumps({'data_all': self.data_procedures, 'curator': self.curator, 'date': self.date,
                           'curator_name': self.curator_name})


class GetDateFile:
    """
    Обработка файлов XML
    """
    def __init__(self, file):
        self.file_data = str(file.read(), 'utf-8')
        self._root_element()
        self._data_element()
        self.add_data_db()

    def _root_element(self):
        r = re.compile(r'<([^(?xml)]\w+\b)', re.I | re.M)
        s = r.search(self.file_data)
        self.root_element = s.group(1)

    def _data_element(self):
        r_data = re.compile(r'<data.*?>(.*)</data>', re.I | re.M | re.S)
        s_data = r_data.search(self.file_data).group(1)
        r_purchaseNumber = re.compile(r'<.*?:purchaseNumber>(.*?)</.*?:purchaseNumber>', re.I | re.M | re.S)
        self.purchaseNumber = r_purchaseNumber.search(s_data).group(1)
        r_docPublishDate = re.compile(r'<.*?:docPublishDate>(.*?)</.*?:docPublishDate>', re.I | re.M | re.S)
        self.docPublishDate = r_docPublishDate.search(s_data).group(1)
        self._convert_date()
        r_purchaseObjectInfo = re.compile(r'<.*?:purchaseObjectInfo>(.*?)</.*?:purchaseObjectInfo>', re.I | re.M | re.S)
        self.purchaseObjectInfo = r_purchaseObjectInfo.search(s_data).group(1)
        r_responsibleOrg = re.compile(r'<.*?responsibleOrg>(.*)</.*?responsibleOrg>', re.I | re.M | re.S)
        s_responsibleOrg = r_responsibleOrg.search(s_data).group(1)
        r_responsibleOrg_regNum = re.compile(r'<.*?:regNum>(.*?)</.*?:regNum>', re.I | re.M | re.S)
        self.responsibleOrg_regNum = r_responsibleOrg_regNum.search(s_responsibleOrg).group(1)
        r_responsibleOrg_fullName = re.compile(r'<.*?:fullName>(.*?)</.*?:fullName>', re.I | re.M | re.S)
        self.responsibleOrg_fullName = r_responsibleOrg_fullName.search(s_responsibleOrg).group(1)
        r_lot = re.compile(r'<.*?:lot>(.*)</.*?:lot>', re.I | re.M | re.S)
        s_lot = r_lot.search(s_data).group(1)
        r_lot_maxPrice = re.compile(r'<.*?:maxPrice>(.*?)</.*?:maxPrice>', re.I | re.M | re.S)
        self.lot_maxPrice = r_lot_maxPrice.search(s_lot).group(1)

    def add_data_db(self):
        """
        Добавляет данные в базу даных
        :return:
        """
        procedure = Procedures(root_element=self.root_element, data_doc_publish_date=self.docPublishDate,
                               data_purchase_number=self.purchaseNumber,
                               data_purchase_object_info=self.purchaseObjectInfo,
                               responsible_org_full_name=self.responsibleOrg_fullName,
                               responsible_org_reg_num=self.responsibleOrg_regNum,
                               lot_max_price=self.lot_maxPrice)
        procedure.save()

    def _convert_date(self):
        r = re.compile(r'^([0-9]{4}-[0-1][0-9]-[0-3][0-9])')
        s = r.search(self.docPublishDate)
        self.docPublishDate = s.group(1)
