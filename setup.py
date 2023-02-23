from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='xml_serializer',
    author='Illia Martyniuk',
    author_email="illymartynyk@gmail.com",
    version="1.0.3",
    url='https://github.com/Eff1c/xml_serializer',
    license='MIT',
    description='Module for serialize (convert) xml to Python dict (with Python objects)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['xml_serializer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
