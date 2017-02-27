#!/usr/bin/env python
import argparse
import yaml
import json
import sys
import os
import re

if sys.version_info[0] == 3:
    import urllib.request as request
else:
    import urllib2 as request

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', default='pyoptix', type=str, metavar='IMAGE[:TAG|@DIGEST]',
                    help='docker image identifier')
parser.add_argument('-a', '--host', default='localhost', type=str,
                    help='docker daemon host address')
parser.add_argument('-p', '--port', default=3476, type=int,
                    help='docker daemon port')

(args, extras) = parser.parse_known_args()

resp = request.urlopen('http://{0}:{1}/docker/cli/json'.format(args.host, args.port)).read().decode()
cuda_config = json.loads(resp)
gpu_devices = []
support_devices = []

GPU_DEVICE_PATTERN = re.compile(r'/dev/nvidia\d+')
for dev in cuda_config['Devices']:
    if GPU_DEVICE_PATTERN.match(dev):
        gpu_devices.append(dev)
    else:
        support_devices.append(dev)

gpu_devices.sort()
n_gpu = len(gpu_devices)
volume = cuda_config['Volumes'][0].split(':')[0]

config = yaml.load("""
version: "2"
services:
  pyoptix:
    image: {0}
    volumes:
    - /home/{1}:/home/{1}
    - /etc/group:/etc/group:ro
    - /etc/passwd:/etc/passwd:ro
    - /etc/shadow:/etc/shadow:ro
    - /etc/sudoers:/etc/sudoers:ro
    - /etc/sudoers.d:/etc/sudoers.d:ro
    - /tmp/.X11-unix:/tmp/.X11-unix:rw
    environment:
    - DISPLAY={2}
    user: '{3}'
volumes:
  {4}:
    external: true
""".format(args.image, os.getlogin(), os.environ['DISPLAY'], os.getuid(), volume))

config['services']['pyoptix']['volumes'].extend(cuda_config['Volumes'])
devices = config['services']['pyoptix'].setdefault('devices', [])
if not any(gdev in devices for gdev in gpu_devices):
    devices.extend(gpu_devices)
devices.extend(support_devices)

with open('docker-compose.yml', 'w') as f:
    yaml.safe_dump(config, f, default_flow_style=False)
