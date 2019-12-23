"""
行驶证
"""
from apphelper.image import union_rbox
import re
class drivinglicense:
    """
    驾驶证结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.license_type()
        self.license_no()
        self.full_name()
        self.nationality()
        self.address()
        self.birthday()
        self.issue_date()
        self.be_class()
        self.valid_period()

    def license_type(self):
        """
        类型 
        """
        license_type={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("中华人民共和国机动车驾驶证",txt)
            if len(res)>0:
                license_type['类型']  = '中华人民共和国机动车驾驶证'
                self.res.update(license_type)
                break  

            if i == self.N-1 and len(res) <=0:
                license_type['类型']  = '其他'
                self.res.update(license_type)
                break

    def license_no(self):
        """
        证号和性别判断
        """
        license_no={}

        # 身份证号码中倒数第二位为奇数是男性、偶数是女性
        sex={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall(r'证号\d*[X|x]',txt)
            res += re.findall(r'证号\d*',txt)
            res += re.findall(r'\d{16,18}',txt)
            if len(res)>0:
                number = res[0].replace('证号','')
                license_no['证号']  = number
                self.res.update(license_no)
                if (int(number[-2]) % 2) == 0:
                    sex['性别'] = '女'
                else:
                    sex['性别'] = '男'
                self.res.update(sex)
                break    
            res = re.findall(r'远号\d*[X|x]',txt)
            res += re.findall(r'远号\d*',txt)
            res += re.findall(r'\d{16,18}',txt)
            if len(res)>0:
                number = res[0].replace('远号','')
                license_no['证号']  = number
                self.res.update(license_no)
                if (int(number[-2]) % 2) == 0:
                    sex['性别'] = '女'
                else:
                    sex['性别'] = '男'
                self.res.update(sex)
                break    


    def full_name(self):
        """
        驾驶证姓名
        """
        name={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            ##匹配姓名
            res = re.findall("名[\u4e00-\u9fa5]{1,4}",txt)
            if len(res) == 0:
                res = re.findall("^务[\u4e00-\u9fa5]{1,3}",txt)

            if len(res)>0:
                if '别男' in res[0]:
                    name['姓名']  = res[0].replace('名','').replace('别男','')
                elif '务' in res[0]:
                    name['姓名']  = res[0].replace('务','')
                else:
                    name['姓名']  = res[0].replace('名','')
                self.res.update(name)
                break


    def nationality(self):
        """
        国籍
        """
        nationality={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            ##匹配国籍
            res = re.findall("国籍[\u4e00-\u9fa5]{1,4}",txt)
            if len(res) == 0:
                res = re.findall("^国[\u4e00-\u9fa5]{1,4}",txt)

            if len(res)>0:
                nationality['国籍']  =res[0][-2:]
                self.res.update(nationality)  
                break

            res = re.findall("Nationaliy.[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                nationality['国籍']  =res[0].replace('Nationaliy.','')
                self.res.update(nationality)  
                break

   
    def address(self):
        """
        住址
        ##此处地址匹配还需完善
        """
        add={}
        addString=[]
        address_cy = 0
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            
            ##增加判断第二行地址Y轴的偏移量不能大于50，否则视为第二行为空
            cy = self.result[i]['cy']

            ##住址
            if '址' in txt or '省' in txt or '市' in txt or '县' in txt or '街' in txt or '村' in txt or "镇" in txt or "区" in txt or "城" in txt or "室" in txt or "房" in txt or "号" in txt:
                res = re.findall("址[\u4e00-\u9fa5]+[0-9]+[\u4e00-\u9fa5]+",txt)
                if len(res) == 0:
                    res = re.findall("址[\u4e00-\u9fa5]+[0-9]+",txt)
                
                if len(res) == 0:
                    res = re.findall("址[\u4e00-\u9fa5]+",txt)

                if address_cy !=0  and cy - 50 < address_cy:
                    addString.append(txt.replace(' ',''))
                    break
                
                if address_cy !=0  and cy - 50 >address_cy:
                    break

                if len(res) > 0 and address_cy == 0:
                    addString.append(res[0].replace('址',''))
                    address_cy = cy        
            
        if len(addString)>0:
            add['住址']  =''.join(addString)
            self.res.update(add) 

    def birthday(self):
        """
        出生日期
        """
        birthday={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("出生日期[0-9\-]{1,10}",txt)
            if len(res)>0:
                birthday['出生日期']  =res[0].replace('出生日期','')
                self.res.update(birthday) 
                break
            res = re.findall("出生日加[0-9\-]{1,10}",txt)
            if len(res)>0:
                birthday['出生日期']  =res[0].replace('出生日加','')
                self.res.update(birthday) 
                break
    
    def issue_date(self):
        """
        初次领证日期
        """
        issue_date={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("次[\u4e00-\u9fa5]+[0-9\-]{1,10}",txt)
            if len(res)>0:
                res2 = re.findall("[0-9\-]{1,10}",res[0])
                if len(res2)>0:
                    issue_date['初次领证日期']  =res2[0]
                    self.res.update(issue_date) 
                    break
    
    def be_class(self):
        """
        准驾车型
        """
        be_class={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("准驾车型[AaBbcCDdEeFfMmNnPp]+",txt)
            if len(res)>0:
                be_class['准驾车型']  =res[0].replace('准驾车型','')
                self.res.update(be_class)
                break
    
    def valid_period(self):
        """
        有效起始日期
        有效截止日期
        """
        valid_period={}
        
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("[0-9\-]{1,10}至",txt)
            if len(res)>0:
                valid_period['有效起始日期']  =res[0].replace('有效起始日期','').replace('至','')
                self.res.update(valid_period) 
                # break    
            res = re.findall("至[0-9\-]{1,10}",txt)
            if len(res)>0:
                valid_period['有效截止日期']  =res[0].replace('至','')
                self.res.update(valid_period) 
                break    
                    