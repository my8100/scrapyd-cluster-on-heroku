# coding: utf-8
import io
import os
from subprocess import Popen


# https://devcenter.heroku.com/articles/runtime-principles#web-servers
# The port to bind to is assigned by Heroku as the PORT environment variable.
PORT = os.environ['PORT']
with io.open("scrapyd.conf", 'r+', encoding='utf-8') as f:
    f.read()
    f.write(u'\nhttp_port = %s\n' % PORT)


# Launch LogParser as a subprocess
logs_dir = '/app/logs'
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

args = ['logparser', '-dir', logs_dir]
args.extend(['--scrapyd_server', '127.0.0.1:%s' % PORT])
args.extend(['--sleep', os.environ.get('PARSE_ROUND_INTERVAL', '10')])
if os.environ.get('ENABLE_TELNET', 'True') == 'False':
    args.extend(['--disable_telnet'])
if os.environ.get('VERBOSE', 'False') == 'True':
    args.extend(['--verbose'])
Popen(args)
