import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    REQUIREMENTS = list(open("requirements.txt").read().splitlines())
except IOError:
    REQUIREMENTS = []

setuptools.setup(
    name="logger-bot",  # Replace with your own username
    version="0.0.1",
    author="Salim Fadhley",
    author_email="salimfadhley@gmaio.com",
    description="A telegram logger bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=REQUIREMENTS,
    entry_points={"console_scripts": ["run_client=sneaky_client.start:start"]},
)
