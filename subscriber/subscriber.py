import os
import json
import redis
import time
import datetime
from elasticsearch_dsl import Float, Document, Date, Integer, Keyword
from elasticsearch_dsl.connections import connections

class DelayData(Document):
    received_messages = Integer()
    sum_delay = Float()
    avg_delay = Float()
    msg_per_Second = Float()
    timestamp = Date()
    pid = Keyword()

    class Index:
        name = 'subscriber'

    def save(self, **kwargs):
        return super(DelayData, self).save(**kwargs)

    def is_published(self):
        return datetime.datetime.now() >= self.published_from


class ElasticHelper(object):
  def __init__(self):
    self.conn = connections.create_connection(hosts=['elasticsearch:9200'])
    self.index = 'subscriber'
    DelayData().init()

  def insert_document(self, **kwargs):
    return DelayData(**kwargs).save()


def get_current_milliseconds():
  return int(round(time.time() * 1000))

redis_conn = redis.StrictRedis(host='redis', port=6379)
pubsub = redis_conn.pubsub()
pubsub.subscribe(['test_channel'])

print('Waiting for messagens...')

counter = 0
delays = []
elastic_logger = ElasticHelper()

# set timezone
timezone = "GTM"
os.environ['TZ'] = timezone
time.tzset()

hostname = open('/etc/hostname', 'r').read()
MSG_INTERVAL = 10000

for message in pubsub.listen():

  # First event received when the channel is open
  if message['type'] == 'subscribe':
    base_milli = get_current_milliseconds()
    continue

  current_milli = get_current_milliseconds()
  parsed_msg = json.loads(message['data'])
  delays.append(current_milli - parsed_msg['sent_ms'])

  counter += 1
  if counter % MSG_INTERVAL == 0:

    delta_t = (current_milli - base_milli) / 1000.0
    data = {
    'received_messages': counter,
    'sum_delay': sum(delays),
    'avg_delay': (sum(delays)/len(delays)),
    'msg_per_Second': (MSG_INTERVAL/delta_t),
    'timestamp': datetime.datetime.now(),
    'pid': hostname
    }

    elastic_logger.insert_document(**data)
    print(
      'Received msgs: {received_messages}. Delay: sum={sum_delay} avg={avg_delay}. msg/s: {msg_per_Second}'
      .format(**data)
    )
    delays = []