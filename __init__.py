"""
Abstract Queue instances
Includes iron.io, AWS, and gevent
"""
__authors__ =  ['Matthew Johnson', 'Lateef Jackson']
__email__ = 'johnson.matthew.h@gmail.com'

import os
import sys
import json
import httplib
from time import sleep

from configobj import ConfigObj
from iron_mq import IronMQ

class Iron:
    def __init__(self, q_config, name):
        self.q_config = q_config
        c = IronMQ(token=self.q_config['TOKEN'], 
                project_id=self.q_config['PROJECT_ID'])
        self.q = c.queue(name)

    def put(self, v):
        m = {'expires_in':int(self.q_config['MSG_EXPIRES']),
             'timeout':int(self.q_config['MSG_TIMEOUT'])}
        m['body'] = json.dumps(v)
        self.q.post(m)

    def get(self):
        while True:
            try: 
                messages = self.q.get(timeout=None)['messages']
            except httplib.BadStatusLine:
                # retry after 5 seconds
                sleep(5)
                continue

            if len(messages) == 0:
                # sleep for 10 secs if queue is empty
                sleep(10) 
                continue

            m = messages[0]
            msg_dict = json.loads(m[u'body'])
            msg_dict['qid'] = m[u'id'] # include queue id
            return msg_dict

    def delete(self, qid):
        self.q.delete(qid)

    def clear(self):
        self.q.clear()

    def size(self):
        return self.q.size()

    __next__ = get
    next = get
    def __iter__(self):
        return self

from boto.sqs.message import Message as SQSMessage
from boto.sqs.connection import SQSConnection
class SQS:
    def __init__(self, q_config, name):
        self.q_config = q_config
        conn = SQSConnection(config['AWS']['AWS_ACCESS_KEY'],
                config['AWS']['AWS_SECRET_KEY'])
        self.q = conn.create_queue(name)

    def put(self, v):
        m = SQSMessage()
        m.set_body(json.dumps(v))
        self.q.write(m)

    def get(self):
        while True:
            messages = self.q.get_messages(1)
            if len(messages) == 0:
                sleep(1) #be nice to cpu 
                continue
            m = messages[0]
            self.q.delete_message(m)
            msg_dict = json.loads(m.get_body())
            msg_dict['qid'] = 'x'  # does not exist with AWS
            return msg_dict

    def clear(self):
        self.q.clear()

    def delete(self, qid):
        pass
            
    __next__ = get
    next = get
    def __iter__(self):
        return self

def Queue(queue_config):
    """Abstract queue object
    Arguments:
        - queue_config (dict): contains configuration for queue
        Example queue configuration:
            {
               'BASENAME': 'my_queue',
               'ENV_MODE': 'dev',
               'TYPE': 'ironio',

               'ironio': {
                 'TOKEN': 'xxxxxxxxx',
                 'PROJECT_ID': yyyyyyyyyy',
                 'MSG_EXPIRES': 1800,
                 'MSG_TIMEOUT': 8400
                },

                'sqs': { 
                 'TYPE': 'sqs',
                 'AWS': {
                         'AWS_ACCESS_KEY':'zzzzzz',
                         'AWS_SECRET_KEY':'xxxxxx'
                        }
                } 
            }
    """

    name = '{0}_{1}'.format(queue_config['ENV_MODE'], queue_config['BASENAME'])
    t = 'TYPE'  # alias

    if t not in queue_config.keys():
        raise Exception('Could not find {0} in configuration'.format(t))

    if queue_config[t] == 'ironio':
        return Iron(queue_config['ironio'], name)

    elif queue_config[t] == 'sqs':
        return SQS(queue_config['sqs'], name)

    elif queue_config[t] == 'gevent':
        from gevent.queue import Queue
        return Queue()

    else:
        raise Exception('No valid queue TYPE specified in configuration: {0}'.format(queue_config[t]))

