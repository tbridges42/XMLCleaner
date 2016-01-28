import xml.etree.ElementTree as ElementTree


class XmlSet:
    def __init__(self, xml=ElementTree.Element("tag")):
        self.root_tag = xml.tag
        self.text = xml.text
        self.children = self.to_set(xml)
        self.attributes = xml.attrib

    def __eq__(self, other):
        return (self.root_tag == other.root_tag and
                self.text == other.text and
                self.attributes == other.attributes and
                self.children == other.children)

    def __hash__(self):
        result = 72
        result *= self.root_tag.__hash__()
        result *= self.text.__hash__()
        for child in self.children:
            result *= child.__hash__()
        for attribute in self.attributes:
            result *= attribute.__hash__()
        return result

    @staticmethod
    def to_set(xml):
        xml_set = set(list(xml))
        children_set = set()
        for (element) in xml_set:
            children_set.add(XmlSet(element))
        return children_set

    def pretty_print_strings(self):
        strings = ['<' + self.root_tag]
        for key, value in self.attributes.items():
            strings[0] += ' ' + key + '="' + value + '"'
        strings[0] += '>'
        if self.text:
            strings.append('\t' + self.text)
        for child in self.children:
            child_strings = child.pretty_print_strings
            for string in child_strings:
                strings.append('\t' + string)
        strings.append('</' + self.root_tag + '>')
        return strings


class XmlSetBase:
    def __init__(self, xml=ElementTree.ElementTree()):
        if xml.getroot():
            self.root = XmlSet(xml.getroot())
        else:
            self.root = XmlSet()

    @staticmethod
    def parse(source):
        return XmlSetBase(ElementTree.parse(source))

    def __eq__(self, other):
        return self.root == other.root
