import os
import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    REQUIREMENTS = list(open("requirements.txt").read().splitlines())
except IOError:
    REQUIREMENTS = []

VERSIONFILE: str = os.path.join(os.getcwd(), "./src/sneaky_client/_version.py")
VSRE: str = r"^__version__\:\s*str\s*=\s*['\"]([0-9\.]+)['\"]"

try:
    VERSION_TEXT: str = open(VERSIONFILE, "rt").read()
except OSError:
    raise RuntimeError(f"Cannot read version from {VERSIONFILE}")

mo = re.search(VSRE, VERSION_TEXT, re.M)
if mo:
    VERSION: str = mo.group(1)
else:
    raise RuntimeError(f"Cannot grep version from text: {VERSION_TEXT}")


setuptools.setup(
    name="sneaky-client",  # Replace with your own username
    version=VERSION,
    author="Salim Fadhley",
    author_email="salimfadhley@gmaio.com",
    description="Multi-network logging framework",
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
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": ["run_telegram_client=sneaky_client.telegram_client:start"]
    },
)
