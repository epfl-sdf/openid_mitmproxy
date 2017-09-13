# Emulation d'un serveur Tequila via un serveur OpenID
# Petit Hello World pour convertir un wget cookie en html cookie
# 170913.1247

import re
import os
import sys
import getopt
import time
import select


class Filter:

    Domain = "tequila.epfl.ch"
    DefaultPath = "/"

    handler = open("data/cookies/cookiezvdf0h2c3mzvo8h1s827mg2v7fvxf7nx", "r")
    zcookie = handler.read()
    handler.close()
    listOfCookies = zcookie.split("\n")
    parsedCookies = ""

    for Cookie in listOfCookies:
        Parse = ""
        Parse = re.findall("([A-za-z._-]+)([ /\\t]+)(TRUE|FALSE)([ /\\t]+)(TRUE|FALSE)([ /\\t]+)([0-9]+)([ /\\t]+)(.*)([ /\\t]+)(.*)", Cookie)

        if len(Parse) != 1:
            continue

        ParsedLen = len(Parse[0])
        # validate cookie
        if ParsedLen == 10 or ParsedLen == 11:
            if ParsedLen == 10: # if cookie has no value
                parsedCookies += Parse[0][8]+"=; "
            else:
                parsedCookies += Parse[0][8]+"="+Parse[0][10]+"; "

    parsedCookies += "path="+DefaultPath+"; domain="+Domain+";"

    print(parsedCookies)

def start():
    return Filter()
