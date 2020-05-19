# $language = "Python"
# $interface = "1.0"

# ImportArbitraryDataFromFileToSecureCRTSessions.py
#   (Designed for use with SecureCRT 6.7 and later)
#   Last Modified: 02 Jul, 2015
#      - Display status bar info for each line we're processing so that if
#        there's an error, the individual running the script might have
#        better information about why the error might have occurred.
#      - Handle cases where a line in the data file might have more fields
#        in it than the number of header fields designated for import. This
#        fixes an error reported by forum user wixxyl here:
#           https://forums.vandyke.com/showthread.php?t=12021
#        If a line has too many fields, create a warning to be displayed
#        later on, and move on to the next line -- skipping the current line
#        because it's unknown whether the data is even valid for import.
#   Last Modified: 24 Nov, 2015
#   Last Modified: 20 Jan, 2015
#      - Combined TAPI protocol handling (which is no longer
#        supported for mass import) with Serial protocol
#        import errors.
#      - Enhanced example .csv file data to show subfolder specification.
#
#   Last Modified: 21 Mar, 2012
#      - Initial version for public forums
#
# DESCRIPTION
# This sample script is designed to create sessions from a text file (.csv
# format by default, but this can be edited to fit the format you have).
#
# To launch this script, map a button on the button bar to run this script:
#    http://www.vandyke.com/support/tips/buttonbar.html
#
# The first line of your data file should contain a comma-separated (or whatever
# you define as the g_strDelimiter below) list of supported "fields" designated
# by the following keywords:
# -----------------------------------------------------------------------------
# session_name: The name that should be used for the session. If this field
#               does not exist, the hostname field is used as the session_name.
#       folder: Relative path for session as displayed in the Connect dialog.
#     hostname: The hostname or IP for the remote server.
#     protocol: The protocol (SSH2, SSH1, telnet, rlogin)
#         port: The port on which remote server is listening
#     username: The username for the account on the remote server
#    emulation: The emulation (vt100, xterm, etc.)
#  description: The comment/description. Multiple lines are separated with '\r'
# =============================================================================
#
#
# As mentioned above, the first line of the data file instructs this script as
# to the format of the fields in your data file and their meaning.  It is not a
# requirement that all the options be used. For example, notice the first line
# of the following file only uses the "hostname", "username", and "protocol"
# fields.  Note also that the "protocol" field can be defaulted so that if a
# protocol field is empty it will use the default value.
# -----------------------------------------------------------------------------
#   hostname,username,folder,protocol=SSH2
#   192.168.0.1,root,_imported,SSH1
#   192.168.0.2,admin,_imported,SSH2
#   192.168.0.3,root,_imported/folderA,
#   192.168.0.4,root,,
#   192.168.0.5,admin,_imported/folderB,telnet
#   ... and so on
# =============================================================================

import datetime
import os
import platform
import re
import shutil
import sys
import time
import subprocess

MsgBox = crt.Dialog.MessageBox

# The g_strDefaultProtocol variable will only be defined within the
# ValidateFieldDesignations function if the protocol field has a default value
# (e.g., protocol=SSH2), as read in from the first line of the data file.
global g_strDefaultProtocol
g_strDefaultProtocol = ""

# If your data file uses spaces or a character other than comma as the
# delimiter, you would also need to edit the g_strDelimiter value a few lines
# below to indicate that fields are separated by spaces, rather than by commas.
# For example:
#       g_strDelimiter = " "
# Using a ";" might be a good alternative for a file that includes the comma
# character as part of any legitimate session name or folder name, etc.
global g_strDelimiter
g_strDelimiter = ","      # comma
# g_strDelimiter = " "    # space
# g_strDelimiter = ";"    # semi-colon
# g_strDelimiter = chr(9) # tab
# g_strDelimiter = "|||"  # a more unique example of a delimiter.

# The g_strSupportedFields indicates which of all the possible fields, are
# supported in this example script.  If a field designation is found in a data
# file that is not listed in this variable, it will not be imported into the
# session configuration.
global g_strSupportedFields
g_strSupportedFields = \
    "description,emulation,folder,hostname,port,protocol,session_name,username"

# If you wish to overwrite existing sessions, set the
# g_bOverwriteExistingSessions to True; for this example script, we're playing
# it safe and leaving any existing sessions in place :).
global g_bOverwriteExistingSessions
g_bOverwriteExistingSessions = False

strOSVer = platform.release()
strHome = os.path.expanduser("~")
global g_strMyDocs
g_strMyDocs = strHome + "/Documents"
if not os.path.isdir(g_strMyDocs):
    # Handle special Windows XP case.
    if strOSVer == "XP":
        g_strMyDocs = strHome + "/My Documents"
    # Handle special CentOS 5.x case.  We make the Documents folder since it
    # doesn't exist in CentOS 5.x.
    elif "el5" in strOSVer:
        try:
            os.makedirs(g_strMyDocs)
        # Since SecureCRT on Mac OS X uses Python 2.5, we are using the old
        # syntax for casting an exception as an object for later use.
        # Python 2.6 and newer would use "except Exception as objErr".
        except Exception, objErr:
            MsgBox("Failed to create log folder at:\n\n" +
            strLogFilePath + "\n\nWith error:\n\n" + str(objErr) +
            "\n\nWill use home folder.")
            g_strMyDocs = strHome

global g_strHostsFile
g_strHostsFile = g_strMyDocs + "/MyDataFile10.csv"

global g_strExampleHostsFile
g_strExampleHostsFile = \
    "\thostname,protocol,username,folder,emulation\n" + \
    "\t192.168.0.1,SSH2,root,Linux Machines,XTerm\n" + \
    "\t192.168.0.2,SSH2,root,Linux Machines,XTerm\n" + \
    "\t...\n" + \
    "\t10.0.100.1,SSH1,admin,CISCO Routers,VT100\n" + \
    "\t10.0.101.1,SSH1,admin,CISCO Routers,VT100\n" + \
    "\t...\n" + \
    "\tmyhost.domain.com,SSH2,administrator,Windows Servers,VShell\n" + \
    "\t...\n"

g_strExampleHostsFile = g_strExampleHostsFile.replace(",", g_strDelimiter)

global g_strConfigFolder, strFieldDesignations, g_strFieldsArray, vSessionInfo

global strSessionName, strHostName, strPort
global strUserName, strProtocol, strEmulation
global strPathForSessions, strLine, nFieldIndex
global strSessionFileName, strFolder, nDescriptionLineCount, strDescription

global g_strLastError, g_strErrors, g_strSessionsCreated
global g_nSessionsCreated, g_nDataLines
g_strLastError = ""
g_strErrors = ""
g_strSessionsCreated = ""
g_nSessionsCreated = 0
g_nDataLines = 0

# Use current date/time info to avoid overwriting existing sessions by
# importing sessions into a new folder named with a unique timestamp.
g_strDateTimeTag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")[:19]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ValidateFieldDesignations(strFields):
    global g_strDelimiter, g_strExampleHostsFile, g_strDefaultProtocol
    global g_strFieldsArray
    if strFields.find(g_strDelimiter) == -1:
        strErrorMsg = "Invalid header line in data file. " + \
            "Delimiter character not found: "
        if len(g_strDelimiter) > 1:
            strDelimiterDisplay = g_strDelimiter
        else:
            if ord(g_strDelimiter) < 33 or ord(g_strDelimiter) > 126:
                strDelimiterDisplay = "ASCII[" + ord(g_strDelimiter) + "]"
            else:
                strDelimiterDisplay = g_strDelimiter

        strErrorMsg = "".join(
            strErrorMsg,
            strDelimiterDisplay,
            "\n\n",
            "The first line of the data file is a header line ",
            "that must include\n",
            "a '" + strDelimiterDisplay,
            "' separated list of field keywords.\n",
            "\n",
            "'hostname' and 'protocol' are required keywords.",
            "\n\n",
            "The remainder of the lines in the file should follow the ",
            "\n",
            "pattern established by the header line ",
            "(first line in the file).\n" + "For example:\n",
            g_strExampleHostsFile)
        MsgBox(strErrorMsg, "Import Data To SecureCRT Sessions")
        return

    g_strFieldsArray = strFields.split(g_strDelimiter)
    if not "hostname" in g_strFieldsArray:
        strErrorMsg = "Invalid header line in data file. " + \
            "'hostname' field is required."
        if len(g_strDelimiter) > 1:
            strDelimiterDisplay = g_strDelimiter
        else:
            if ord(g_strDelimiter) < 33 or ord(g_strDelimiter) > 126:
                strDelimiterDisplay = "ASCII[" + ord(g_strDelimiter) + "]"
            else:
                strDelimiterDisplay = g_strDelimiter

        MsgBox(strErrorMsg + "\n" +
            "The first line of the data file is a header line " +
            "that must include\n" +
            "a '" + strDelimiterDisplay +
            "' separated list of field keywords.\n" +
            "\n" +
            "'hostname' and 'protocol' are required keywords." +
            "\n\n" +
            "The remainder of the lines in the file should follow the " +
            "\n" +
            "pattern established by the header line " +
            "(first line in the file)." + "\n" + "For example:\n" +
            g_strExampleHostsFile,
            "Import Data To SecureCRT Sessions")
        return


    if not "protocol" in g_strFieldsArray:
        if strFields.find("protocol=") == -1:
            MsgBox("Invalid data file header line: \n\n" +
                "\t" + strFieldDesignations + "\n" +
                "\n--> 'protocol' field is required.",
                "Import Data To SecureCRT Sessions")
            return

    for strField in g_strFieldsArray:
        #MsgBox("{0}\nHas 'protocol': {1}\nHas '=': {2}".format(strField, strField.find("protocol"), strField.find("=")))
        if strField.find("protocol") > -1 and \
           strField.find("=") > -1:
                g_strDefaultProtocol = strField.split("=")[1].upper()
                #MsgBox(("Found a default protocol spec: {0}".format(g_strDefaultProtocol)))
                # Fix the protocol field since we know the default protocol
                # value
                strFields = strFields.replace(strField, "protocol")


    g_strFieldsArray = strFields.split(g_strDelimiter)
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def SessionExists(strSessionPath):
    # Returns True if a session specified as value for strSessionPath already
    # exists within the SecureCRT configuration.
    # Returns False otherwise.
    try:
        objTosserConfig = crt.OpenSessionConfiguration(strSessionPath)
        return True
    except Exception as objInst:
        return False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def OpenPathInDefaultApp(strFile):
    strPlatform = sys.platform
    strOSVer = platform.release()
    try:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', strFile))
        elif strPlatform == "win32":
            os.startfile(strFile)
        elif "el5" in strOSVer or "el6" in strOSVer:
            os.system("gedit " + strFile)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', strFile))
        else:
            MsgBox("Unknown operating system:  " + os.name)
    except Exception, objErr:
        MsgBox(
            "Failed to open " + strFile + " with the default app.\n\n"  +
            str(objErr).replace('\\\\', '\\').replace('u\'', '\''))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Import():
    global g_strHostsFile, strFieldDesignations, g_strErrors, g_strDelimiter
    global g_strDefaultProtocol, g_nDataLines, g_strSessionsCreated, g_nSessionsCreated
    g_strHostsFile = crt.Dialog.FileOpenDialog(
        "Please select the host data file to be imported.",
        "Open",
        g_strHostsFile,
        "Text Files (*.txt)|*.txt|CSV Files (*.csv)|*.csv||")

    if g_strHostsFile == "":
        return

    nStartTime = time.time()
    bFoundHeader = False
    nLine = 0
    vSessionInfo = []
    # Open our data file for reading
    with open(g_strHostsFile, "r") as objDataFile:
        # Iterate over each of the lines in the file, processing them one by one.
        for strLine in objDataFile:
            strLine = strLine.strip("\r\n")
            nLine += 1
            # if nLine == 1 or (nLine % 10) == 0:
            crt.Session.SetStatusText("Processing line #{0} from import file: {1}".format(nLine, str(strLine)))
            bSaveSession = False
            strSessionPath = ""
            strPort = ""
            strProtocol = ""
            strHostName = ""
            strUserName = ""
            strEmulation = ""
            strFolder = ""
            strDescription = ""
            if not bFoundHeader:
                strFieldDesignations = strLine
                # Validate the data file
                if not ValidateFieldDesignations(strFieldDesignations):
                    return
                else:
                    # Get a timer reading so that we can calculate how long it takes to import.
                    nStartTime = time.time()
                    bFoundHeader = True
            else:
                vSessionInfo = strLine.split(g_strDelimiter)
                if len(vSessionInfo) < len(g_strFieldsArray):
                    if strLine.strip() == "":
                        strLine = "[Empty Line]"
                    g_strErrors = ("\n" +
                        "Insufficient data on line #{0:04d}: {1:s}{2:s}".format(nLine, strLine, g_strErrors))
                else:
                    # Variable used to determine if a session file should actually be
                    # created, or if there was an unrecoverable error (and the session
                    # should be skipped).
                    bSaveSession = True

                    # Now we will match the items from the new file array to the correct
                    # variable for the session's ini file
                    for nFieldIndex in xrange(0, len(vSessionInfo)):
                        if nFieldIndex >= len(g_strFieldsArray):
                            g_strErrors = ("\n" +
                                "Error: Too many data fields({0:d}) found on line #{1:04d}: {2:s}".format(len(vSessionInfo), nLine, strLine) +
                                "<-- This line should only have these {0:d} fields: {1:s}{2:s}".format(len(g_strFieldsArray), ",".join(g_strFieldsArray), g_strErrors))
                            bSaveSession = False
                            break

                        #MsgBox("nFieldIndex: {0}\nlen(vSessionInfo):{1}\n{2}:{3}".format(nFieldIndex, len(vSessionInfo), g_strFieldsArray[nFieldIndex], vSessionInfo[nFieldIndex]))
                        strFieldLabel = g_strFieldsArray[nFieldIndex].strip()
                        if strFieldLabel == "session_name":
                            strSessionName = vSessionInfo[nFieldIndex].strip()
                            # Check folder name for any invalid characters
                            mSession = re.search(r"[\\\|\/\:\*\?\\\"\<\>]", strSessionName)
                            if mSession:
                                bSaveSession = False
                                g_strErrors = ("\nError: Invalid characters found in SessionName \"{0}\" specified on line #{1:04d}: {2:s}{3:s}".format(
                                    strSessionName, nLine, strLine, g_strErrors))

                        elif strFieldLabel == "port":
                            strPort = vSessionInfo[nFieldIndex].strip()
                            if not strPort == "":
                                if not strPort.isdigit():
                                    bSaveSession = False
                                    g_strErrors = ("\nError: Invalid port \"{0}\" specified on line #{1:04d}: {2:s}{3:s}".format(
                                        strPort, nLine, strLine, g_strErrors))

                        elif strFieldLabel == "protocol":
                            strProtocol = vSessionInfo[nFieldIndex].lower().strip()


                            if strProtocol == "ssh2":
                                strProtocol = "SSH2"
                            elif strProtocol == "ssh1":
                                strProtocol = "SSH1"
                            elif strProtocol == "telnet":
                                strProtocol = "Telnet"
                            elif strProtocol == "serial" or strProtocol == "tapi":
                                bSaveSession = False
                                g_strErrors = ("\n" +
                                    "Error: Unsupported protocol \"" + vSessionInfo[nFieldIndex].strip() +
                                    "\" specified on line #" +
                                    "{0:04d}: {1:s}".format(nLine, strLine) +
                                    g_strErrors)
                            elif strProtocol == "rlogin":
                                strProtocol = "RLogin"
                            else:
                                if g_strDefaultProtocol <> "":
                                    strProtocol = g_strDefaultProtocol
                                else:
                                    bSaveSession = False
                                    g_strErrors = ("\n" +
                                        "Error: Invalid protocol \"" + strProtocol +
                                        "\" specified on line #" +
                                        "{0:04d}: {1:s}".format(nLine, strLine) +
                                        g_strErrors)

                        elif strFieldLabel == "hostname":
                            strHostName = vSessionInfo[nFieldIndex].lower().strip()
                            if strHostName == "":
                                bSaveSession = False
                                g_strErrors = ("\n" +
                                    "Error: Hostname field on line #{0:04d} is empty: {1:s}".format(nLine, strLine) +
                                    g_strErrors)

                        elif strFieldLabel == "username":
                            strUserName = vSessionInfo[nFieldIndex].lower().strip()

                        elif strFieldLabel == "emulation":
                            strEmulation = vSessionInfo[nFieldIndex].lower().strip()
                            if strEmulation == "xterm":
                                strEmulation = "Xterm"
                            elif strEmulation == "vt100":
                                strEmulation = "VT100"
                            elif strEmulation == "vt102":
                                strEmulation = "VT102"
                            elif strEmulation == "vt220":
                                strEmulation = "VT220"
                            elif strEmulation == "ansi":
                                strEmulation = "ANSI"
                            elif strEmulation == "linux":
                                strEmulation = "Linux"
                            elif strEmulation == "scoansi":
                                strEmulation = "SCOANSI"
                            elif strEmulation == "vshell":
                                strEmulation = "VShell"
                            elif strEmulation == "wyse50":
                                strEmulation = "WYSE50"
                            elif strEmulation == "wyse60":
                                strEmulation = "WYSE60"
                            else:
                                bSaveSession = False
                                g_strErrors = ("\n" +
                                    "Error: Invalid emulation \"{0}\" specified on line #{1:04d}: {2:s}{3:s}".format(
                                        strEmulation, nLine, strLine, g_strErrors))

                        elif strFieldLabel == "folder":
                            strFolderOrig = vSessionInfo[nFieldIndex].strip()
                            strFolder = strFolderOrig.lower()

                            # Check folder name for any invalid characters
                            # Note that a folder can have subfolder designations,
                            # so '/' is a valid character for the folder (path).
                            mSession = re.search('[\\|\\:\\*\\?\\\\"\\<\\>]', strFolder)
                            if mSession:
                                bSaveSession = False
                                g_strErrors = ("\n" +
                                    "Error: Invalid characters in folder \"{0:s}\" specified on line #{1:04d}: {2:s}{3:s}".format(
                                        strFolder, nLine, strLine, g_strErrors))
                            else:
                                strFolder = strFolderOrig

                        elif strFieldLabel == "description":
                            strDescription = vSessionInfo[nFieldIndex].strip()
                            if strDescription == "":
                                g_strErrors = ("\n" +
                                    "Warning: 'description' field on line #{0:04d} is empty: {1:s}{2:s}".format(
                                        nLine, strLine, g_strErrors))
                            else:
                                strDescription = strDescription.replace("\\r", "\r")

                        else:
                            # If there is an entry that the script is not set to use
                            # in strFieldDesignations, stop the script and display a
                            # message
                            strMsg1 = "Error: Unknown field designation: {0:s}\n\tSupported fields are as follows:\n\n\t{1:s}\n\nFor a description of the supported fields, see the comments in the sample script file.".format(g_strFieldsArray[nFieldIndex], g_strSupportedFields)

                            if g_strErrors.strip() <> "":
                                strMsg1 = (strMsg1 + "\n\n" +
                                    "Other errors found so far include: " +
                                    g_strErrors)
                            MsgBox(strMsg1, "Import Data To SecureCRT Sessions: Data File Error")
                            return
                    if bSaveSession:
                        # Use hostname if a session_name field wasn't present
                        if strSessionName == "":
                            strSessionName = strHostName

                        # Canonicalize the path to the session, as needed
                        strSessionPath = strSessionName
                        if strFolder != "":
                            strSessionPath = strFolder + "/" + strSessionName

                        # Strip any leading '/' characters from the session path
                        strSessionPath = strSessionPath.strip('/')

                        if SessionExists(strSessionPath):
                            if not g_bOverwriteExistingSessions:
                                # Append a unique tag to the session name, if it already exists
                                strSessionPath = "{0:s}(import_({1:s})".format(strSessionPath, g_strDateTimeTag)

                        #MsgBox(
                        #    "Line #{0}: {1}\nbSaveSession: {2}\nSessionPath: {3}\n\nPort: {4}\nProtocol: {5}\nHostname: {6}\nUsername: {7}\nEmulation: {8}\nFolder: {9}\nDescription: {10}\n\n{11}".format(
                        #        nLine, strLine, bSaveSession, strSessionPath, strPort, strProtocol, strHostName, strUserName, strEmulation, strFolder, strDescription, g_strErrors))

                        # Now: Create the session.
                        # ===================================================================
                        # Copy the default session settings into new session name and set the
                        # protocol.  Setting protocol protocol is essential since some variables
                        # within a config are only available with certain protocols.  For example,
                        # a telnet configuration will not be allowed to set any port forwarding
                        # settings since port forwarding settings are specific to SSH.
                        objConfig = crt.OpenSessionConfiguration("Default")
                        objConfig.SetOption("Protocol Name", strProtocol)

                        # We opened a default session & changed the protocol, now we save the
                        # config to the new session path:
                        objConfig.Save(strSessionPath)

                        # Now, let's open the new session configuration we've saved, and set
                        # up the various parameters that were specified in the file.
                        objConfig = crt.OpenSessionConfiguration(strSessionPath)
                        if objConfig.GetOption("Protocol Name") != strProtocol:
                            MsgBox("Error: Protocol not set. Expected \"{0}\", but got \"{1}\"".format(strProtocol, objConfig.GetOption("Procotol Name")))
                            return

                        if strDescription != "":
                            vDescription = strDescription.split("\r")
                            objConfig.SetOption("Description", vDescription)

                        objConfig.SetOption("Emulation", strEmulation)

                        if strProtocol.lower() <> "serial":
                            if strHostName != "":
                                objConfig.SetOption("Hostname", strHostName)

                            if strUserName != "":
                                objConfig.SetOption("Username", strUserName)

                        if strProtocol.upper() == "SSH2":
                            if strPort == "":
                                strPort = 22
                            objConfig.SetOption("[SSH2] Port", int(strPort))
                        elif strProtocol.upper() == "SSH1":
                            if strPort == "":
                                strPort = "22"
                            objConfig.SetOption("[SSH1] Port", int(strPort))
                        elif strProtocol.upper() == "TELNET":
                            if strPort == "":
                                strPort = "23"
                            objConfig.SetOption("Port", int(strPort))


                        # If you would like ANSI Color enabled for all imported sessions (regardless
                        # of value in Default session, remove comment from following line)
                        # ---------------------------------------------------------------------------
                        objConfig.SetOption("ANSI Color", True)

                        # Add other "SetOption" calls desired here...
                        # ---------------------------------------------------------------------------
                        objConfig.SetOption("Auto Reconnect", False)
                        objConfig.SetOption("Color Scheme", "Traditional")
                        objConfig.SetOption("Color Scheme Overrides Ansi Color", True)
                        objConfig.SetOption("Copy to clipboard as RTF and plain text", True)
                        objConfig.SetOption("Line Send Delay", 15)
                        #objConfig.SetOption("Log Filename V2", "${VDS_USER_DATA_PATH}\_ScrtLog(%S)_%Y%M%D_%h%m%s.%t.txt")
                        objConfig.SetOption("Rows", 60)
                        objConfig.SetOption("Cols", 140)
                        objConfig.SetOption("Use Word Delimiter Chars", True)
                        #objConfig.SetOption("Word Delimiter Chars", " <>()+=$%!#*")
                        objConfig.SetOption("Word Delimiter Chars", " ~!@#$%^&()[]{}+=:;>,\|")
                        objConfig.SetOption("Use Position", True)
                        objConfig.SetOption("X Position", 100)
                        objConfig.SetOption("Y Position", 50)

                        objConfig.Save()

                        if g_strSessionsCreated <> "":
                            g_strSessionsCreated = g_strSessionsCreated + "\n"

                        g_strSessionsCreated = g_strSessionsCreated + "    " + strSessionPath
                        g_nSessionsCreated += 1

            # Reset all variables in preparation for reading in the next line of
            # the hosts info file.
            strEmulation = ""
            strPort = ""
            strHostName = ""
            strFolder = ""
            strUserName = ""
            strSessionName = ""
            strDescription = ""
            nDescriptionLineCount = 0
            g_nDataLines += 1

    nTimeElapsed = time.time() - nStartTime
    strResults = "Import operation completed in %2.3f seconds." % (nTimeElapsed)

    if g_nSessionsCreated > 0:
        strResults = (strResults + "\n" +
            "-" * 70 + "\n" +
            "Number of Sessions created: %d\n" % (g_nSessionsCreated))
    else:
        strResults = (strResults + "\n" +
            "-" * 70 + "\n" +
            "No sessions were created from %d lines of data." % (g_nDataLines))

    crt.Session.SetStatusText("Import operation completed in {0:2.3f} seconds".format(nTimeElapsed))

    # Log activity information to a file for debugging purposes...
    strFilename = "{0}/__SecureCRT-Session-ImportLog-{1}.txt".format(g_strMyDocs, g_strDateTimeTag)
    if g_strErrors == "":
        strResults = (
            "No errors/warnings encountered from the import operation.\n\n{0:s}".format(strResults))
    else:
        strResults = "Errors/warnings from this operation include:{0}\n{1}\n{2}\n\n".format(
            g_strErrors, "-" * 70, strResults)

    objFile = open(strFilename, "w")
    objFile.write(strResults)
    objFile.close()


    # Display the log file as an indication that the information has been
    # imported.
    OpenPathInDefaultApp(strFilename)

    crt.Screen.SendSpecial("MENU_TOGGLE_SESSION_MANAGER")

    crt.Sleep(2000)
    crt.Session.SetStatusText("")

Import()
