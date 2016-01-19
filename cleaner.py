import xml.etree.ElementTree as ET
import shutil
import os
from os import walk


# Get all files in current directory that end in .xml
def get_xml_files(directoryname):
    files = []
    for (dirpath, dirnames, filenames) in walk(directoryname):
        for (currentfile) in filenames:
            if currentfile.endswith('.xml'):
                files.append(dirpath + os.sep + currentfile)
        break
    return files


# Get the current working folder
def get_working_folder():
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (dirname) in dirnames:
            return dirname


# return an xml tree from filename
def to_xml(filename):
    try:
        return ET.parse(filename)
    except ET.ParseError as err:
            print('Malformed xml: ' + filename + str(err.position))


# return a set of unique elements in xml tree
def add_to_set(elements, xml):
    for (element) in xml.getroot().findall('Purchase'):
        if not(ET.tostring(element).strip() in elements):
            elements.add(ET.tostring(element).strip())


# print a set of elements as a flat xml to filename
def print_set(elements, filename, mode):
    f = open(filename, mode)
    f.write(b'<?xml version="1.0"?>\n<Purchases>\n')
    for (element) in elements:
        f.write(b'\t')
        f.write(element)
        f.write(b'\n')
    f.write(b'</Purchases>')
    f.close()


# get all files to be tested
def get_test_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (filename) in filenames:
            if filename.endswith('.xml'):
                print(filename)
                files.append(filename)
        break
    return files


# build a canonical set of all xml files in directory and write to a canon file
def build_canon(directory):
    elements = set()
    for (filename) in get_xml_files(directory):
        add_to_set(elements, to_xml(filename))
    if elements != set():
        print_set(elements, get_canon_path(directory), 'wb')


# remove duplicates from xml
# the returned tuple will contain an set containing all the unique elements of xml that are not in canon
# and a set containing all the elements of canon with the new unique elements of xml appended
def remove_duplicates(xml, canon):
    output = set()
    for (element) in xml.getroot():
        if not(ET.tostring(element).strip() in canon):
            add_to_set(output, xml)
            add_to_set(canon, xml)
        else:
            print('Duplicate found:' + str(ET.tostring(element).strip()))
    return output, canon


# create a file of only unique records
def create_upload_file(directory, filename):
    xml = to_xml(filename)
    canon = set()
    try:
        add_to_set(canon, ET.parse(get_canon_path(directory)))
    except ET.ParseError:
        print('Malformed canon: ' + filename)
        return
    except FileNotFoundError:
        print('No Canon')
    output, canon = remove_duplicates(xml, canon)
    print_set(output, get_output_path(filename), 'wb')
    print_set(canon, get_canon_path(directory), 'wb')


# build a relative path and filename for a canon file
def get_canon_path(directory):
    return directory + os.sep + directory + '-canon.xml'


def get_output_path(filename):
    return 'upload-' + filename


# given a filename matching some-random-stuff-agency.xml, return the agency name
def get_agency_name(filename):
    # the agency abbreviation is the last section of a hyphen-separated filename
    agency = filename.split('-')[-1].split('.')[0]
    # one agency has an additional "85" in the last section
    if agency == '85':
        agency = filename.split('-')[-2].split('.')[0]
    return agency


def main():
    print("Working")
    for (filename) in get_test_files():
        print(filename)
        if filename.startswith('upload-'):
            continue
        agency = get_agency_name(filename)
        # if the agency has not previously been encountered, create a directory for it
        if not (os.path.isdir(agency)):
            os.mkdir(agency)
        # if there is no canon file for the agency, create one
        if not(os.path.isfile(get_canon_path(agency))):
            build_canon(agency)
        if not(os.path.isfile(get_output_path(filename))):
            create_upload_file(agency, filename)
        if not(os.path.isfile(agency + os.sep + filename)):
            shutil.move(filename, agency)
        else:
            os.remove(filename)

if __name__ == "__main__":
    main()
