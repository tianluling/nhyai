"""
行驶证
"""
from apphelper.image import union_rbox
import re
class vehiclelicense:
    """
    驾驶证结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.license_type()
        self.plate_no()
        self.vehicle_type()
        self.owner()
        self.address()
        self.use_character()
        self.model()
        self.vin()
        self.engine_no()
        self.register_date()
        self.issue_date()

    def license_type(self):
        """
        类型 
        """
        license_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("中华人民共和国机动车行驶证",txt)
            if len(res)>0:
                license_type['类型']  ='中华人民共和国机动车行驶证'
                self.res.update(license_type)
                break 
            else:
                license_type['类型']  ='其他'
                self.res.update(license_type)
                break

    def plate_no(self):
        """
        号牌号码
        """
        plate_no={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("号牌号码[\u4E00-\u9FA5A-Za-z0-9]{1,7}",txt)
            if len(res)>0:
                plate_no['号牌号码']  = res[0].replace('号牌号码','')
                self.res.update(plate_no) 
            res = re.findall("号肿号码[\u4E00-\u9FA5A-Za-z0-9]{1,7}",txt)
            if len(res)>0:
                plate_no['号牌号码']  =res[0].replace('号肿号码','')
                self.res.update(plate_no) 
                break  

    def vehicle_type(self):
        """
        车辆类型
        """
        vehicle_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*车辆类型[\u4E00-\u9FA5]{1,4}",txt)
            if len(res)>0:
                #vehicle_type['车辆类型']  =res[0].replace('.*车辆类型','')
                vehicle_type["车辆类型"] = res[0].split('车辆类型')[-1]
                self.res.update(vehicle_type) 
                break  

    def owner(self):
        """
        所有人
        """
        owner={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("所有人[\u4E00-\u9FA5]{1,4}",txt)
            if len(res)>0:
                owner['所有人']  =res[0].replace('所有人','')
                self.res.update(owner) 
                break  

    def address(self):
        """
        住址
        """
        address={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("住址[\u4E00-\u9FA5\0-9]+",txt)
            if len(res)>0:
                address['住址']  =res[0].replace('住址','')
                self.res.update(address) 

            res = re.findall("主广址[\u4E00-\u9FA5\0-9]+",txt)
            if len(res)>0:
                address['住址']  =res[0].replace('主广址','')
                self.res.update(address) 
                break  

    def use_character(self):
        """
        使用性质
        """
        use_character={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("使用性质[\u4E00-\u9FA5]{1,3}",txt)
            if len(res)>0:
                use_character['使用性质']  =res[0].replace('使用性质','')
                self.res.update(use_character) 
                break  

    def model(self):
        """
        品牌型号
        """
        model={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*品牌型号[\u4E00-\u9FA5]+",txt)
            if len(res)>0:
                model["品牌型号"] = res[0].split('品牌型号')[-1]
                self.res.update(model) 
                break  

    def vin(self):
        """
        车辆识别代号
        """
        vin={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*车辆识别代号[A-Za-z0-9]+",txt)
            if len(res)>0:
                vin["车辆识别代号"] = res[0].split('车辆识别代号')[-1]
                self.res.update(vin) 
            res = re.findall(".*辆识别代号[A-Za-z0-9]+",txt)
            if len(res)>0:
                vin["车辆识别代号"] = res[0].split('辆识别代号')[-1]
                self.res.update(vin) 
                break  
    def engine_no(self):
        """
        发动机号码
        """
        engine_no={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*发动机号码[A-Za-z0-9]+",txt)
            if len(res)>0:
                engine_no["发动机号码"] = res[0].split('发动机号码')[-1]
                self.res.update(engine_no) 
                break  

    def register_date(self):
        """
        注册日期
        """
        register_date={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*注册日期[0-9\-]{1,10}",txt)
            if len(res)>0:
                register_date["注册日期"] = res[0].replace('.*注册日期','')
                self.res.update(register_date) 
                break  
            res = re.findall(".*注进日期[0-9\-]{1,10}",txt)
            if len(res)>0:
                register_date["注册日期"] = res[0].split('注进日期')[-1][0:9] 
                self.res.update(register_date) 
                break  

    def issue_date(self):
        """
        发证日期
        """
        issue_date={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(".*发证日期[0-9\-]{1,10}",txt)
            if len(res)>0:
                issue_date["发证日期"] = res[0].split('发证日期')[-1]
                self.res.update(issue_date) 
                break  

