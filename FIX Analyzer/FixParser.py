import re
import clr

clr.AddReference('System.Xml')

from System import Object
from System.Xml import XmlReader, XmlNodeType

def get_messages_from_text(input):
	msg_list = re.findall('(8=FIX.+?\x01.*?\x0110=\d+\x01)', input)
	return [translate_message_to_list(msg) for msg in msg_list]

def translate_message_to_list(msg):
	tag_list = [match.group(1) for match in re.finditer('(?=\x01(\d+=.*?)\x01)', '\x01' + msg)]
	tag_key_value_list = []
	for tag in tag_list:
		match = re.search('(\d+)=(.*)', tag)
		if match:
			tag_names = get_fix_names(match.group(1), match.group(2))
			tag_key_value_list.append(NamedFixTag(match.group(1), match.group(2), tag_names[0], tag_names[1]))

	return tag_key_value_list

def get_fix_names(tag, value):
	tag_name = ""
	value_name = ""
	reader = XmlReader.Create('FixDict.xml')
	while reader.ReadToFollowing("field"):
		if tag == reader.GetAttribute("number"):
			tag_name = reader.GetAttribute("name")
			subtree = reader.ReadSubtree()
			while subtree.ReadToFollowing("value"):
				if value == subtree.GetAttribute("enum"):
					value_name = subtree.GetAttribute("description")
					break
			break

	reader.Dispose()
	return tag_name, value_name

class FixTag(object):
	def __init__(self, tag, value):
		self.tag = tag
		self.value = value

	@property
	def Tag(self):
		return self.tag

	@Tag.setter
	def Tag(self, value):
		self.tag = value

	@property
	def Value(self):
		return self.value

	@Value.setter
	def Value(self, value):
		self.value = value

class NamedFixTag(FixTag):
	def __init__(self, tag, value, tag_name, value_name):
		FixTag.__init__(self, tag, value)
		self.tag_name = tag_name
		self.value_name = value_name

	@property
	def TagName(self):
		return self.tag_name

	@TagName.setter
	def TagName(self, value):
		self.tag_name = value

	@property
	def ValueName(self):
		return self.value_name

	@ValueName.setter
	def ValueName(self, value):
		self.value_name = value