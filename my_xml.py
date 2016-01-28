import xml.etree.ElementTree as ET


# TODO: Switch to xml_set
# TODO: Implement auto-download
# TODO: Implement custom source/destination
# TODO: Incorporate merge


def normalize_record(element):
    return ET.tostring(element).strip()


# convert an xml tree of 'Purchase' to a set of records
def to_set(xml):
    xml_set = xml.getroot().findall('Purchase')
    norm_set = set()
    for element in xml_set:
        norm_set.add(normalize_record(element))
    return norm_set


# print a set of elements as a flat xml to filename
def print_as_xml(elements, filename, mode):
    f = open(filename, mode)
    f.write(b'<?xml version="1.0"?>\n<Purchases>\n')
    for (element) in elements:
        f.write(b'\t')
        f.write(element)
        f.write(b'\n')
    f.write(b'</Purchases>')
    f.close()


# return an xml tree from filename
def from_file(filename):
    try:
        return ET.parse(filename)
    except ET.ParseError as err:
        print('Malformed xml: ' + filename + str(err.position))
