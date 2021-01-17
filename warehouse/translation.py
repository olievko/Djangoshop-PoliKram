from modeltranslation.translator import translator
from warehouse.models import Warehouse


translator.register(Warehouse, fields=['title', 'address'])