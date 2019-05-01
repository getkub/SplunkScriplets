# Converts Splunk inputs.conf to CSV file

import ConfigParser as configparser
import csv

config = configparser.ConfigParser()
config.read('/tmp/inputs.btool')
csv_columns = ['stanza', 'index', 'sourcetype' ]

f=open('/tmp/myoutput.csv', 'wb')
w=csv.DictWriter(f,fieldnames=csv_columns, extrasaction='ignore')
w.writeheader()

for each_section in config.sections():
    mydict = dict(config.items(each_section))
    mydict['stanza'] = each_section
    w.writerow(mydict)
    
f.close()
