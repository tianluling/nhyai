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
        self.plate_no()


    def plate_no(self):
        """
        车牌号
        """
        plate_no={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$",txt)
            if len(res)>0:
                plate_no["车牌号"] = res[0]
                self.res.update(plate_no) 
                break

            if i == self.N-1 and len(res) <=0:
                plate_no["车牌号"] = "其他"
                self.res.update(plate_no) 
                break
   