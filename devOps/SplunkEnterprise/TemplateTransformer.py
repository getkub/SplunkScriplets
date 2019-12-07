import shutil
import time
import os, sys, argparse
import fnmatch
import pystache
import json

localtime   = time.localtime()
timeString  = time.strftime("%Y%m%d%H%M%S", localtime)

# ----------------------------------------------------------------------
#
# This script will transform template into final code when following inputs are given
#     - Template Source
#     - configuration data in JSON
#     - Environment Tag
#
# ----------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Validate Input Config')
parser.add_argument('source',metavar='sourceDir', help=' - Source Directory with templates')
parser.add_argument('configs', metavar='configFile', help=' - Absolute Path of Config File')
parser.add_argument('env',metavar='environment', help=' - Environment like DEV, TEST, PROD')

args = parser.parse_args()
if not os.path.isfile(args.configs):
      print('Config file not exists. Quitting... ')
      sys.exit(1)

if not os.path.exists(args.source):
      print('Source Template Directory NOT exists. Quitting... ')
      sys.exit(1)

ENV = args.env

print "===== Start of Script ====="

srcA = args.source
item = ""
dstA = "/tmp/" + "workspace." + timeString
errors = []

# Source and Destination Directories
src = os.path.join(srcA, item)
dst = os.path.join(dstA, item)

# print ('SRC = %s' % src)
# print ('DST = %s' % dst)

#if not os.path.exists(dst):
#     os.makedirs(dst)

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
        print('Directories Copied Temporarily to -> %s' % dstA)

copyDirectory(src,dst)

# JSON Configuration File
jsonConfig = args.configs
with open(jsonConfig) as json_file:
    d = json.load(json_file)

# Parse data just for required Environment
envSpecific = d[ENV]
# print(envSpecific)

matches = []
renderer = pystache.Renderer()

# Identifies "root" of destination directory
# Filters down the file and opens new file without extension "mustache"
# Writes the file and cleans up  .mustache files

for root, dirnames, filenames in os.walk(dst):
  for filename in fnmatch.filter(filenames, '*.mustache'):
    templateFile = os.path.join(root, filename)
    newFile = os.path.splitext(templateFile)[0]
    matches.append(newFile)
    f1=open(newFile, 'w+')
    f1.write(renderer.render_path(templateFile, envSpecific))
    f1.close()
    os.remove(templateFile)

print "Files Modified => " + str(matches)
print "===== End of Script ====="
