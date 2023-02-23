# XML Serializer

Allows you to convert XML to python dict (with python objects) using a schema.

## Examples

You can see examples of using the module in [serializer_test.py](test/serializer_test.py)

We have next xml data (profiles.xml)

```xml
<payload>
    <MyProfile>
        <record id="1" nickname="eff1c" admin="true">
            <posts topic="something">
                <post name="test post" description="It's my test post." />
                <post name="python xml_serializer" description="It's very useful module!" />
            </posts>
        </record>
    </MyProfile>
</payload>
```

And we want to turn it into

```python
{
    "payload": {
        "my_profile": {
            "record": {
                "id": 1,
                "nickname": "eff1c",
                "admin": True,
                "posts": {
                    "topic": "something",
                    "post": [
                        {"name": "test post", "description": "It's my test post."},
                        {
                            "name": "python xml_serializer",
                            "description": "It's very useful module!",
                        },
                    ],
                },
            }
        }
    }
}
```

We will write next schema

```python
from xml_serializer import Tag, TagAttr
from xml_serializer.converter_types import Integer, String, Boolean

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
```

Get etree element (tag)

```python
from xml.etree import ElementTree as etree

tree = etree.parse("profiles.xml")
root = tree.getroot()

# you can use root tag or find any else
main_tag = root.find("payload")
```

And call the method to pass them to

```python
from xml_serializer import xml_serialize

response = xml_serialize(profiles_schema, main_tag)
```

## Schema

### Tag/TagAttr
In order to serialize data, you need to describe the scheme of its structure.  
To do this, we create a python dict with Tag/TagAttr object keys.  
The value for Tag is a set of TagAttr-s or Tag.
I think it's clear that TagAttr is an attribute of the current tag, and Tag is actually a nested tag.

```python
from xml_serializer import Tag, TagAttr
from xml_serializer.converter_types import String

schema = {
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
```

Both Tag and TagAttr have 2 parameters: field_name and name.  
`field_name` - it is name in xml.  
`name` - it is our custom name with which the object will return to us after serialization (**by default** - field_name).

### Field data types

To convert TagAttr values, we use data types: **String**, **Integer**, **Float**, **Boolean**, **NestedType**.  

**String**, **Integer**, **Float**, **Boolean** are similar to common data types (as in python).
All of them have the `nullable` parameter (**True** by default).  
When set to **False**, if the tag does not have this attribute in the input data, an error will be raised

#### NestedType

It is a data type that allows you to intercept serialization in the middle of a schema and
process the resulting data according to your needs.

In order to use it, we have to describe the nested schema separately
and create a function that will process the data received from it.  
NestedType has 2 attributes for it: `schema` and `data_handling_function`

```python
from xml_serializer import Tag, TagAttr
from xml_serializer.converter_types import Boolean, String, NestedType


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


schema_with_nesting = {
    Tag("record"): {
        TagAttr("admin"): Boolean(),
        Tag("posts", "post_names"): NestedType(posts_schema, get_post_names)
    }
}
```

In this example, we return only a list of post-s names to the posts tag, discarding all the information we don't need.
This way, NestedType allows you to modify the output data schema without unnecessary iterations.

#### Custom type

You can create your own field data types. Use `AbstractType` for it.

```python
from xml_serializer.abstract_type import AbstractType

class Boolean(AbstractType):
    def convert_method(self, value):
        return True if value.lower() == "true" else False
```