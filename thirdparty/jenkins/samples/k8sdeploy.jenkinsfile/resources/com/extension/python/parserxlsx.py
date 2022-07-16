import sys
import openpyxl
import json

first_list = ["urm-core", "urm-entity"]

release_order = {"first":[],"parallels":[], "last": []}

filepath = sys.argv[1]

wb = openpyxl.load_workbook(filepath)
onlineList = []
 
for value in wb.active.values:
    if "√" in value[2:8]:
        onlineList.append(value[1].strip())
 
for first in first_list:
    if first in onlineList:
        onlineList.remove(first)
        release_order["first"].append(first)
 
for name in onlineList:
    if name.startswith("bd"):
        release_order["last"].append(name)
    else:
        release_order["parallels"].append(name)

with open("online.json","w",encoding="utf8") as wf:
    json.dump(release_order, wf)
