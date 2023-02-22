from typing import Union
from xml.etree.ElementTree import Element as xml_tag

from .abstract_type import AbstractType


class BaseField:
    def __init__(self, field_name: str, name: str = None):
        self.field_name = field_name

        if not name:
            name = field_name

        self.name = name


class Tag(BaseField):
    """
    Describes a tag in the serialization scheme
    """
    pass


class TagAttr(BaseField):
    """
    Describes a tag attribute in the serialization scheme
    """
    pass


def xml_serialize(schema: dict, tag: xml_tag):
    """
    Serialize xml by schema

    :param schema: schema for serializing
    :param tag: etree element
    :return: serialized xml (to python dict)
    """
    response = {}

    schema_tag, inner_schema = get_schema_tag_and_inner_schema(schema)

    serialized_xml = serialize_by_inner_schema(inner_schema, tag)

    response[schema_tag.name] = serialized_xml

    return response


def serialize_by_inner_schema(schema: dict, tag: xml_tag):
    """
    Use schema without current tag.

    :param schema: schema for serializing
    :param tag: etree element
    :return: serialized xml (to python dict) without current tag
    """
    xml_element = XMLElement(schema, tag)
    response = xml_element.serialize()

    return response


def get_schema_tag_and_inner_schema(schema: dict) -> (Tag, Union[list, dict]):
    schema_items = list(schema.items())

    if len(schema_items) > 1:
        raise ValueError("You can't parse multiple tags without the root tag!")

    schema_tag = schema_items[0][0]
    inner_schema = schema_items[0][1]

    return schema_tag, inner_schema


class XMLElement:
    def __init__(self, schema: dict, tag: xml_tag) -> dict:
        self.schema = schema
        self.tag = tag

    def serialize(self):
        response = {}

        tag_descriptions, tag_attr_descriptions = self.get_field_descriptions()

        if tag_attr_descriptions:
            tag_attrs = self.fill_tag_attrs(
                tag_attr_descriptions
            )
            if tag_attrs:
                response.update(tag_attrs)

        if tag_descriptions:
            tags = self.fill_tags(
                tag_descriptions
            )
            if tags:
                response.update(tags)

        return response or None

    def get_field_descriptions(self) -> (dict, dict):
        tag_descriptions = {}
        tag_attr_descriptions = {}

        for key, value in self.schema.items():
            is_tag = isinstance(key, Tag)

            if is_tag:
                tag_descriptions[key] = value

            else:
                tag_attr_descriptions[key] = value

        return tag_descriptions, tag_attr_descriptions

    def fill_tag_attrs(self, fields_description):
        response = {}

        for key, converter_type in fields_description.items():
            value = self.tag.get(key.field_name)

            if converter_type and value:
                value = converter_type.convert(value)

            response[key.name] = value

        return response

    def fill_tags(self, fields_description: dict):
        children_tags_with_nesting = self.get_children_tags_with_nesting(
            fields_description
        )

        response = {
            key.name: None for key in fields_description
        }

        for children_tag, schema_tag in children_tags_with_nesting.items():
            current_schema_item = self.schema[schema_tag]

            item_type = fields_description[schema_tag]

            if isinstance(item_type, dict):
                response[schema_tag.name] = serialize_by_inner_schema(
                    current_schema_item,
                    children_tag
                )

            elif isinstance(item_type, list):
                self.list_serialize(
                    current_schema_item,
                    children_tag,
                    schema_tag,
                    response
                )

            elif isinstance(item_type, AbstractType):
                response[schema_tag.name] = item_type.convert_method(children_tag)

            else:
                raise TypeError("The wrong type has been set!")

        return response

    def get_children_tags_with_nesting(self, fields_description: dict):
        tag_names = {tag.field_name: tag for tag in fields_description}

        return {
            tag: tag_names[tag.tag] for tag in self.tag
            if tag.tag in tag_names
        }

    @staticmethod
    def list_serialize(
        current_schema_item: dict,
        tag: xml_tag,
        schema_tag: Tag,
        response: dict
    ):
        current_schema_item = current_schema_item[0]
        serialized_list = serialize_by_inner_schema(current_schema_item, tag)

        if not response[schema_tag.name]:
            response[schema_tag.name] = [serialized_list]
        else:
            response[schema_tag.name].append(serialized_list)
