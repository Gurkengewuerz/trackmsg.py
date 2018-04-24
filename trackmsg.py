#!/usr/bin/python3
from bottle import route, run, template, static_file, auth_basic, response
from regex_postfix import *
from datetime import datetime
import math
import json
import config

class PostfixLogParser():
    
    def __init__(self, logfile="/var/log/mail.log", sender=".*", recipient=None):
        self.search_tokens = []
        self.search_tokens.append(client_regex)
        
        self.logfile = logfile
        self.sender = sender
        self.recipient = recipient

        if sender:
            self.search_tokens.append(re.compile(".* from=<" + sender + ">.*"))
            self.search_tokens.append(re.compile(".*<" + sender + "> ->.*"))
        else:
            self.search_tokens.append(from_regex)
        
        if recipient:
            self.search_tokens.append(re.compile(".* to=<" + recipient + ">.*"))
            self.search_tokens.append(re.compile(".* -> .*<" + recipient + ">.*"))
        elif not sender:
            self.search_tokens.append(to_regex)

        with open(self.logfile) as f:
            self.f = f.readlines()


    def parse(self):
        messages_dict = {}
        return_array = []
        for line in self.f:
            for phrase in self.search_tokens:
                if phrase.match(line):
                    message_id = None
                    message_ids = id_regex.findall(line)
                    if message_ids:
                        message_id = message_ids[0].lstrip()
                        message_id_regex = re.compile(".* " + message_id + "[:,] .*")
                        if not message_id_regex in self.search_tokens:
                            if (self.sender and not client_regex.match(line)) or (self.recipient and (not from_regex.match(line) and not client_regex.match(line))):
                                self.search_tokens.append(message_id_regex)
                    if message_id:
                        if not message_id in messages_dict:
                            messages_dict[message_id] = {}
                            messages_dict[message_id]['id'] = message_id
                            messages_dict[message_id]['date'] = None
                            messages_dict[message_id]['timestamp'] = None
                            messages_dict[message_id]['server'] = None
                            messages_dict[message_id]['sender'] = None
                            messages_dict[message_id]['recipient'] = None
                            messages_dict[message_id]['relay'] = None
                            messages_dict[message_id]['status'] = None
                            messages_dict[message_id]['score'] = "N/A"

                        client = client_regex.findall(line)
                        if client:
                            messages_dict[message_id]['server'] = client[0]
                            break

                        sender = from_regex.findall(line)
                        if sender:
                            messages_dict[message_id]['sender'] = sender[0]
                            break

                        to = to_regex.findall(line)
                        if to:
                            messages_dict[message_id]['recipient'] = to[0]

                        relay = relay_regex.findall(line)
                        if relay:
                            messages_dict[message_id]['relay'] = relay[0]

                        score = score_regex.findall(line)
                        if score:
                            amavisstatus = amavisstatus_regex.findall(line)
                            if not amavisstatus:
                                amavisstatus = "N/A"
                            else:
                                amavisstatus = amavisstatus[0]
                            score = "%s%s" % (score[0], amavisstatus)
                            messages_dict[message_id]['score'] = score
                        
                        date_split = line.split(" ")
                        if len(date_split) >= 3:
                            messages_dict[message_id]['date'] = date_split[0] + " " + date_split[1]  + " " + date_split[2]
                            messages_dict[message_id]['timestamp'] = datetime.strptime(messages_dict[message_id]['date'], "%b %d %H:%M:%S").strftime('%s')

                        status = status_regex.findall(line)
                        if status:
                            messages_dict[message_id]['status'] = status[0][0]
                            messages_dict[message_id]['status_extended'] = status[0][1]
                            #if messages_dict[message_id]['score'] != "N/A":
                            return_array.append(messages_dict[message_id])
                            break

                    break

        return json.dumps(return_array)


def check(user, pw):
    return pw == config.AUTH_BASIC_PASSWORD

@route("/")
@auth_basic(check)
def index():
    return template("index.tpl")
    
@route("/data")
@auth_basic(check)
def index():
    p = PostfixLogParser(logfile=config.LOGFILE)
    response.content_type = "application/json; charset=utf-8"
    return p.parse()


run(host = "0.0.0.0", port = config.LISTEN_PORT)