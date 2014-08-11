from copy import deepcopy
from django.test import TestCase
import wtforms

from jsonschema import validate, Draft4Validator, ValidationError

from schemulator import form_to_schema, field_to_schema, schema_to_form, schema_to_wtfield


# These are FIELDS to test within the form and their equivalent representation
# as PROPERTIES within the JSON schema

#BOOLEAN FIELD: Also used to test OPTIONAL and DEFAULT keywords
boolean_field = wtforms.BooleanField(   "Boolean Field",
                                        description="This is a boolean field",
                                        default=True,
                                        validators=[wtforms.validators.Optional()])

boolean_field_js = {
    'type': 'boolean',
    'title': 'Boolean Field',
    'description': 'This is a boolean field',
    'default': True,
    'optional': True
}

# STRING FIELD: Tests wtforms.validators.Length()
string_field = wtforms.StringField( "String Field",
                                    description="This is a string field",
                                    validators=[wtforms.validators.Length(min=10, max=50)])


string_field_js = {
    'type': 'string',
    'title': 'String Field',
    'description': 'This is a string field',
    'minLength':10,
    'maxLength':50
}

# TEXT FIELD
text_field = wtforms.TextField( "Text Field",
                                description="This is a text field",
                                validators=[wtforms.validators.Length(min=10, max=50)])


text_field_js = {
    'type': 'string',
    'title': 'Text Field',
    'description': 'This is a text field',
    'minLength':10,
    'maxLength':50
}

# TEXT AREA FIELD: Test '__widget' keyword
text_area_field = wtforms.TextAreaField("Text Area Field",
                                        description="This is a text area field",
                                        validators=[wtforms.validators.Length(min=0, max=200)])


text_area_field_js = {
    '__widget':'TextArea',
    'type': 'string',
    'title': 'Text Area Field',
    'description': 'This is a text area field',
    'minLength':0,
    'maxLength':200
}

# EMAIL FIELD: Tests wtforms.validators.Email()
email_field = wtforms.StringField(  "Email Field",
                                    description="This is an email field",
                                    default="email@example.com",
                                    validators=[wtforms.validators.Email(),
                                                wtforms.validators.Length(min=10)])

email_field_js = {
    'type': 'string', 
    'title': 'Email Field',
    'description': 'This is an email field', 
    'format': 'email', 
    'default': 'email@example.com',
    'minLength':10
}

# DECIMAL FIELD: Tests wtforms.validators.NumberRange()
decimal_field = wtforms.DecimalField(   "Decimal Field",
                                        description="This is a decimal field",
                                        validators=[wtforms.validators.NumberRange(min=0, max=100)])

decimal_field_js = {
    'type': 'number', 
    'title': 'Decimal Field',
    'description': 'This is a decimal field', 
    'maximum': 100, 
    'minimum': 0, 
}

# FLOAT FIELD
float_field = wtforms.FloatField( "Float Field",
                                description="This is a float field",
                                validators=[wtforms.validators.NumberRange(min=2.53),
                                            wtforms.validators.Optional()])

float_field_js = {
    'type': 'number', 
    'title': 'Float Field',
    'description': 'This is a float field', 
    'minimum': 2.53, 
    'optional': True,
}

# INTEGER FIELD
integer_field = wtforms.IntegerField(   "Integer Field",
                                        description="This is an integer field",
                                        default=10)

integer_field_js = {
    'type': 'integer', 
    'title': 'Integer Field',
    'description': 'This is an integer field', 
    'default': 10,
}

# SELECT FIELD
select_field = wtforms.SelectField( "Select Field",
                                    description="This is a select field",
                                    choices=["choice_1", "choice_2", "choice_3"])

select_field_js = {
    'type': 'string', 
    'title': 'Select Field',
    'description': 'This is a select field', 
    'enum': ["choice_1", "choice_2", "choice_3"],
}

# RADIO FIELD
radio_field = wtforms.RadioField( "Radio Field",
                                  description="This is a radio field",
                                  choices=["choice_1", "choice_2", "choice_3"])


radio_field_js = {
    '__widget':'ListWidget',
    'type': 'string', 
    'title': 'Radio Field',
    'description': 'This is a radio field', 
    'enum': ["choice_1", "choice_2", "choice_3"],
}

# SELECT MULTIPLE FIELD
select_multiple_field = wtforms.SelectMultipleField( "Select Multiple Field",
                                    description="This is a select multiple field",
                                    choices=["choice_1", "choice_2", "choice_3"])


select_multiple_field_js = {
    'type': 'string', 
    'title': 'Select Multiple Field',
    'description': 'This is a select multiple field', 
    'enum': ["choice_1", "choice_2", "choice_3"],
}

# IPV4 FIELD
ipv4_field = wtforms.StringField(   "IPV4 Address Field",
                                    description="This is an IPV4 address field",
                                    validators=[wtforms.validators.IPAddress(ipv4=True)])
                                       

ipv4_field_js = {
    'type': 'string', 
    'title': 'IPV4 Address Field',
    'description': 'This is an IPV4 address field', 
    'format': 'ipv4', 
}

# IPV6 FIELD
ipv6_field = wtforms.StringField(   "IPV6 Address Field",
                                    description="This is an IPV6 address field",
                                    validators = [wtforms.validators.IPAddress(ipv6=True)])

ipv6_field_js = {
    'type': 'string', 
    'title': 'IPV6 Address Field',
    'description': 'This is an IPV6 address field', 
    'format': 'ipv6', 
}

# DATE FIELD
date_field = wtforms.DateField( "Date Field",
                                description="This is a date field")

date_field_js = {
    'type': 'string', 
    'title': 'Date Field',
    'description': 'This is a date field', 
}

# TIME FIELD: Tests the Regexp Validator
time_field = wtforms.StringField( "Time Field",
                                description="This is a time field",
                                validators=[wtforms.validators.Regexp("^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$|^([0-1]?[0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$")])


time_field_js = {
    'type': 'string', 
    'title': 'Time Field',
    'description': 'This is a time field', 
    'pattern':"^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$|^([0-1]?[0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
}

# DATE TIME FIELD
date_time_field = wtforms.DateTimeField(    "Date-Time Field",
                                            description="This is a date-time field")


date_time_field_js = {
    'type': 'string', 
    'title': 'Date-Time Field',
    'description': 'This is a date-time field', 
    'format': 'date-time', 
}

# SLUG FIELD: Tests the Regexp Validator
slug_field = wtforms.StringField(   "Slug Field",
                                    description="This is a slug field",
                                    validators=[wtforms.validators.Optional(),
                                                wtforms.validators.Length(min=10, max=50),
                                                wtforms.validators.Regexp(r"^[a-z0-9-]+$")])


slug_field_js = {
    'type': 'string', 
    'title': 'Slug Field',
    'description': 'This is a slug field', 
    'optional':True,
    'maxLength':50,
    'minLength':10,
    'pattern':r"^[a-z0-9-]+$"
}

# URL FIELD
url_field = wtforms.StringField("URL Field",
                                description="This is an URL field",
                                validators = [wtforms.validators.URL(require_tld=False)])

url_field_js = {
    'type': 'string', 
    'title': 'URL Field',
    'description': 'This is an URL field', 
}


# A FORM
class TestForm(wtforms.Form):
    boolean_field = boolean_field
    string_field = string_field
    text_field = text_field
    text_area_field = text_area_field
    email_field = email_field
    decimal_field = decimal_field
    float_field = float_field 
    integer_field = integer_field
    select_field = select_field
    radio_field = radio_field
    select_multiple_field = select_multiple_field
    ipv4_field = ipv4_field
    ipv6_field = ipv6_field
    date_field = date_field
    time_field = time_field
    date_time_field = date_time_field
    slug_field = slug_field
    url_field = url_field

# An instance of TestForm to work with
test_form = TestForm()

def dict_in_dict(d, subset_d):
    """
    Checks if the items in a dictionary are all contained within some other
    dictionary. This is used to check if the schema created contains all the
    expected information.
    """
    return all([i in d.items() for i in subset_d.items()])

class FormToSchemaTestCase(TestCase):
    
    def setUp(self):
        pass

   # def test_unsupported_field(self):

   #     class TestFormCopy(TestForm):
   #         pass

   #     setattr(TestFormCopy, 'select_multiple_field', select_multiple_field)
   #     self.test_form = TestFormCopy()
   #     #import ipdb; ipdb.set_trace()

   #     with self.assertRaises(AttributeError):
   #         field_schema = field_to_schema(self.test_form.select_multiple_field)

    def test_schema(self):
        schema = form_to_schema(test_form)
        self.assertIsNone(Draft4Validator.check_schema(schema))

    def test_boolean_field(self):
        field_schema = field_to_schema(test_form.boolean_field)
        self.assertTrue(dict_in_dict(field_schema, boolean_field_js))

    def test_string_field(self):
        field_schema = field_to_schema(test_form.string_field)
        self.assertTrue(dict_in_dict(field_schema, string_field_js))
        
    def test_text_field(self):
        field_schema = field_to_schema(test_form.text_field)
        self.assertTrue(dict_in_dict(field_schema, text_field_js))
        
    def test_text_area_field(self):
        field_schema = field_to_schema(test_form.text_area_field)
        self.assertTrue(dict_in_dict(field_schema, text_area_field_js))
        
    def test_email_field(self):
        field_schema = field_to_schema(test_form.email_field)
        self.assertTrue(dict_in_dict(field_schema, email_field_js))
        
    def test_decimal_field(self):
        field_schema = field_to_schema(test_form.decimal_field)
        self.assertTrue(dict_in_dict(field_schema, decimal_field_js))
        
    def test_float_field(self):
        field_schema = field_to_schema(test_form.float_field)
        self.assertTrue(dict_in_dict(field_schema, float_field_js))
        
    def test_integer_field(self):
        field_schema = field_to_schema(test_form.integer_field)
        self.assertTrue(dict_in_dict(field_schema, integer_field_js))
       
    def test_select_field(self):
        field_schema = field_to_schema(test_form.select_field)
        self.assertTrue(dict_in_dict(field_schema, select_field_js))
        
    def test_radio_field(self):
        field_schema = field_to_schema(test_form.radio_field)
        self.assertTrue(dict_in_dict(field_schema, radio_field_js))
        
    def test_select_multiple_field(self):
        field_schema = field_to_schema(test_form.select_multiple_field)
        self.assertTrue(dict_in_dict(field_schema, select_multiple_field_js))

    def test_ipv4_field(self):
        field_schema = field_to_schema(test_form.ipv4_field)
        self.assertTrue(dict_in_dict(field_schema, ipv4_field_js))
        
    def test_ipv6_field(self):
        field_schema = field_to_schema(test_form.ipv6_field)
        self.assertTrue(dict_in_dict(field_schema, ipv6_field_js))

    def test_date_field(self):
        field_schema = field_to_schema(test_form.date_field)
        self.assertTrue(dict_in_dict(field_schema, date_field_js))

    def test_date_field_validation(self):
        field_schema = field_to_schema(test_form.date_field)
        self.assertIsNone(validate('2006-10-25', field_schema))
        self.assertIsNone(validate('10/25/2006', field_schema))
        self.assertIsNone(validate('10/25/06', field_schema))
        # Try/Except clause has to be used instead of assertRaises() because 
        # validate() itself doesn't raise ValidationError.
        try:
            validate('128-4-5269', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass
        try:
            validate('foo', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass
        
    def test_time_field(self):
        field_schema = field_to_schema(test_form.time_field)
        self.assertTrue(dict_in_dict(field_schema, time_field_js))

    def test_time_field_validation(self):
        field_schema = field_to_schema(test_form.time_field)
        self.assertIsNone(validate('10:00:30', field_schema))
        self.assertIsNone(validate('10:00', field_schema))
        # Try/Except clause has to be used instead of assertRaises() because 
        # validate() itself doesn't raise ValidationError.
        try:
            validate('10:70', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass
        try:
            validate('foo', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass
    
    def test_date_time_field(self):
        field_schema = field_to_schema(test_form.date_time_field)
        self.assertTrue(dict_in_dict(field_schema, date_time_field_js))

    def test_slug_field(self):
        field_schema = field_to_schema(test_form.slug_field)
        self.assertTrue(dict_in_dict(field_schema, slug_field_js))

    def test_slug_field_validation(self):
        field_schema = field_to_schema(test_form.slug_field)
        self.assertIsNone(validate('th1s-is-a-v4l1d-slug', field_schema))
        try:
            validate('this_IS_not:a/valid-slug!', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass

    def test_url_field(self):
        field_schema = field_to_schema(test_form.url_field)
        self.assertTrue(dict_in_dict(field_schema, url_field_js))

    def test_url_field_validation(self):
        field_schema = field_to_schema(test_form.url_field)

        self.assertIsNone(validate('http://www.example.org/resource.txt', field_schema))
        self.assertIsNone(validate('https://localhost:8000', field_schema))
        self.assertIsNone(validate('http://209.85.255.255', field_schema))
        self.assertIsNone(validate('ftp://example.org/', field_schema))

        try:
            validate('http://notvalid', field_schema)
            validate('htp://notvalid.com', field_schema)
            validate('localhost', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass

class SchemaToFormTestCase(TestCase):

    def setUp(self):
        
        fields = {
            'boolean_field':boolean_field,
            'string_field':string_field,
            'text_field':text_field,
            'text_area_field':text_area_field,
            'email_field':email_field,
            'decimal_field':decimal_field,
            'float_field':float_field,
            'integer_field':integer_field,
            'select_field':select_field,
            'radio_field':radio_field,
            'select_multiple_field':select_multiple_field,
            'ipv4_field':ipv4_field,
            'ipv6_field':ipv6_field,
            'date_field':date_field,
            'time_field':time_field,
            'date_time_field':date_time_field,
            'slug_field':slug_field,
            'url_field':url_field,
        }

        self.schema = {  
            '$schema':'http://json-schema.org/draft-04/schema#',
            'title':'JSON Schema',
            'description':'This is a JSON Schema describing a form',
            'properties':{}
        }

    def test_form_to_schema_to_form(self):
        """
        Translates a form to a schema and back to a form and checks if the 
        form fields are the same in both forms. In this case, the __wtforms_field_cls
        keyword is being used as it is set in the form_to_schema function. 
        """
        schema = form_to_schema(test_form)
        recovered_form = schema_to_form(schema, form_type='wtforms')
        rffi = [i[1].type for i in sorted(recovered_form._fields.items())]
        tffi = [i[1].type for i in sorted(test_form._fields.items())]
        self.assertEquals(rffi, tffi)

    def test_boolean_field(self):
        schema = self.schema 
        schema['properties']['boolean_field'] = boolean_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['boolean_field']), boolean_field_js))

    def test_string_field(self):
        schema = self.schema 
        schema['properties']['string_field'] = string_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['string_field']), string_field_js))
        
    def test_text_field(self):
        schema = self.schema 
        schema['properties']['text_field'] = text_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['text_field']), text_field_js))

    def test_text_area_field(self):
        schema = self.schema 
        schema['properties']['text_area_field'] = text_area_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['text_area_field']), text_area_field_js))

    def test_email_field(self):
        schema = self.schema 
        schema['properties']['email_field'] = email_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['email_field']), email_field_js))
        
    def test_decimal_field(self):
        schema = self.schema 
        schema['properties']['decimal_field'] = decimal_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['decimal_field']), decimal_field_js))
        
    def test_float_field(self):
        schema = self.schema 
        schema['properties']['float_field'] = float_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['float_field']), float_field_js))
        
    def test_integer_field(self):
        schema = self.schema 
        schema['properties']['integer_field'] = integer_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['integer_field']), integer_field_js))
        
    def test_select_field(self):
        schema = self.schema 
        schema['properties']['select_field'] = select_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['select_field']), select_field_js))
        
    def test_radio_field(self):
        schema = self.schema 
        schema['properties']['radio_field'] = radio_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['radio_field']), radio_field_js))

    def test_select_multiple_field(self):
        schema = self.schema 
        schema['properties']['select_multiple_field'] = select_multiple_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['select_multiple_field']), select_multiple_field_js))
        
    def test_ipv4_field(self):
        schema = self.schema 
        schema['properties']['ipv4_field'] = ipv4_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['ipv4_field']), ipv4_field_js))
    
    def test_ipv6_field(self):
        schema = self.schema 
        schema['properties']['ipv6_field'] = ipv6_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['ipv6_field']), ipv6_field_js))
        
    def test_date_field(self):
        schema = self.schema 
        schema['properties']['date_field'] = date_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['date_field']), date_field_js))

    def test_time_field(self):
        schema = self.schema 
        schema['properties']['time_field'] = time_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['time_field']), time_field_js))

    def test_date_time_field(self):
        schema = self.schema 
        schema['properties']['date_time_field'] = date_time_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['date_time_field']), date_time_field_js))
    
    def test_slug_field(self):
        schema = self.schema 
        schema['properties']['slug_field'] = slug_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['slug_field']), slug_field_js))
    
    def test_url_field(self):
        schema = self.schema 
        schema['properties']['url_field'] = url_field_js
        form = schema_to_form(schema, form_type='wtforms')
        self.assertTrue(dict_in_dict(field_to_schema(form['url_field']), url_field_js))

