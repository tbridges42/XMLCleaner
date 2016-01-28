import unittest
from xml_set import XmlSetBase
from xml_set import XmlSet


class TestXmlSet(unittest.TestCase):
    def test_create_xml_set(self):
        xml_set = XmlSet()
        self.assertIsNotNone(xml_set)
        self.assertIsInstance(xml_set, XmlSet)
        self.assertEquals("tag", xml_set.root_tag)
        self.assertEquals(None, xml_set.text)
        self.assertEquals(set(), xml_set.children)
        self.assertEquals({}, xml_set.attributes)

    def test_create_xml_set_base(self):
        xml_set_base = XmlSetBase()
        self.assertIsNotNone(xml_set_base)
        xml_set = xml_set_base.root
        self.assertIsNotNone(xml_set)
        self.assertIsInstance(xml_set, XmlSet)
        self.assertEquals("tag", xml_set.root_tag)
        self.assertEquals(None, xml_set.text)
        self.assertEquals(set(), xml_set.children)
        self.assertEquals({}, xml_set.attributes)

    def test_hash_not_zero(self):
        xml_set = XmlSet()
        xml_hash = xml_set.__hash__()
        self.assertNotEquals(0, xml_hash)

    def test_empty_xmls_are_equal(self):
        xml_set1 = XmlSet()
        xml_set2 = XmlSet()
        self.assertEquals(xml_set1, xml_set2)

    def test_basic_xmls_are_equal(self):
        xml_set1 = XmlSet()
        xml_set1.text = "Test"
        xml_set2 = XmlSet()
        xml_set2.text = "Test"
        self.assertEquals(xml_set1, xml_set2)

    def test_basic_xmls_are_not_equal(self):
        xml_set1 = XmlSet()
        xml_set1.text = "Test"
        xml_set2 = XmlSet()
        xml_set2.text = "wrong"
        self.assertNotEquals(xml_set1, xml_set2)

    def test_nested_xmls_are_equal(self):
        xml_set_child = XmlSet()
        xml_set_parent1 = XmlSet()
        xml_set_parent2 = XmlSet()
        xml_set_parent1.children.add(xml_set_child)
        xml_set_parent2.children.add(xml_set_child)
        self.assertEquals(xml_set_parent2, xml_set_parent1)

    def test_nested_xmls_not_equal(self):
        xml_set_child = XmlSet()
        xml_set_parent1 = XmlSet()
        xml_set_parent2 = XmlSet()
        xml_set_parent1.children.add(xml_set_child)
        xml_set_child.text = "Wrong"
        xml_set_parent2.children.add(xml_set_child)
        self.assertNotEquals(xml_set_parent2, xml_set_parent1)

    def test_duplicate_children_blocked(self):
        xml_set_child = XmlSet()
        xml_set_parent1 = XmlSet()
        xml_set_parent2 = XmlSet()
        xml_set_parent1.children.add(xml_set_child)
        xml_set_parent1.children.add(xml_set_child)
        xml_set_parent1.children.add(xml_set_child)
        xml_set_parent2.children.add(xml_set_child)
        self.assertEquals(xml_set_parent2, xml_set_parent1)

    # TODO: Test pretty print
    # TODO: Test to_set
    # TODO: Test parse


if __name__ == '__main__':
    unittest.main()
