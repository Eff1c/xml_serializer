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

Get 

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
