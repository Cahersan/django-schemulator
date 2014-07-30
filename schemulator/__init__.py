from importlib import import_module

from django import forms

from json_schema_toolkit.document import JSONDocument, JSONDocumentField


""" 
Django Schemulator
"""

# Dictionaries for django form fields to json schema toolkit fields translation
# {FORM : JSON_SCHEMA}

FIELDS = {
        #Django Forms built-in Field classes
        "BooleanField":"JSONBooleanField",
        "CharField":"JSONStringField",
        "ChoiceField":"JSONListField",
        "TypedChoiceField":"",
        "DateField":"JSONDateField",
        "DateTimeField":"JSONDateTimeField",
        "DecimalField":"JSONDecimalField",
        "EmailField":"JSONEmailField",
        "FileField":"",
        "FilePathField":"",
        "FloatField":"JSONDecimalField",
        "ImageField":"",
        "IntegerField":"JSONIntegerField",
        "IPAddressField":"JSONIPAddressField",
        "GenericIPAddressField":"JSONIPAddressField",
        "MultipleChoiceField":"",
        "TypedMultipleChoiceField":"",
        "NullBooleanField":"",
        "RegexField":"",
        "SlugField":"",
        "TimeField":"",
        "URLField":"",
        #Django forms slightly complex built-in Field classes
        "ComboField":"",
        "MultiValueField":"",
        "SplitDateTimeField":"",
        #Fields which handle relationships
        "ModelChoiceField":"",
        "ModelMultipleChoiceField":"",
        #Custom Fields
        "Field":"",
}

KEYWORDS = {
    #Base keywords
    "label":"title",
    "help_text":"description",
    "initial":"default",
    "required":"optional",
    #String type-specific keywords
    "max_length":"maxLength",
    "min_length":"minLength",
    #Numerical type-specific keywords
    "min_value":"minimum",
    "max_value":"maximum",
    #Choice-specific keyword
    "choices":"content",
}

def field_to_schema(field):
    """
    """
    field_type = field.__class__.__name__  
        
    mod = import_module('json_schema_toolkit.document', FIELDS[field_type])
    jschema_field = getattr(mod, FIELDS[field_type])()
    
    # Special case for GenericIPAddressField, as protocol is not a field
    # attribute, and must be induced from the validator.
    if field_type == "GenericIPAddressField":
        #import ipdb; ipdb.set_trace()
        validator = str(field.validators[0]) 
        value = 'ipv6' if 'ipv6' in validator else 'ipv4'
        setattr(jschema_field, 'protocol', value)
    
    # Setup of JSON Schema keywords 
    for (field_kw, jschema_kw) in KEYWORDS.items():
        if hasattr(field, field_kw):
            value = getattr(field, field_kw)
            # Special case for choices, as these are described with a simple
            # JSONDocumentField 
            if field_kw == "choices":
                value = [JSONDocumentField(enum=value)]
            if field_kw == "required":
                value = not value
            setattr(jschema_field, jschema_kw, value)

    return jschema_field._generate_schema()

def form_to_schema(form):
    """
    """

    schema = {  
        '$schema':'http://json-schema.org/draft-04/schema#',
        'title':'JSON Schema',
        'description':'This is a JSON Schema describing a form',
        'properties':{}
    }

    # Loop through all form fields, get their JSON schema representation and
    # add it to the schema properties
    for (name, field) in form.base_fields.items():

        field_schema = field_to_schema(field)
        schema['properties'][name] = field_schema

    return schema

def schema_to_field(schema):
    """
    Returns a Django Forms field when given a schema fragment describing a 
    field: that is, any entry of the 'properties' keyword
    """

    jschema_type = schema['type']
    kwargs = {}

    # This loop sets the value of relevant field keyword arguments
    for (field_kw, jschema_kw) in KEYWORDS.items():
        if jschema_kw in schema:
            value = schema[jschema_kw]
            if jschema_kw == "optional":
                value = not value
            kwargs[field_kw]=value
    
    # This loop decides upon which form field should be used
    if jschema_type == 'boolean':
        field_type = 'BooleanField'  
    elif jschema_type == 'string':
        field_type = 'CharField'  
        if 'format' in schema:
            if schema['format'] == 'email':
                field_type = 'EmailField'
            if schema['format'] == 'date-time':
                field_type = 'DateTimeField'
            if schema['format'] == 'ipv4':
                field_type = 'GenericIPAddressField'
            if schema['format'] == 'ipv6':
                field_type = 'GenericIPAddressField'
                kwargs['protocol']='ipv6'
    elif jschema_type == 'integer':
        field_type = 'IntegerField'
    elif jschema_type == 'number':
        field_type = 'FloatField'
    elif jschema_type == 'array':
        field_type = 'ChoiceField'
        if 'items' in schema: kwargs['choices'] = schema['items'][0]['enum']

    mod = import_module('django.forms', field_type)
    form_field = getattr(mod, field_type)
    field = form_field(**kwargs)

    return field

def schema_to_form(schema):
    """
    """

    form = forms.Form()

    # loop along fields
    for (name, prop) in schema['properties'].items():
    
        field = schema_to_field(prop)
        form.fields[name] = field

    return form 

