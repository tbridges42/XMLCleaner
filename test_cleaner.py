import unittest
import cleaner
import os
import shutil
import xml.etree.ElementTree as ET


class TestCleaner(unittest.TestCase):

    def test_get_agency_name(self):
        result = cleaner.get_agency_name('some-stuff-with-name-of-agency.xml')
        self.assertEquals(result, 'agency')

    def test_get_agency_name_85(self):
        result = cleaner.get_agency_name('some-stuff-with-name-of-agency-85.xml')
        self.assertEquals(result, 'agency')

    def equal_xml(self, gold, test):
        xml_gold_list = list(gold.getroot().iter())
        xml_test_list = list(test.getroot().iter())
        self.assertEquals(len(xml_gold_list), len(xml_test_list))
        string_gold_list = []
        string_test_list = []
        for i in range(1, len(xml_gold_list)):
            string_gold_list.append(ET.tostring(xml_gold_list[i]).strip())
            string_test_list.append(ET.tostring(xml_test_list[i]).strip())
        for i in range(0, len(string_gold_list)):
            self.assertTrue(string_gold_list[i] in string_test_list, str(i) + ': ' + str(string_gold_list[i]))

    def reset(self):
        if os.path.isfile('upload-xml-test.xml'):
            os.remove('upload-xml-test.xml')
        if os.path.isfile('test' + os.sep + 'xml-test.xml') and not(os.path.isfile('xml-test.xml')):
            shutil.move('test' + os.sep + 'xml-test.xml', os.getcwd())
        if os.path.isdir('test'):
            shutil.rmtree('test')

  #  def test_add_to_set_unique(self):

    # TODO: Fix this
    # def test_duplicate_xml(self):
    #     test_root = ET.Element("Purchases")
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A unique purchase"
    #     for i in range(0, 4):
    #         purchase = ET.SubElement(test_root, "Purchase")
    #         ET.SubElement(purchase, "Description").text = "A duplicate purchase"
    #     for i in range(0, 4):
    #         purchase = ET.SubElement(test_root, "Purchase")
    #         ET.SubElement(purchase, "Description").text = "A complicated duplicate purchase"
    #         ET.SubElement(purchase, "ExactValue").text = "15651231.54"
    #         ET.SubElement(purchase, "NIGPCode").text = "94511"
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A unique purchase in canon"
    #     for i in range(0, 4):
    #         purchase = ET.SubElement(test_root, "Purchase")
    #         ET.SubElement(purchase, "Description").text = "A complicated duplicate purchase in canon"
    #         ET.SubElement(purchase, "ExactValue").text = "15651231.54"
    #         ET.SubElement(purchase, "NIGPCode").text = "94511"
    #     test = ET.ElementTree(test_root)
    #
    #     canon_root = ET.Element("Purchases")
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A unique purchase in canon"
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A complicated duplicate purchase in canon"
    #     ET.SubElement(purchase, "ExactValue").text = "15651231.54"
    #     ET.SubElement(purchase, "NIGPCode").text = "94511"
    #     canon = ET.ElementTree(canon_root)
    #
    #     gold_root = ET.Element("Purchases")
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A unique purchase"
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A duplicate purchase"
    #     purchase = ET.SubElement(test_root, "Purchase")
    #     ET.SubElement(purchase, "Description").text = "A complicated duplicate purchase"
    #     ET.SubElement(purchase, "ExactValue").text = "15651231.54"
    #     ET.SubElement(purchase, "NIGPCode").text = "94511"
    #     gold = ET.ElementTree(gold_root)
    #
    #     self.equal_xml(cleaner.remove_duplicates(test, canon), gold)

    def test_cleaner(self):
        self.reset()
        cleaner.main()
        self.equal_xml(cleaner.to_xml('upload-gold.xml'), cleaner.to_xml('upload-xml-test.xml'))

if __name__ == '__main__':
    unittest.main()
