import shutil
import os
import my_xml
from os import walk
from tqdm import tqdm


# Get all files in current directory that end in .xml
def get_xml_files(directoryname):
    files = []
    for (dirpath, dirnames, filenames) in walk(directoryname):
        for (currentfile) in filenames:
            if currentfile.endswith('.xml'):
                files.append(dirpath + os.sep + currentfile)
        break
    return files


# get all files to be tested
def get_test_files(directory):
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for (filename) in filenames:
            if filename.endswith('.xml'):
                files.append(filename)
        break
    return files


# build a canonical set of all xml files in directory and write to a canon file
def build_canon(directory):
    elements = set()
    for (filename) in get_xml_files(directory):
        elements |= my_xml.to_set(my_xml.from_file(filename))
    if elements != set():
        my_xml.print_as_xml(elements, get_canon_path(directory), 'wb')


# remove duplicates from a set of records based on a canonical history of past records
# the returned tuple will contain an set containing all the unique elements of xml that are not in canon
# and a set containing all the elements of canon with the new unique elements of xml appended
def remove_duplicates(xml_set, canon):
    output = set()
    output |= xml_set
    canon |= output
    return output, canon


# create a file of only unique records
def create_upload_file(directory, filename):
    xml = my_xml.from_file(filename)
    canon = set()
    if os.path.isfile(get_canon_path(directory)):
        canon |= my_xml.to_set(my_xml.from_file(get_canon_path(directory)))
    output, canon = remove_duplicates(my_xml.to_set(xml), canon)
    my_xml.print_as_xml(output, get_output_path(filename), 'wb')
    my_xml.print_as_xml(canon, get_canon_path(directory), 'wb')


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


def clean(directory):
    total_size = 0
    files = get_test_files(directory)
    for file in files:
        total_size = total_size + os.path.getsize(file)
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Cleaning files') as progress_bar:
        for (filename) in get_test_files():
            if filename.startswith('upload-'):
                continue
            agency = get_agency_name(filename)
            # if the agency has not previously been encountered, create a directory for it
            if not (os.path.isdir(agency)):
                os.mkdir(agency)
            # if there is no canon file for the agency, create one
            if not (os.path.isfile(get_canon_path(agency))):
                build_canon(agency)
            if not (os.path.isfile(get_output_path(filename))):
                create_upload_file(agency, filename)
            progress_bar.update(os.path.getsize(filename))
            if not (os.path.isfile(agency + os.sep + filename)):
                shutil.move(filename, agency)
            else:
                os.remove(filename)


def main():
    clean(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    main()
