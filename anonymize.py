import logging
import os
import random
import generate
import configHandler
import tokenizer


# Function to split a fixed width line up based on a config object
def splitFixedWidth(line, c):
    f = []
    i = 0
    for w in c.getChunkSizes():
        log.debug(
            "Split [" + line + "] column from start [" + str(i) + "] width " + str(w) + " = [" + line[i:(i + w)] + "]")
        f.append(line[i:(i + w)])
        i = i + w
    return f


# TODO: replace log with a wrapper to standardise log formats and include timestamp + metadata
# TODO: default to warning unless -v or -verbose flag (in which case INFO)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("anonymize")

# TODO: convert to pass these as parameters
configFile = "./samples/customer.cf"
sourceFile = "./samples/customer.csv"
# configFile = "./samples/accounts.cf"
# sourceFile = "./samples/accounts.dat"

outputFile = "./output/" + sourceFile.split('/')[-1]

c = configHandler.ConfigHandler(configFile)
tokenisers = {}
for cfield in c.config['fields']:
    if cfield['mode'] == "token":
        name = cfield['name']
        tokenisers[name] = tokenizer.Tokenizer('./mapping/' + name + ".map")

if 'delimiter' not in c.config:
    delim = ""
else:
    delim = c.config['delimiter']

# Process source file line by line and output to 
with open(sourceFile) as source:
    output = open(outputFile, "w")
    line = source.readline().strip()

    # If the config denotes a header then output the first line directly to the output file and read another line
    if c.config['header']:
        output.writelines(line + "\n")
        line = source.readline().strip()

    while line:
        log.info("Input line :[" + line + "]")
        outline = None
        fieldIndex = 0

        # Split up input string
        if delim == "":
            # TODO get fields based on fixed split
            fields = splitFixedWidth(line, c)
        else:
            fields = line.split(delim)

        # Process and anonymise each field
        for field in fields:
            log.debug(".Read:[" + field + "]")
            cfield = c.config['fields'][fieldIndex]

            newValue = ""

            if cfield['presentRatio'] >= random.random():
                if cfield['mode'] == 'original':
                    log.debug("..Keeping value unchanged")
                    newValue = field
                elif cfield['mode'] == 'random':
                    log.debug("..Generate random value regex[" + cfield['regEx'] + "]")
                    newValue = generate.generate(cfield['regEx'])
                elif cfield['mode'] == 'token':
                    log.debug("..Searching for token [" + field + "]")
                    t = tokenisers[cfield['name']].getToken(field)
                    if t == "":
                        t = generate.generate(cfield['regEx'])
                        tokenisers[cfield['name']].storeToken(field, t)
                    newValue = t

            if delim == "":
                newValue = newValue.rjust(cfield['width'], ' ')
                if outline is None:
                    outline = ""

                outline = outline + newValue
            else:
                if outline is not None:
                    outline = outline + delim + newValue
                else:
                    outline = newValue

            fieldIndex += 1

        log.info("Output line:[" + outline + "]")
        output.writelines(outline + "\n")
        line = source.readline().strip()
