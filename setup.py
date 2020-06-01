import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dict-to-gql-EliyahuBasa",
    version="0.0.1",
    author="Eliyahu Basa",
    author_email="eliyaoo32@gmail.com",
    description="A simple graphql query builder from json/dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliyaoo32/dict_to_graphql",
    packages=setuptools.find_packages(),
    classifiers=[
        "JSON to Graphql Query",
        "Graphql Query",
        "Graphql Client Query"
    ],
    python_requires='>=3.5',
)
