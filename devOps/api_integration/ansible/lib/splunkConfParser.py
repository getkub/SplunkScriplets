import configparser
import sys, os

splunkConfJSON =  {}
# Get All config contents
def ConfigSectionMap(configFile):
    dict1 = {}
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform=str
    try:
        config.read(configFile)
        for cs in config.sections():
            dict1[cs] = config.items(cs)
    except configparser.MissingSectionHeaderError as mshe:
        dict1['error_type'] = "MissingSectionHeaderError"
        dict1['error_details'] = mshe
    except configparser.ParsingError as pe:
        dict1['error_type'] = "ParsingError"
        dict1['error_details'] = pe
    except configparser.DuplicateSectionError as dse:
        dict1['error_type'] = "DuplicateSectionError"
        dict1['error_details'] = dse
    except configparser.DuplicateOptionError as doe:
        dict1['error_type'] = "DuplicateOptionError"
        dict1['error_details'] = doe
    except configparser.Error as e:
        dict1['error_type'] = "configparser_OtherError"
        dict1['error_details'] = e
    finally:
        return dict1

# https://wiki.python.org/moin/ConfigParserExamples
if len(sys.argv) > 1:
    inFile = sys.argv[1]
    if os.path.isfile(inFile) and os.access(inFile, os.R_OK):
        splunkConfJSON = ConfigSectionMap(inFile)
    else:
        splunkConfJSON['error_type'] = "fileError"
else:
    splunkConfJSON['error_type'] = "NoInputArgumentError"

print(splunkConfJSON)
