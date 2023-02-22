import json
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element as xml_tag

import pytest

from xml_serializer.main import xml_serialize, Tag, TagAttr
from xml_serializer.converter_types import Integer, String, Boolean, NestedType

profiles_schema = {
    Tag("payload"): {
        Tag("MyProfile", "my_profile"): {
            Tag("record"): {
                TagAttr("id"): Integer(nullable=False),
                TagAttr("nickname"): String(nullable=False),
                TagAttr("admin"): Boolean(),
                Tag("posts"): {
                    TagAttr("topic"): String(nullable=False),
                    Tag("post"): [
                        {
                            TagAttr("name"): String(),
                            TagAttr("description"): String()
                        }
                    ]
                }
            }
        }
    }
}


posts_schema = {
    Tag("post", "posts"): [
        {
            TagAttr("name"): String(),
            TagAttr("description"): String()
        }
    ]
}


def get_post_names(data):
    posts = data["posts"]

    return [post["name"] for post in posts]


profiles_schema_with_nesting = {
    Tag("payload"): {
        Tag("MyProfile", "my_profile"): {
            Tag("record"): {
                TagAttr("id"): Integer(nullable=False),
                TagAttr("nickname"): String(nullable=False),
                TagAttr("admin"): Boolean(),
                Tag("posts", "post_names"): NestedType(posts_schema, get_post_names)
            }
        }
    }
}


def get_main_tag(file_name: str, tag_name: str = None) -> xml_tag:
    tree = etree.parse(f"test_payloads/{file_name}.xml")
    root = tree.getroot()

    if tag_name is None or root.tag == tag_name:
        return root

    tag = root.find(tag_name)

    return tag


def get_response(name: str) -> str:
    with open(f"test_responses/{name}.json", "r") as f:
        file_data = json.load(f)

    return file_data


test_data = [
    (
        profiles_schema,
        get_main_tag("profiles", "payload"),
        get_response("profiles"),
    ),
    (
        profiles_schema_with_nesting,
        get_main_tag("profiles", "payload"),
        get_response("profiles_with_nesting"),
    ),
]


@pytest.mark.parametrize('schema, main_tag, expected_response', test_data)
def test_serializer(schema: dict, main_tag, expected_response):
    response = xml_serialize(schema, main_tag)

    assert response == expected_response
