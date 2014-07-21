from importlib import import_module

from django import forms

from json_schema_toolkit.document import JSONDocument, JSONDocumentField


""" 
Django Schemulator
"""

# Dictionaries for form to schema translation {FORM : JSON_SCHEMA}

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
    #GenericIPAddressfield
    "protocol":"format"
}

def form_to_schema(form):

    class JSchema(JSONDocument):
        
        class Meta(object):
            title = u'JSON Schema'
            description = u'This is a JSON Schema describing a form'

    fields = form.base_fields.values()
    field_count = 1 # TODO: Would be better with slugyfied labels, but what if no label?

    for f in fields:

        field_type = f.__class__.__name__  
        
        mod = import_module('json_schema_toolkit.document', FIELDS[field_type])
        jschema_field = getattr(mod, FIELDS[field_type])()
        
        # Setup of JSON Schema keywords 
        for kw in KEYWORDS.keys():
            if hasattr(f, kw):
                content = getattr(f, kw)
                # Special case for choices, as these are described with a simple
                # JSONDocumentField 
                if kw is "choices":
                    content = [JSONDocumentField(enum=content)]
                if kw is "protocol":
                    import ipdb; ipdb.set_trace()
                    content = f.protocol
                setattr(jschema_field, KEYWORDS[kw], content)

        # Setting the JSON Schema field within the JSON Schema
        setattr(JSchema, "field_" + str(field_count), jschema_field)
        field_count+=1

    schema = JSchema({})._schema
    
    return schema
