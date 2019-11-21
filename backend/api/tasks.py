# -*- coding: utf-8 -*-
"""
@author: wangshujing
"""
from django_rq import job
from django.conf import settings
import requests
import json
from .mpush import mpush

app_key = settings.APP_KEY
master_secret = settings.MASTER_SECRET
ipush = mpush(app_key, master_secret)

@job
def task_check_video(iserializer, serial_number):

    video_id = iserializer.id
    url = settings.LOCAL_SERVER + '/api/v1/video/get_video_inspection/?format=json&is_task=1&id=' + str(video_id)
    print (url)
    
    try:
        resp = requests.get(url)#发送请求
        # print (resp.status_code)
        # print (resp.request.url)
        # print (resp.request.body)
        # print (resp.text)
        jsonStr = json.loads(resp.text)
        print (jsonStr)

        # 推送通知消息到APP
        title = "识别通知"
        description = "您提交的内容已识别结束！"
        result = jsonStr['results'][0]
        data = eval(result['data'])
        user_id = result['user_id']
        system_id = result['system_id']
        channel_id = result['channel_id']
        user_id = result['user_id']
        video_url = result['video_url']
        serial_number = result['serial_number']
        screenshot_url = data['screenshot_url']
        violence_sensitivity_level = data['violence_sensitivity_level']
        porn_sensitivity_level = data['porn_sensitivity_level']
        violence_percent = data['violence_percent']
        porn_percent = data['porn_percent']
        
        push_obj = {
            "title": title,
            "description": description,
            "system_id": system_id,
            "channel_id": channel_id,
            "user_id": user_id,
            "video_url": video_url,
            "screenshot_url": screenshot_url,
            "violence_sensitivity_level": violence_sensitivity_level,
            "porn_sensitivity_level": porn_sensitivity_level,
            "violence_percent": violence_percent,
            "porn_percent": porn_percent,
            "serial_number": serial_number
        }
        print (push_obj)
        ipush.notification(user_id, title,description,push_obj)

    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass

    

