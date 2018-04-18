import xml.etree.ElementTree
e = xml.etree.ElementTree.parse("Maps/grasslands.tmx").getroot()
for child in e:
	print(child.tag,child.attrib)