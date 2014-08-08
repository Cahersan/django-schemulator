# Introduction

__django-schemulator__ aims to provide an easy way to generate descriptions of
forms using JSON Schema. __django-schemulator__ can convert [Django Forms](https://docs.djangoproject.com/en/dev/ref/forms/api/#django.forms.Form) and
[WTForms](https://wtforms.readthedocs.org/en/latest/index.html#) to JSON Schema representations and viceversa.

Learn more about JSON Schema in [json-schema.org](http://json-schema.org/) and throught this [great guide](http://spacetelescope.github.io/understanding-json-schema/index.html) to the JSON Schema syntax.

### Installation

Install __django-schemulator__ via `pip`
    
    git clone https://github.com/Cahersan/django-schemulator
    cd django-schemulator
    pip install .


django-schemulator uses:

[json-document](https://github.com/Cahersan/json-document)  
[json-schema-toolkit](https://github.com/Cahersan/json-schema-toolkit)


### What's Supported?

__django-schemulator__ is still under developement, but so far supports a great deal of
Django Forms and WTForms fields as well as field arguments and validators. Refer to
[what's supported](support.md) to learn more.  

