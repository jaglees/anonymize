import logging
import os
import random
import generate
import configHandler

def splitFixedWidth(line, c):
    f=[]
    i=0
    for w in c.getChunkSizes():
        log.debug("Split ["+line+"] column width "+str(w)+" = ["+line[i:w]+"]")
        f.append(line[i:w])
        i=i+w
    return f

# TODO: replace log with a wrapper to standardise log formats and include timestamp + metadata
logging.basicConfig(level=logging.INFO)
log=logging.getLogger("anonymize")

# TODO: convert to pass these as parameters
# configFile = "./samples/customer.cf"
# sourceFile = "./samples/customer.csv"
configFile = "./samples/accounts.cf"
sourceFile = "./samples/accounts.dat"

outputFile= "./output/"+ sourceFile.split('/')[-1]

c = configHandler.ConfigHandler(configFile)

if ('delimiter' not in c.config):
    delim=""
else:
    delim=c.config['delimiter']

# Process source file line by line and output to 
with open (sourceFile) as source:
    output= open(outputFile, "w")
    line = source.readline().strip()

    # If the config denotes a header then output the first line directly to the output file and read another line
    if (c.config['header']):
        output.writelines(line+"\n")
        line = source.readline().strip()

    while line:
        log.info("Input line :["+line+"]")
        outline=None
        fieldIndex=0

        # Split up input string
        if (delim==""):
            # TODO get fields based on fixed split
            fields=splitFixedWidth(line,c)
        else:
            fields=line.split(delim)

        # Process and anonymise each field
        for field in fields:
            log.debug(".Read:["+field+"]")
            cfield = c.config['fields'][fieldIndex]

            newValue=""

            if (cfield['presentRatio'] >= random.random()):
                if (cfield['mode'] == 'origional'):
                    log.debug("..Keeping value unchanged")
                    newValue = field
                elif (cfield['mode'] == 'random'):
                    log.debug("..Generate random value regex["+cfield['regEx']+"]")
                    newValue = generate.generate(cfield['regEx'])
                elif (cfield['mode'] == 'token'):
                    log.debug('..Searching for token')
                    # t = getToken( field )
                    # if (t = ""):
                    t = generate.generate(cfield['regEx'])
                    #   storeToken (field, token)
                    newValue=t

            if delim=="":
                newValue = newValue.rjust(cfield['width'],' ')
                if outline==None:
                    outline=""

                outline=outline+newValue
            else:
                if outline!=None: 
                    outline=outline+","+newValue
                else:
                    outline=newValue
            
            fieldIndex+=1

        log.info("Output line:["+outline+"]")
        output.writelines(outline+"\n")
        line = source.readline().strip()