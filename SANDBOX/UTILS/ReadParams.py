import re  # python regular expressions


class ReadParams:

    def __init__(self, filename):
        ffile = open(filename, 'r')
        next(ffile)  # skip header line
        next(ffile)  # skip header line

        iinput = []
        for line in ffile:
            prsvalue = re.search(r'\[(.*)\]', line).group(1)  # parse out values from square brackets
            iinput.append(prsvalue)
        ffile.close()

        self.iinput = iinput

    def getParam(self, param):
        match = [s for s in self.iinput if param in s]  # choose only lists identified by param
        scanIdDisp = match[0].split(",")[2]
        plabel = match[1].split(",")[2]

        return {'scanIdDisp': int(scanIdDisp), 'plabel': plabel}
