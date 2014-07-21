## django-schemulator

django-schemulator provides the `form_to_schema(form)` function which generates a 
JSONSchema describing the Django form which is fed as the input argument.

What's this all about? Read the following:

[json-schema.org](http://json-schema.org/)
[A great guide to the JSON Schema syntax](http://spacetelescope.github.io/understanding-json-schema/index.html)
[Django built-in form fields](https://docs.djangoproject.com/en/1.7/ref/forms/fields/)

django-schemulator uses:

[json-document](https://github.com/Cahersan/json-document)
[json-schema-toolkit](https://github.com/Cahersan/json-schema-toolkit)

To use django formulator install it using `pip`
    
    git clone https://github.com/Cahersan/django-schemulator
    cd django-schemulator
    pip install .

and then import the function as follows

    from schemulator import form_to_schema 

django-schemulator is still under developement, but so far it supports the
following Django fields:

* BooleanField	
* CharField	
* ChoiceField	(using `choices` argument)
* DateField	
* DateTimeField	
* DecimalField	
* EmailField	
* FloatField	
* IntegerField	
* IPAddressField	
* GenericIPAddressField	

Here is a list of the field arguments supported so far:

* help_text
* label
* initial
* required

Additionaly, in string-based fields, the following field arguments can be used:

* min_length
* max_length

In number-based fields, the following field arguments can be used:

* min_value
* max_value

