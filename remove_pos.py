import shutil
import os
import my_xml
from os import walk


# get all files to be tested
def get_test_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (filename) in filenames:
            if filename.endswith('.xml'):
                files.append(filename)
        break
    return files


def main():
    files = get_test_files()
    for file in files:
        xml = my_xml.from_file(file)
        purchases = xml.findall("Purchase")
        pos = set()
        for purchase in purchases:
            po = my_xml.get_value(purchase, "PurchaseOrderNumber")
            if po in pos:
                xml.getroot().remove(purchase)
            else:
                pos.add(po)
        my_xml.print_as_xml(my_xml.to_set(purchases), "clean-" + file, "wb")


if __name__ == "__main__":
    main()
