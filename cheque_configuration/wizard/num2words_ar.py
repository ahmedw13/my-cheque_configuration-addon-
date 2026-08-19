# استرشاد من
# ASammour
# amsammour[at]gmail[dot]com

# Author: Ahmed El Gabalawy
# Ahmed.Gabalawy@gmail.com
# ويمكنك نشر، أو نسخ، أو إعادة توزيع الكود حتى للأغراض التجارية

import decimal

# القيم الخاصة بقيم الاحاد

ones = {
    1: "واحد",
    2: "اثنان",
    3: "ثلاثة",
    4: "أربعة",
    5: "خمسة",
    6: "ستة",
    7: "سبعة",
    8: "ثمانية",
    9: "تسعة",
    10: "عشرة",
    11: "أحد عشر",
    12: "اثنى عشر"
}

# القيم الخاصة بقيم العشرات

tens = {
    0: "",
    1: "عشر",
    2: "عشرون",
    3: "ثلاثون",
    4: "أربعون",
    5: "خمسون",
    6: "ستون",
    7: "سبعون",
    8: "ثمانون",
    9: "تسعون"
}


# القيم الخاصة بقيم المئات

hundreds = {
    0: "",
    1: "مائة",
    2: "مئتان",
    3: "ثلاثمائة",
    4: "أربعمائة",
    5: "خمسمائة",
    6: "ستمائة",
    7: "سبعمائة",
    8: "ثمانمائة",
    9: "تسعمائة"
}


# القيم الخاصة بقيم الآلاف

thousands = {
    1: "ألف",
    2: "ألفان",
    39: "آلاف",
    1199: "ألفًا"
}


# القيم الخاصة بقيم الملايين

millions = {
    1: "مليون",
    2: "مليونان",
    39: "ملايين",
    1199: "مليونًا"
}


# القيم الخاصة بقيم المليارات

billions = {
    1: "مليار",
    2: "ملياران",
    39: "مليارات",
    1199: "مليارًا"
}


# القيم الخاصة بقيم التريليونات

trillions = {
    1: "تريليون",
    2: "تريليونان",
    39: "تريليونات",
    1199: "تريليونًا"
}

def oneTen(number):
    #  القيم الافتراضية
    result :str 
#Karim Ahmed
    # من 0 إلى 12
    if int(number) <= 12:
        if int(number) == 0 :
            result = ''
        else :
            result = ones[int(number)]

    #   إذا كان العدد أكبر من12 وأقل من 99
    #   يقوم بجلب القيمة الأولى من العشرات
    #   والثانية من الآحاد
#Karim Ahmed
    else:
        if int(number[1]) == 0:
            result = tens[int(number[0])]
        elif int(number[0]) == 1:
            result = ones[int(number[1])] + ' ' + tens[int(number[0])]
        else:
            result = ones[int(number[1])] + ' و ' + tens[int(number[0])]

    return result

def hundred(number):
    result :str

#Karim Ahmed
    # تحديد قيمة الرقم الأول
    first = number[0]
    if first == '0' :
        result = oneTen(number[1:3])
    else:
        result = hundreds[int(first)]
        if len(oneTen(number[1:3])) == 0 :
            result = result + " " + oneTen(number[1:3])
        else:
            result = result + " و " + oneTen(number[1:3])
    # إضافة منزلة العشرات إلى الرقم المفقط
    # باستخدام دالة العشرات السابقة
    
    return result
#Karim Ahmed

def thousand(number):
    result :str
    if len(number) == 4:
        if number[0] == '1':
            result = thousands[1]
        elif number[0] == '2' :
            result = thousands[2]
        else:
            result = ones[int(number[0])] + ' ' + thousands[39]
        if int(number[1:4]) > 0 :
            result = result + ' و ' + hundred(number[1:])

    elif len(number) == 5:
        result = oneTen(number[0:2]) + ' ' + thousands[1199]
        if int(number[2:5]) > 0 :
            result = result + ' و ' + hundred(number[2:])

    elif len(number) == 6:
        result = hundred(number[0:3]) + ' ' + thousands[1199]
        if int(number[3:6]) > 0 :
            result = result + ' و ' + hundred(number[3:])
        
    return result

def million(number):
    result :str
    if len(number) == 7:
        if number[0] == '1':
            result = millions[1]
        elif number[0] == '2' :
            result = millions[2]
        else:
            result = ones[int(number[0])] + ' ' + millions[39]
        if int(number[1:]) > 0 :
            result = result + ' و ' + thousand(number[1:])

    elif len(number) == 8:
        result = oneTen(number[0:2]) + ' ' + millions[1199]
        if int(number[2:]) > 0 :
            result = result + ' و ' + thousand(number[2:])

    elif len(number) == 9:
        result = hundred(number[0:3]) + ' ' + millions[1199]
        if int(number[3:]) > 0 :
            result = result + ' و ' + thousand(number[3:])
        
    return result
    
def billion(number):
    result :str
    if len(number) == 10:
        if number[0] == '1':
            result = billions[1]
        elif number[0] == '2' :
            result = billions[2]
        else:
            result = ones[int(number[0])] + ' ' + billions[39]
        if int(number[1:]) > 0 :
            result = result + ' و ' + million(number[1:])

    elif len(number) == 11:
        result = oneTen(number[0:2]) + ' ' + billions[1199]
        if int(number[2:]) > 0 :
            result = result + ' و ' + million(number[2:])

    elif len(number) == 12:
        result = hundred(number[0:3]) + ' ' + billions[1199]
        if int(number[3:]) > 0 :
            result = result + ' و ' + million(number[3:])
        
    return result

def trillion(number):
    result :str
    if len(number) == 10:
        if number[0] == '1':
            result = trillions[1]
        elif number[0] == '2' :
            result = trillions[2]
        else:
            result = ones[int(number[0])] + ' ' + trillions[39]
        if int(number[1:]) > 0 :
            result = result + ' و ' + billion(number[1:])

    elif len(number) == 11:
        result = oneTen(number[0:2]) + ' ' + trillions[1199]
        if int(number[2:]) > 0 :
            result = result + ' و ' + billion(number[2:])

    elif len(number) == 12:
        result = hundred(number[0:3]) + ' ' + trillions[1199]
        if int(number[3:]) > 0 :
            result = result + ' و ' + billion(number[3:])
        
    return result

def udf_num2words_ar(value: decimal,main_unit:str,sub_unit:str):
    """           
    currency = {
        'EGP': ('جنيها','قرشا'),
        'SAR': ('ريال','هلله'),
        'AED': ('درهم','فلسا')
            }
            
        Convert number to arabic text \n
        Ex. tafkeet(123.24) -> فقط مائة و ثلاثة و عشرون جنيها و أربعة و عشرون قرشا
    """
    
    # extract fraction two decimal only
    frac_val = int(str(int(value * 100))[-2:])

        
    if frac_val > 0 :
        fraction = oneTen(str(frac_val))

    number = str(int(value))

    # متغير لتخزين النص المفقط بداخله
    result :str

    # التحقق من أن المتغير يحتوي أرقامًا فقط، وأقل من تسعة وتسعين تريليون
    if len(number) > 15:
        raise Exception('number is to big')

    # إذا كان العدد من 0 إلى 99
    if len(number) <= 2:
        result = oneTen(number)

    # كان العدد من 100 إلى 999
    elif len(number) == 3:
        result = hundred(number)

    # إذا كان العدد من 1000 إلى 999999
    # أي يشمل الآلاف وعشرات الألوف ومئات الألوف
    elif len(number) <= 6:
        result = thousand(number)

    elif len(number) <= 9:
        result = million(number)

    elif len(number) <= 12:
        result = billion(number)
    
    elif len(number) <= 15:
        result = trillion(number)


    if frac_val == 0 :
        return result + ' ' + main_unit
    else :
        return result + ' ' + main_unit + ' و ' + fraction + ' ' + sub_unit
    
    

