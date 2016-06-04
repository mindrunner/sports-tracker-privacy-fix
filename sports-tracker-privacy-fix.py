#!/usr/bin/env python
#
# This file is part of sports-tracker-privacy-fix.  sports-tracker-privacy-fix
# is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__ = "Lukas Elsner"
__copyright__ = "Copyright 2014, mindrunner"
__credits__ = ["Rocky"]
__license__ = "GPL"
__version__ = "2"
__maintainer__ = "Lukas Elsner"
__email__ = "open@mindrunner.de"
__status__ = "Prototype"

import requests
import json
import os

# Setup
user = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
# 0  for private
# 17 for friends
# ?? for public
visibility = 17

# Login
# TODO: Check for wrong login data
payload = {'l': user, 'p': password}
r = requests.post("http://www.sports-tracker.com/apiserver/v1/login"
                  "?source=javascript",
                  data=payload)
j = json.loads(r.text)
skey = j['sessionkey']

print("Logged in as {}".format(j['username']))
print("Sessionkey is {}".format((skey)))

cookies = dict(sessionkey=skey, dashboardFeed="my-workouts")
headers = {'STTAuthorization': skey, 'Content-Type': 'application/json'}

# Get the feed (first 9999 items)
r = requests.get("http://www.sports-tracker.com/apiserver/v1/workouts"
                 "?sortonst=true&limit=9999&offset=0",
                 cookies=cookies, headers=headers)

data = json.loads(r.text)

# Loop through the result.
for item in data['payload']:
    print("workoutKey: {}".format((item['workoutKey'])))
    print("totalTime: {}".format((item['totalTime'])))
    print("visibilityFriends: {}".format((item['visibilityFriends'])))
    print("sharingFlags: {}".format((item['sharingFlags'])))

    if 'description' in item:
        description = item['description']
    else:
        description = 'unnamed'

    if item['sharingFlags'] != visibility:
        payload = [
            {"totalDistance": item['totalDistance'],
             "workoutKey": item['workoutKey'],
             "activityId": item['activityId'],
             "startTime": item['startTime'],
             "totalTime": item['totalTime'],
             "description": description,
             "hrMaxValue": item['hrdata']['max'],
             "hrAvgValue": item['hrdata']['avg'],
             "energyConsumption": item['energyConsumption'],
             "sharingFlags": visibility}
        ]
        r = requests.post("http://www.sports-tracker.com/"
                          "apiserver/v1/workouts/header",
                          cookies=cookies, headers=headers,
                          data=json.dumps(payload))
        print(r.text)
    else:
        print("Nothing to fix")
        print()
