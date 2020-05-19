import os


class Tokenizer:
    t = {}
    tokenFileUrl = ""

    def __init__(self, tokenfile):
        self.tokenFileUrl = tokenfile

        if not os.path.isfile(tokenfile):
            print(f"Tokenizer store file ({tokenfile}) doesn't exist. Creating.")
            os.makedirs(os.path.dirname(tokenfile), exist_ok=True)
            open(tokenfile, 'w').close()

        # read from disk to dictionary
        try:
            with open(tokenfile) as source:
                line = source.readline().strip()
                while line:
                    fields = line.split(',')
                    self.t[fields[0]] = fields[1]
                    line = source.readline().strip()

        except IOError:
            print("File doesn't exist")
        print("Loaded " + str(len(self.t)) + " records")

    def getToken(self, original):
        r = ""
        if original in self.t:
            r = self.t[original]

        return r

    def storeToken(self, original, token):
        self.t[original] = token
        with open(self.tokenFileUrl, "a") as output:
            output.writelines(original + "," + token + "\n")
