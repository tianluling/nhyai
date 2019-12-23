"""
created by: wangshujing
"""
import jpush

class mpush:
    def __init__(self, app_key, master_secret):
        self = self
        self.app_key = app_key
        self.master_secret = master_secret

        self._jpush = jpush.JPush(self.app_key, self.master_secret)
        self._jpush.set_logging("DEBUG")
    
    def send(self):
        push = self._jpush.create_push()
        push.audience = jpush.all_
        push.notification = jpush.notification(alert="!hello python jpush api")
        push.platform = jpush.all_
        try:
            response=push.send()
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn")
        except common.JPushFailure:
            print ("JPushFailure")
        except:
            print ("Exception")
        
    def alias(self):
        push = self._jpush.create_push()
        alias=["1"]
        alias1={"alias": alias}
        print(alias1)
        push.audience = jpush.audience(
            jpush.tag("tag1", "tag2"),
            alias1
        )

        push.notification = jpush.notification(alert="您上传的内容已审核通过！！")
        push.platform = jpush.all_
        print (push.payload)
        push.send()

    def audience(self, userid, body):
        push = self._jpush.create_push()

        push.audience = jpush.audience(
            jpush.alias(userid)
        )


        push.notification = jpush.notification(alert=body)
        push.platform = jpush.all_
        print (push.payload)
        try:
            response=push.send()
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn")
        except common.JPushFailure:
            print ("JPushFailure")
        except:
            print ("Exception")

    def notification(self, userid, title, desc, jsonStr):
        push = self._jpush.create_push()

        push.audience = jpush.audience(
            jpush.alias(userid)
        )

        push.platform = jpush.all_

        push.options = {
            "apns_production": False
        }

        ios = jpush.ios(alert=desc, sound="a.caf", extras=jsonStr, mutable_content=1)
        android = jpush.android(alert=title, priority=1, style=1, alert_type=1, title=title, big_text=desc, extras=jsonStr)

        push.notification = jpush.notification(alert="南海云AI平台识别成功通知", android=android, ios=ios)

        # pprint (push.payload)
        # result = push.send()
        try:
            response=push.send()
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn")
        except common.JPushFailure:
            print ("JPushFailure")
        except:
            print ("Exception")

if __name__ == '__main__':
    # app_key = u'145ae20dfa17aa0c5a1a90a7'
    # master_secret = u'aef06bda9671310fe0c28b89'
    app_key = u'518ac02ef206677bc8e8b0da'
    master_secret = u'c5c5baf57bf15052624ae5a7'

    ipush = mpush(app_key, master_secret)
    # ipush.send()
    # ipush.audience(1, jsonStr)+
    
    image = 'https://ai.hn-ssc.com/media/videos/capture_out_images/8e4932d2-0b45-11ea-93b8-408d5c8912e3/85.jpg'
    
    jsonStr = {
        "name": "王测试",
        "value": "DSFADS ",
        "image": image
    }
    title = "识别通知"
    desc = "您提交的内容已识别结束！"
    # ipush.audience('88EA29CA2B0B48EBB2697CD5B745B8EC', jsonStr)
    # ipush.notification(1, title,desc,jsonStr)
    ipush.notification('88EA29CA2B0B48EBB2697CD5B745B8EC', title,desc,jsonStr)
    
