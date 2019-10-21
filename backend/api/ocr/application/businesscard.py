"""
名片
"""
from apphelper.image import union_rbox
import re
from .positions import positionClass


class businesscard:
    """
    名片结构化识别
    """

    def __init__(self, result):
        self.result = union_rbox(result, 0.2)
        self.N = len(self.result)
        self.res = {}
        self.business_name()
        self.position()
        self.company()
        self.address()
        self.email()
        self.phone()
        self.telephone()
        self.qq()
        self.webchat()

    def business_name(self):
        """
        姓名
        """
        business_name = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("^([\u4E00-\u9FA5]+|[a-zA-Z]+)$",txt)
            if len(res) > 0:
                business_name['姓名'] = res[0]
                self.res.update(business_name)
                break

            if i == self.N-1 and len(res) <=0:
                business_name['姓名'] = '其他'
                self.res.update(business_name)
                break

    def position(self):
        """
        职位
        """
        position = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')  
            if positionClass().check_positionWords(txt):
                position['职位'] = txt
                self.res.update(position)
                break

    def company(self):
        """
        公司
        """
        company = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            if("公司" in txt):
                company['公司'] = txt
                self.res.update(company)
                break

    def address(self):
        """
        地址
        """
        address = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("地址[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['地址']  = res[0].replace('地址:','')
                self.res.update(address)
                break
                


    def email(self):
        """
        邮箱
        """
        email = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("邮箱[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['邮箱']  = res[0].replace('邮箱:','')
                self.res.update(address)
                break

    def phone(self):
        """
        手机
        """
        phone = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("手机[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['手机']  = res[0].replace('手机:','')
                self.res.update(address)
                break
    
    def telephone(self):
        """
        电话
        """
        telephone = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("电话[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['电话']  = res[0].replace('电话:','')
                self.res.update(address)
                break
    
    def qq(self):
        """
        QQ
        """
        qq = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("QQ[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['QQ']  = res[0].replace('QQ:','')
                self.res.update(address)
                break
    
    def webchat(self):
        """
        微信
        """
        webchat = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall("微信[\u4E00-\u9FA5A-Za-z0-9]+:",txt)
            if len(res)>0:
                address['微信']  = res[0].replace('微信:','')
                self.res.update(address)
                break
