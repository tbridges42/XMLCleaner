import xml.etree.ElementTree as ET


# TODO: Switch to xml_set
# TODO: Implement auto-download
# TODO: Implement custom source/destination
# TODO: Incorporate merge


def normalize_record(element):
    element_string = ET.tostring(element, method='html')
    element_string = element_string.strip()
    element_string = element_string.replace(b'\t', b'  ')
    return element_string


# convert an xml tree of 'Purchase' to a set of records
def to_set(xml):
    try:
        xml_set = xml.getroot().findall('Purchase')
    except AttributeError:
        xml_set = set()
    norm_set = set()
    purchase_orders = set()
    for element in xml_set:
        try:
            purchase_order = (element.find("PurchaseOrderNumber").text, element.find("SpecificValue").text)
            if purchase_order not in purchase_orders:
                norm_set.add(normalize_record(element))
                purchase_orders.add(purchase_order)
        except AttributeError:
            norm_set.add(normalize_record(element))
    return norm_set


# print a set of elements as a flat xml to filename
def print_as_xml(elements, filename, mode):
    f = open(filename, mode)
    f.write(b'<?xml version="1.0"?>\n<Purchases>\n')
    for (element) in elements:
        f.write(b'    ')
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
        return None


def get_value(root, attribute):
    element = root.find(attribute)
    if element is not None:
        return root.find(attribute).text
    else:
        return None

