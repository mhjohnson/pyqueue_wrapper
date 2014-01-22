#!/usr/bin/env python

from distutils.core import setup

setup(name='pyqueue_wrapper',
      version='1.0.1',
      description=' Wrapper for popular queues like Amazon SQS and iron.IO',
      author='Matthew H. Johnson, PharmD',
      author_email='johnson.matthew.h@gmail.com',
      url='https://bitbucket.org/mhjohnson/pyqueue_wrapper/overview',
      packages=['pyqueue_wrapper'],
      install_requires=['iron-core>=1.1.1', 'iron-mq>=0.5', 'boto>=2.8.0']
     )
