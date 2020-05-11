import json
import redis
import time
import os

def get_current_milliseconds():
  return int(round(time.time() * 1000))


def discover_channels():
  channels_str = os.getenv('REDIS_CHANNELS', 'test_channel')
  return channels_str.split(':')

channels = discover_channels()
print('Messages are going to be published to {} channels: {}'.format(len(channels), channels))

print('Starting sending messagens in...')
for i in reversed(range(5)):
  print(i)
  time.sleep(1)

redis_conn = redis.StrictRedis(host='redis', port=6379)

template_msg = {'come': 'abacate', 'come1': 'abacate', 'come2': 'abacate', 'come3': 'abacate', }

while True:
  template_msg['sent_ms'] = get_current_milliseconds()
  json_msg = json.dumps(template_msg)

  for channel in channels:
    redis_conn.publish(channel, json_msg)
