import re

id_regex = re.compile(" [A-F0-9]{7,10}")
client_regex = re.compile(".* client=(.*)$")
from_regex = re.compile(".* from=<(.*?)>, ")
to_regex = re.compile(".* to=<(.*?)>, ")
relay_regex = re.compile(" relay=(.*?(?:\[.*\].?[0-9]*)?), ")
status_regex = re.compile(" status=(.*?) (.*)$")
score_regex = re.compile(" Hits: ([0-9\-\.]+), ")
amavisstatus_regex = re.compile("\([0-9\-]+\)([a-zA-Z\- 0-9]+)")
