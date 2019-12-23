# -*- coding: utf-8 -*-
"""
@author: wangshujing
"""
from django_rq import get_worker
from background_task import background

@background(schedule=60)
def test_task():
    print ("============test_task======================")

@background(schedule=60)
def run_django_rq_task():
    print ("============run_django_rq_task============")
    get_worker().work(burst=True)
