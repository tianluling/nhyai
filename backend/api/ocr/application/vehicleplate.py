"""
车牌
"""
from apphelper.image import union_rbox
import re
class vehicleplate:
    """
    车牌结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.license_type()
        self.license_no()
        self.full_name()
        self.address()
        self.birthday()
        self.first_issue()
        self.be_class()
        self.valid_period()


    def plate_no(self):
        """
        车牌号
        """
        plate_no={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                plate_no["车牌号"] = res[0].split('')[-1]
                self.res.update(plate_no) 
                break
            else:
                plate_no["车牌号"] = "其他"
                self.res.update(plate_no) 
                break
   