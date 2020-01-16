# Scanned Variant Generator


This tool converts a PDF or an image of a document into a scanned or mobile-caputured variant.

Note: This tool is an existing project developed for internal use in middle of 2018. It has since then not been updated.
I decided to make it open source since I found it quite handy.
This is my first github upload. I will follow up with more internally-developed and new projects soon!

Example:
Original

<img src="https://github.com/waleedfarrukhgini/scanned_variant_generator/blob/master/variant_generator/resources/Datev.jpg" width="200">

Mobile-captured variant

<img src="https://drive.google.com/uc?export=view&id=1pbiPP9nb1Me0KfSYY7dRzzyHXI4SrwoZ" width="200"> 

## Installation

1. Clone the package
```
    git clone git@git.i.gini.net:vision/scanned_variant_generator.git
    cd scanned_variant_generator
```
2. create a virtual environment(optional)
```
    virtualenv -p python3.x venv
    source venv/bin/activate
```
3. Install PyBlur (from https://github.com/lospooky/pyblur with a minor change):
```
    cd pyblur
    pip install .
```
4. Install the package:
```
    cd ..
    pip install .
```

## Usage

To generate an scanned/mobile variant of an image or a PDF,
```
    variant-generator input_file_path -o "(Optional)output_image_path" -c "(Optional)configuration_file_path" -b "(Optional)background_file_path or directory"
```
## Help
```
    variant-generator --help
```
## Example:
```
    variant-generator variant_generator/resources/Datev.jpg

    variant-generator variant_generator/resources/Datev.pdf -o out.jpg -b variant_generator/resources/backgrounds/
```

## Tests:

To run the tests,
```
   cd tests/
   pytest .
```
