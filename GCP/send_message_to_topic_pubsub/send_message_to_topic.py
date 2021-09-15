import json
import re
import os
import subprocess
import os
from subprocess import Popen

def send_to_pubsub_subprocess(list_messages, topic):
    try:
        FNULL = open(os.devnull, 'w')
        commands=[]
        #gcloud pubsub topics publish topic1 --message "$(cat message.json)"
        for message in list_messages:
            commands.append(["gcloud", "pubsub", "topics", "publish", topic, "--message", message])

        procs = [ Popen(command,stdout=FNULL) for command in commands ]
        return True
    except Exception as e:
        return False

def read_json_file(filename):
    with open(filename) as json_file:
        text = json_file.read()
        return text
        #json_data = json.load(json_file)
        #print(text)

test_messages = []
#send_to_pubsub_subprocess(list_messages=test_messages, topic='topic1')
for i in range(10):
    test_messages.append(read_json_file(filename="/home/maximiliano.barrios/IdeaProjects/project3/message.json"))

print(len(test_messages))
print(test_messages)



