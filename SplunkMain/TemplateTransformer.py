import shutil
import time
import os, sys
import fnmatch
import pystache
import json

localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)

dstA = "/tmp/" + "workspace." + timeString
if not os.path.exists(dstA):
    os.makedirs(dstA)

srcA = "/home/user1/data/mustache/"
item = "local"

# Source and Destination Directories
src = os.path.join(srcA, item)
dst = os.path.join(dstA, item)

def copyDirectory(src, dst):
    try:
        print('Start Copying Directory: ')
        shutil.copytree(src, dst)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
        sys.exit(1)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
        sys.exit(1)
    else:
        print('Directory Copied Successfully')

copyDirectory(src,dst)

# JSON Configuration File
jsonConfig = "spnk.json"
with open(jsonConfig) as json_file:
    d = json.load(json_file)

matches = []
renderer = pystache.Renderer()

# Identifies "root" of destination directory
# Filters down the file and opens new file without extension "mustache"
# Writes the file and cleans up  .mustache files

for root, dirnames, filenames in os.walk(dst):
  for filename in fnmatch.filter(filenames, '*.mustache'):
    templateFile = os.path.join(root, filename)
    matches.append(templateFile)
    f1=open(os.path.splitext(templateFile)[0], 'w+')
    f1.write(renderer.render_path(templateFile, d))
    f1.close()
    os.remove(templateFile)

print "Files Modified => " + str(matches)
