from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .producer import publish


@shared_task(name = "share_data")
def share_data_to_other_node(message, *args, **kwargs):
  publish()

# @shared_task(name = "print_time")
# def print_time():
#   now = datetime.now()
#   current_time = now.strftime("%H:%M:%S")
#   print(f"Current Time is {current_time}")
  
# @shared_task(name='get_calculation')
# def calculate(val1, val2):
#   total = val1 + val2
#   return total