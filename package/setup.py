import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# https://stackoverflow.com/questions/54430694/python-setup-py-how-to-get-find-packages-to-identify-packages-in-subdirectori
setuptools.setup(
    name="limes-inventory",
	version="0.5.0.dev",
    author="Tony Liu",
    author_email="contacttonyliu@gmail.com",
    description="limes distributed inventory interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tony-xy-Liu/Limes",
    project_urls={
        "Bug Tracker": "https://github.com/Tony-xy-Liu/Limes/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    # package_data={
    #     # "":["*.txt"],
    #     # "package-name": ["*.txt"],
    #     "test_package": ["res/*.txt"],
    # },
    python_requires=">=3.9",
)