# Methods

__django-schemulator__ provides the following methods:

#### `wtfield_to_schema(field)` 

This method takes a WTForms field and returns a JSON schema (a dictionary).

&nbsp;

#### `field_to_schema(field)` 

This method takes a Django Forms field and returns a JSON schema (a dictionary).

&nbsp;

#### `form_to_schema(form)` 

This method takes a Django Form or a WTForms and returns a JSON schema (a dictionary).
Internally, it analyzes the fields that the form contains and uses one of the previous 
methods to provide the JSON schema representation.

__Example__

* Django Form

        class TestForm(forms.Form):

            boolean_field = forms.BooleanField(
                                    label="Boolean Field",
                                    help_text="This is a boolean field",
                                    initial=True,
                                    required=False)
         
            text_field = forms.CharField(
                                    label="Text Field",
                                    help_text="This is a text field",
                                    required=False,
                                    max_length=100,
                                    min_length=20)text_field = text_field
         
            email_field = forms.EmailField( label="Email Field",
                                    help_text="This is an email field",
                                    initial="email@example.com",
                                    max_length=100,
                                    required=False)

* WTForm

        class TestForm(wtforms.Form): 

            boolean_field = wtforms.BooleanField(
                                    "Boolean Field",
                                    description="This is a boolean field",
                                    default=True,
                                    validators=[wtforms.validators.Optional()])

            email_field = wtforms.StringField(
                                   "Email Field",
                                   description="This is an email field",
                                   default="email@example.com",
                                   validators=[ wtforms.validators.Email(),
                                                wtforms.validators.Length(max=100),)
                                                wtforms.validators.Optional()])

            text_field = wtforms.StringField(
                                   "Text Field",
                                   description="This is a text field",
                                   validators=[ wtforms.validators.Length(min=20, max=100),
                                                wtforms.validators.Optional()])


For both forms, the corresponding JSON Shema is the following. 
__Note:__ _Some irrelevant entries have been removed for clarity._

    { '$schema': 'http://json-schema.org/draft-04/schema#', 
      'description': 'This is a JSON Schema describing a form',
      'title': 'JSON Schema'
      'properties': {
           'boolean_field': {
               'description': 'This is a boolean field', 
               'null': False, 
               'optional': True,
               'title': 'Boolean Field',
               'default': True,
               'type': 'boolean'}, 
           'email_field': {
               'description': 'This is an email field',
               'format': 'email',
               'maxLength': 100,
               'null': False, 
               'optional': True, 
               'title': 'Email Field',
               'default': 'email@example.com',
               'type': 'string'}, 
           'text_field': {
               'description': 'This is a text field',
               'minLength': 20,
               'maxLength': 100,
               'null': False,
               'optional': True,
               'title': 'Text Field',
               'default': None,
               'type': 'string'}},
    }

&nbsp;

#### `schema_to_form(schema, form_type=None)` 

This method takes a dictionary with a valid JSON Schema syntax and returns a form.
By default, the form returned is a Django Form, but by setting the`form_type` 
argument to `wtforms` the output is a WTForm.

&nbsp;

#### `schema_to_wtfield(schema)` 

This method is used by the`schema_to_form()` method to dynamically generate the
fields within the returned form. It takes a dictionary with a valid JSON Schema syntax describing a field
and returns an WTForms `UnboundField` instance.

If you where to use it independently, you may bind the field to a form by setting it as an
attribute of a WTForms form before instatination, via `setattr`.

&nbsp;

#### `schema_to_field(schema)` 

This method is used by the`schema_to_form()` method to dynamically generate the
fields within the returned form. It takes a dictionary with a valid JSON Schema syntax describing a field
and returns an Django Forms field instance.

&nbsp;

## Special JSON Schema Keywords

__django-schemulator__ recognizes three special keywords within a JSON Schema
representation of a form. These can be provided to explicitly indicate which field
classes and widgets should be used within the forms. These should be the name of
the form or widget class.

* `__django_form_field_cls`

    The Django forms field class to be used.

* `__wtforms_field_cls`

    The WTForms field class to be used.

* `__widget`

    The Django forms or WTforms widget class to be used.

__Example__:
 
The following JSON Schema describes a Django forms `CharField` with a `Textarea` widget instead
of the default `TextInput` widget.

    {
    '__django_form_field_cls': 'CharField', 
    '__widget': 'Textarea',
    'type': 'string',
    'title': 'Text Area Field',
    'description': 'This is a text area field',
    'minLength': 0, 
    'maxLength': 200,
    'optional': False,
    }
