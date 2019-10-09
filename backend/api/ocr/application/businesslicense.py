"""
银行卡
"""
from apphelper.image import union_rbox
import re
from .banklist import banklist
class businesslicense:
    """
    营业执照
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.license_type()
        self.business_id()
        self.business_name()
        self.business_type()
        self.address()
        self.operator()
        self.registered_capital()
        self.register_date()
        self.business_term()
        self.scope()

    def license_type(self):
        """
        营业执照 
        """
        license_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("营业执照",txt)
            if len(res)>0:
                license_type['营业执照']  ='营业执照'
                self.res.update(license_type) 
                break
            else:
                license_type['营业执照']  ='其他'
                self.res.update(license_type)
                break 

    def business_id(self):
        """
        注册号/统一社会信用代码
        """
        business_id={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*统一社会信用代码[A-Za-z0-9]+",txt)
            if len(res)>0:
                business_id["统一社会信用代码"] = res[0].split('统一社会信用代码')[-1]
                self.res.update(business_id) 
                break  

    def business_name(self):
        """
        名称
        """
        business_name={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("名称[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                business_name['名称']  = res[0].replace('名称','')
                self.res.update(business_name) 
            res = re.findall("称[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                business_name['名称']  = res[0].replace('称','')
                self.res.update(business_name) 
                break  

    def business_type(self):
        """
        类型
        """
        business_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("类型[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                business_type['类型']  = res[0].replace('类型','')
                self.res.update(business_type) 
            res = re.findall("型[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                business_type['类型']  = res[0].replace('型','')
                self.res.update(business_type) 
                break  

    def address(self):
        """
        住所
        """
        address={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("住 所[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                address['住 所']  = res[0].replace('住 所','')
                self.res.update(address) 
            res = re.findall("样 所[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                address['住 所']  = res[0].replace('样 所','')
                self.res.update(address) 
                break  

    def operator(self):
        """
    法定代表人/经营者
        """
        operator={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("法定代表人[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                operator['法定代表人']  = res[0].replace('法定代表人','')
                self.res.update(operator) 
                break  

    def registered_capital(self):
        """
        注册资本
        """
        registered_capital={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("注册资本[\u4E00-\u9FA5.,A-Za-z0-9]+",txt)
            if len(res)>0:
                registered_capital['注册资本']  = res[0].replace('注册资本','')
                self.res.update(registered_capital) 
                break  

    def register_date(self):
        """
        成立日期
        """
        register_date={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')            
            res = re.findall("成立日期[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                register_date["成立日期"] = res[0].replace('成立日期','')
                self.res.update(register_date) 
                break

    def business_term(self):
        """
        营业期限
        """
        business_term={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("营业期限[\u4E00-\u9FA5A-Za-z0-9]+",txt)
            if len(res)>0:
                business_term["营业期限"] = res[0].replace('营业期限','')
                self.res.update(business_term) 
                break

    def scope(self):
        """
        经营范围
        """
        scope={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("经营范围[\u4E00-\u9FA5,、;:()【】A-Za-z0-9]+",txt)
            if len(res)>0:
                #scope["经营范围"] = res[0].split('经营范围')[-1]
                scope["经营范围"] = res[0].replace('经营范围','')
                self.res.update(scope) 
                break
   
    
    