# pyqueue_wrapper documentation

## Summary
This a wrapper that standardizes queue services for gevent, iron.IO and AWS (more to come)  
Sometimes there is a need to utilize multiple queue services, but refactoring code is not an option.
With pyqueue_wrapper, one can easily switch between the supported queue services.

## Setup Instructions
###Install
```bash
pip install https://bitbucket.org/imedicare/pyqueue_wrapper/get/master.zip
```

###Setup
Create configuration json file (example):
```javascript
{
    "BASENAME": "my_queue",
    "ENV_MODE": "dev",
    "TYPE": "ironio",
    "ironio": {
        "TOKEN": "xxxxxxxxx",
        "PROJECT_ID": "yyyyyyyyyy",
        "MSG_EXPIRES": 1800,
        "MSG_TIMEOUT": 8400
    },
    "sqs": {
        "TYPE": "sqs",
        "AWS": {
            "AWS_ACCESS_KEY": "zzzzzz",
            "AWS_SECRET_KEY": "xxxxxx"
        }
    }
}
```
**The name of the queue depends on two configuration variables**:

 1. **BASENAME** - name of queue 
 2. **ENV_MODE** - environment suffix used on naming of queue

In this example, the full name of the queue would become my_queue_dev

**Be sure to specify the TYPE**  
**TYPE** - the queue service to use (eg: 'sqs' for AWS SQS, 'ironio' for iron.io QS)

###Usage:
```python
import json
import pyqueue_wrapper

### load configuration file
config = json.loads(open('/path/to/config_file.json')) # see configuration example above
q = pyqueue_wrapper.Queue(config)

### methods
new_message = ({'msg1':'this is a test'})
q.put(new_message)

## get

# iterate through queue
for msg in q:
    print(msg) #Note: will contain 'qid' as reference extra field
# get a single message
received_message = q.get()

## delete
qid = received_message['qid']
q.delete(qid) # Note: not required for AWS SQS, because auto deletes

## clear
q.clear() # clear all messages in queue
```

