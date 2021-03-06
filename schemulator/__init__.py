from importlib import import_module

from django import forms

from json_schema_toolkit.document import JSONDocument, JSONDocumentField
import wtforms


""" 
Django Schemulator
"""

# Dictionaries for django form fields to json schema toolkit fields translation
# {FORM : JSON_SCHEMA}

FIELDS = {
    #Django Forms built-in Field classes
    "BooleanField":"JSONBooleanField",
    "CharField":"JSONStringField",
    "ChoiceField":"JSONStringField",
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
    "SlugField":"JSONSlugField",
    "TimeField":"JSONTimeField",
    "URLField":"JSONURLField",
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

WTFIELDS = {
    "BooleanField":"JSONBooleanField",
    "DateField":"JSONDateField",
    "DateTimeField":"JSONDateTimeField",
    "DecimalField":"JSONDecimalField",
    "Field":"",
    "FileField":"",
    "FloatField":"JSONDecimalField",
    "FormField":"",
    "HiddenField":"",
    "IntegerField":"JSONIntegerField",
    "PasswordField":"",
    "RadioField":"JSONStringField",
    "SelectField":"JSONStringField",
    "SelectFieldBase":"",
    "SelectMultipleField":"JSONStringField",
    "StringField":"JSONStringField",
    "SubmitField":"",
    "TextAreaField":"JSONStringField",
    "TextField":"JSONStringField",
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
    "choices":"enum",
}

TYPES = {
    'boolean':'BooleanField',
    'integer':'IntegerField',
    'number':'FloatField',
    'string':'CharField'
}

FORMATS = {
    'date-time':'DateTimeField',
    'email':'EmailField',
    'ipv4':'GenericIPAddressField',
    'ipv6':'GenericIPAddressField',
}


def wtfield_to_schema(field):
    """
    """
    field_type = field.type  
        
    mod = import_module('json_schema_toolkit.document', WTFIELDS[field_type])
    try:
        jschema_field = getattr(mod, WTFIELDS[field_type])()
    except AttributeError:
        raise AttributeError(field_type + " is currently unsupported.")

    # Setup of common JSON Schema keywords 
    setattr(jschema_field, 'title', field.label.text)
    setattr(jschema_field, 'description', field.description)
    setattr(jschema_field, 'default', field.default)

    schema = jschema_field._generate_schema()

    schema['__wtforms_field_cls'] = field_type
    schema['__widget'] = field.widget.__class__.__name__

    if  field_type == 'SelectField' or \
        field_type == 'SelectMultipleField' or \
        field_type == 'RadioField':
        schema['enum'] = field.choices 

    # Setup of jsonschema keywords depending on validators
    for validator in  field.validators:
        val = validator.__class__.__name__
        
        if val == 'Optional':
            schema['optional']=True
        if val == 'Email':
            schema['format']='email'
        if val == 'NumberRange':
            if validator.min is not None: schema['minimum'] = validator.min
            if validator.max is not None: schema['maximum'] = validator.max
        if val == 'Length':
            if validator.min is not -1: schema['minLength'] = validator.min 
            if validator.max is not -1: schema['maxLength'] = validator.max
        if val == 'IPAddress':
            if validator.ipv4: schema['format'] = 'ipv4'
            if validator.ipv6: schema['format'] = 'ipv6' 
        if val == 'URL' or  val == 'Regexp':
            schema['pattern']=validator.regex.pattern

    return schema


def field_to_schema(field):
    """
    """

    if isinstance(field, wtforms.Field):
        schema = wtfield_to_schema(field)
        return schema

    field_type = field.__class__.__name__  
        
    mod = import_module('json_schema_toolkit.document', FIELDS[field_type])
    jschema_field = getattr(mod, FIELDS[field_type])()
    
    # Special case for GenericIPAddressField, as protocol is not a field
    # attribute, and must be deduced from the validator.
    if field_type == "GenericIPAddressField":
        validator = str(field.validators[0]) 
        value = 'ipv6' if 'ipv6' in validator else 'ipv4'
        setattr(jschema_field, 'protocol', value)
    
    # Setup of JSON Schema keywords 
    for (field_kw, jschema_kw) in KEYWORDS.items():
        if hasattr(field, field_kw):
            value = getattr(field, field_kw)
            # Special case, optional != required
            if field_kw == "required": value = not value
            setattr(jschema_field, jschema_kw, value)
    
    schema = jschema_field._generate_schema()

    # Set __django_form_field_cls keyword
    schema['__django_form_field_cls'] = field_type
    schema['__widget'] = field.widget.__class__.__name__

    return schema


def form_to_schema(form):
    """
    """

    schema = {  
        '$schema':'http://json-schema.org/draft-04/schema#',
        'title':'JSON Schema',
        'description':'This is a JSON Schema describing a form',
        'properties':{}
    }
    
    if isinstance(form, wtforms.form.BaseForm):
        for field in form:

            field_schema = field_to_schema(field)
            schema['properties'][field.name] = field_schema
    else:
        # Loop through all form fields, get their JSON schema representation and
        # add it to the schema properties
        for (name, field) in form.fields.items():

            field_schema = field_to_schema(field)
            schema['properties'][name] = field_schema

    return schema


def schema_to_wtfield(schema):
    """
    Returns a WTForms Field when given a schema fragment. Returns a field which
    is Unbound.
    """
    
    kwargs = {}
    validators = []

    # This block sets the value of relevant field keyword arguments
    if 'description' in schema: kwargs['description'] = schema['description']
    if 'title' in schema: kwargs['label'] = schema['title']
    if 'default' in schema: kwargs['default'] = schema['default']
    if 'optional' in schema: validators.append(wtforms.validators.Optional())
    if 'minLength' in schema: validators.append(wtforms.validators.Length(min=schema['minLength']))
    if 'maxLength' in schema: validators.append(wtforms.validators.Length(max=schema['maxLength']))
    if 'minimum' in schema: validators.append(wtforms.validators.NumberRange(min=schema['minimum']))
    if 'maximum' in schema: validators.append(wtforms.validators.NumberRange(max=schema['maximum']))
    if 'pattern' in schema: validators.append(wtforms.validators.Regexp(schema['pattern']))
    
    # This block decides upon which form wtfield should be used.
    if '__wtforms_field_cls' in schema:
        field_type = schema['__wtforms_field_cls']
    elif 'enum' in schema:
        field_type = 'SelectField'
        kwargs['choices'] = schema['enum']
    elif 'format' in schema and schema['type'] == 'string':
        field_type = 'StringField'
        if schema['format'] == 'ipv4':
            validators.append(wtforms.validators.IPAddress(ipv4=True))
        if schema['format'] =='ipv6': 
            validators.append(wtforms.validators.IPAddress(ipv6=True))
        if schema['format'] == 'email': 
            validators.append(wtforms.validators.Email())
        if schema['format'] == 'date-time': 
            field_type = 'DateTimeField'
    else: 
        field_type = TYPES[schema['type']]
        if field_type=='CharField': field_type='StringField' 
    
    kwargs['validators']=validators

    if '__widget' in schema:
        mod = import_module('wtforms.widgets', schema['__widget'])
        widget = getattr(mod, schema['__widget'])() 
        kwargs['widget'] = widget

    mod = import_module('wtforms', field_type)
    form_field = getattr(mod, field_type)(**kwargs)

    return form_field


def schema_to_field(schema):
    """
    Returns a Django Forms field when given a schema fragment describing a 
    field: that is, any entry of the 'properties' keyword
    """

    # This block sets the value of relevant field keyword arguments
    
    kwargs = {}

    for (field_kw, jschema_kw) in KEYWORDS.items():
        if jschema_kw in schema:
            value = schema[jschema_kw]
            if jschema_kw == "optional":
                value = not value
            kwargs[field_kw]=value
    
    # This block decides upon which form field should be used. This can be 
    # explicitly specified in a JSON schema via the '__django_form_field_cls'
    # keyword

    if '__django_form_field_cls' in schema:
        field_type = schema['__django_form_field_cls']
    elif 'enum' in schema:
        field_type = 'ChoiceField'
    elif 'format' in schema and schema['type'] == 'string':
        field_type = FORMATS[schema['format']]
        # Special case for ipv6
        if schema['format'] == 'ipv6': kwargs['protocol']='ipv6'
    else: 
        field_type = TYPES[schema['type']]

    if '__widget' in schema:
        mod = import_module('django.forms.widgets', schema['__widget'])
        widget = getattr(mod, schema['__widget'])() 
        kwargs['widget'] = widget

    mod = import_module('django.forms', field_type)
    form_field = getattr(mod, field_type)
    field = form_field(**kwargs)

    return field


def schema_to_form(schema, form_type=None):
    """
    """

    # Case for wtforms
    if form_type == 'wtforms':

        class Form(wtforms.Form):
            pass

        for (name, prop) in schema['properties'].items():
            field = schema_to_wtfield(prop)
            setattr(Form, name, field)
        
        return Form()

    # Case for Django Forms
    form = forms.Form()

    # loop along fields
    for (name, prop) in schema['properties'].items():
    
        field = schema_to_field(prop)
        form.fields[name] = field

    return form 

