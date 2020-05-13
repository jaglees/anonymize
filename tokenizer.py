
class Tokenizer:
    t = { }
    tokenFileUrl=""
    def __init__(self, tokenfile):
        self.tokenFileUrl=tokenfile
        # read from disk to dictionary
        try:
            with open (tokenfile) as source:
                line = source.readline().strip()
                while line:
                    fields = line.split(',')
                    self.t[fields[0]] = fields[1]
                    line = source.readline().strip()

        except IOError:
            print("File doesn't exist")
        print("Loaded "+str(len(self.t))+" records")

    def getToken(self, origional):
        r=""
        if origional in self.t:
            r=self.t[origional]
        
        return r

    def storeToken(self, origional, token):
        self.t[origional] = token
        with open(self.tokenFileUrl, "a") as output:
            output.writelines(origional+","+token+"\n")
