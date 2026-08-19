from odoo import fields, models, api,_
import math
from decimal import ROUND_HALF_UP, Decimal
from .num2words_ar import udf_num2words_ar
from num2words import num2words

def round_decimal(value):
    return value.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

def split_at_decimal(value):
    value=round_decimal(Decimal(value))
    
    integer, decimal = (int(i) for i in str(value).split(".")) 
    
    return integer, decimal
    
def udf_num2words(self,value,lang,main_unit,sub_unit,split_value,end_value):
    if value!=False and lang!=False and value>0:    
        result =""
        value=Decimal(value)
        
        if lang[:3].lower()=="ar_":
            value=round_decimal(value)
            
            result= udf_num2words_ar(value,main_unit,sub_unit)
        else:
            integer, decimal =split_at_decimal(value)
            
            result = num2words(integer, lang=lang) + " " + main_unit        
            
            split_value=" " + split_value

            if value % 1 != 0:
                result += split_value+  num2words(decimal, lang=lang) + " " + sub_unit

            result = result.replace("،", split_value)
            
        return result +" " + end_value
    else:
        return ''  

class inheritPdcWizard(models.Model):
    _inherit = "pdc.wizard"
    _description = "PDC Wizard add number2words"
    
    def num2words(self,value,lang,main_unit,sub_unit,split_value,end_value):
        return udf_num2words(self,value=value, lang=lang,
                            main_unit=main_unit,sub_unit=sub_unit,
                            split_value=split_value,end_value=end_value)
