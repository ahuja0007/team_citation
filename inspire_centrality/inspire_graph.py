import fileinput
import json
import codecs
import sys
import ast

UTF8writer = codecs.getwriter('utf8')
sys.stdout = UTF8writer(sys.stdout)

for line in fileinput.input():
  key, value = line.split('\t')
  key = ast.literal_eval(key)
  d = json.loads(value)
  for collab in d.keys():
    print key, collab, d[collab]
