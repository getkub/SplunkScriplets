import ConfigParser as configparser
config = configparser.ConfigParser()
config.read('/tmp/inputs.btool')

for each_section in config.sections():
    for (each_key, each_val) in config.items(each_section):
        print each_key , ':' , each_val
