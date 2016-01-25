import my_xml
import time
import os
from os import walk


# get all files to be merged
def getunmergedfiles():
    files = []
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (filename) in filenames:
            if filename.startswith('upload') and filename.endswith('.xml'):
                files.append(filename)
        break
    return files


def main():
    agencies = {}
    for (filename) in getunmergedfiles():
        # the agency abbreviation is the last section of a hyphen-separated filename
        agency = filename.split('-')[-1].split('.')[0]
        # one agency has an additional "85" in the last section
        if agency == '85':
            agency = filename.split('-')[-2].split('.')[0]
        print(agency)
        agencyset = set()
        if agency in agencies:
            agencyset = agencies[agency]
        agencyset |= my_xml.from_file(filename)
        agencies[agency] = agencyset

    for (agency) in agencies:
        print(agency)
        my_xml.print_as_xml(agencies[agency], "upload-" + agency + "-" + time.strftime("%y%m%d") + "-merged.xml", "wb")


if __name__ == "__main__":
    main()