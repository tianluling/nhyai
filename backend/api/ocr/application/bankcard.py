"""
银行卡
"""
from apphelper.image import union_rbox
import re
from .banklist import banklist
class bankcard:
    """
    银行卡结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.bank_name()
        self.card_number()
        self.card_type()

    def bank_name(self):
        """
        银行名称
        """
        bank_name={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                for record in res:
                    bankName = banklist().get_bank_name(record)
                    if bankName is not None:
                        bank_name['银行名称']  = bankName
                        self.res.update(bank_name) 
                        break    

    def card_number(self):
        """
        卡号
        """
        card_number={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = txt
            if(txt.isnumeric() and len(txt)>15):
                card_number['卡号']  =txt
                self.res.update(card_number) 
                break    
   

    def card_type(self):
        """
        卡类型
        """
        card_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = txt
            if txt.isnumeric() and len(txt)==16:
                card_type['卡类型'] = '信用卡'
                self.res.update(card_type)
                break

            if txt.isnumeric() and len(txt) >16:
                card_type['卡类型'] = '借记卡'
                self.res.update(card_type)
                break

    