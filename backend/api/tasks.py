# -*- coding: utf-8 -*-
"""
@author: wangshujing
"""
from django_rq import job
from django.conf import settings
import requests
import json


@job
def task_check_video(iserializer, serial_number):

    video_id = iserializer.id
    url = settings.LOCAL_SERVER + '/api/v1/video/get_video_inspection/?format=json&is_task=1&id=' + video_id
    
    try:
        resp = requests.get(url)#发送请求
        # print (resp.status_code)
        # print (resp.request.url)
        # print (resp.request.body)
        # print (resp.text)
        jsonStr = json.loads(resp.text)
        print (jsonStr)
    except requests.Timeout:
        pass
    except requests.ConnectionError:
        pass

    

