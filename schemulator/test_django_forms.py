from django.test import TestCase
from django import forms

from jsonschema import validate, Draft4Validator, ValidationError

from schemulator import form_to_schema, field_to_schema, schema_to_form, schema_to_field


# These are FIELDS to test within the form and their equivalent representation
# as PROPERTIES within the JSON schema

#BOOLEAN FIELD
boolean_field = forms.BooleanField( label="Boolean Field",
                                    help_text="This is a boolean field",
                                    initial=True,
                                    required=False)

boolean_field_js = {
    'default': True,
    'title': 'Boolean Field',
    'description': 'This is a boolean field',
    'type': 'boolean',
    'optional': True,
}

# TEXT FIELD
text_field = forms.CharField(   label="Text Field",
                                help_text="This is a text field",
                                required=False,
                                max_length=100,
                                min_length=20)

text_field_js = {
    'type': 'string',
    'description': 'This is a text field', 
    'title': 'Text Field',
    'optional': True,
    'maxLength': 100,
    'minLength': 20,
}

# TEXT AREA FIELD: Tests '__widget' keyword
text_area_field = forms.CharField(   label="Text Area Field",
                                help_text="This is a text area field",
                                max_length=200,
                                min_length=0,
                                widget=forms.widgets.Textarea)

text_area_field_js = {
    '__widget':'Textarea',
    'type': 'string',
    'description': 'This is a text area field', 
    'title': 'Text Area Field',
    'optional': False,
    'maxLength': 200,
    'minLength': 0,
}

# EMAIL FIELD
email_field = forms.EmailField( label="Email Field",
                                help_text="This is an email field",
                                initial="email@example.com",
                                max_length=100,
                                required=False)

email_field_js = {
    'type': 'string', 
    'title': 'Email Field',
    'description': 'This is an email field', 
    'format': 'email', 
    'default': 'email@example.com',
    'maxLength': 100, 
    'optional': True,
}

# DECIMAL FIELD
decimal_field = forms.DecimalField( label="Decimal Field",
                                    help_text="This is a decimal field",
                                    initial=10.04,
                                    max_value=100,
                                    min_value=0,
                                    required=True)

decimal_field_js = {
    'type': 'number', 
    'title': 'Decimal Field',
    'description': 'This is a decimal field', 
    'default': 10.04,
    'maximum': 100, 
    'minimum': 0, 
    'optional': False,
}

# FLOAT FIELD
float_field = forms.FloatField( label="Float Field",
                                help_text="This is a float field",
                                initial=10.04,
                                max_value=100,
                                min_value=2.53,
                                required=False)

float_field_js = {
    'type': 'number', 
    'title': 'Float Field',
    'description': 'This is a float field', 
    'default': 10.04,
    'maximum': 100, 
    'minimum': 2.53, 
    'optional': True,
}

# INTEGER FIELD
integer_field = forms.IntegerField( label="Integer Field",
                                    help_text="This is an integer field",
                                    initial=10,
                                    max_value=50,
                                    min_value=10,
                                    required=False)

integer_field_js = {
    'type': 'integer', 
    'title': 'Integer Field',
    'description': 'This is an integer field', 
    'default': 10,
    'maximum': 50, 
    'minimum': 10, 
    'optional': True,
}

# CHOICE FIELD
choice_field = forms.ChoiceField(   label="Choice Field",
                                    help_text="This is a choice field",
                                    choices=["choice_1", "choice_2", "choice_3"],
                                    required=False)

choice_field_js = {
    'type': 'string', 
    'title': 'Choice Field',
    'description': 'This is a choice field', 
    'enum': ["choice_1", "choice_2", "choice_3"],
    'optional': True,
}

# IP FIELD
ip_field = forms.IPAddressField(   label="IP Address Field",
                                   help_text="This is an IP address field")
                                       

ip_field_js = {
    'type': 'string', 
    'title': 'IP Address Field',
    'description': 'This is an IP address field', 
    'format': 'ipv4', 
    'optional': False,
}

# GENERIC IP FIELD
gen_ip_field = forms.GenericIPAddressField(label="Generic IP Address Field",
                                           help_text="This is a Generic IP address field",
                                           protocol='IPV6')

gen_ip_field_js = {
    'type': 'string', 
    'title': 'Generic IP Address Field',
    'description': 'This is a Generic IP address field', 
    'format': 'ipv6', 
}

# DATE FIELD
date_field = forms.DateField(   label="Date Field",
                                help_text="This is a date field",
                                required=False)

date_field_js = {
    'type': 'string', 
    'title': 'Date Field',
    'description': 'This is a date field', 
}

# TIME FIELD
time_field = forms.TimeField(   label="Time Field",
                                help_text="This is a time field",
                                required=False)


time_field_js = {
    'type': 'string', 
    'title': 'Time Field',
    'description': 'This is a time field', 
    'pattern':"^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$|^([0-1]?[0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
}

# DATE TIME FIELD
date_time_field = forms.DateTimeField(  label="Date-Time Field",
                                        help_text="This is a date-time field",
                                        required=False)


date_time_field_js = {
    'type': 'string', 
    'title': 'Date-Time Field',
    'description': 'This is a date-time field', 
    'format': 'date-time', 
}

# SLUG FIELD
slug_field = forms.SlugField(   label="Slug Field",
                                help_text="This is a slug field",
                                required=False,
                                max_length=100,
                                min_length=10)


slug_field_js = {
    'type': 'string', 
    'title': 'Slug Field',
    'description': 'This is a slug field', 
    'maxLength':100,
    'minLength':10
}

# URL FIELD
url_field = forms.URLField( label="URL Field",
                            help_text="This is an URL field",
                            required=False,
                            max_length=100,
                            min_length=0)


url_field_js = {
    'type': 'string', 
    'title': 'URL Field',
    'description': 'This is an URL field', 
    'maxLength':100,
    'minLength':0
}

# A FORM
class TestForm(forms.Form):
    boolean_field = boolean_field
    text_field = text_field
    text_area_field = text_area_field
    email_field = email_field
    decimal_field = decimal_field
    float_field = float_field 
    integer_field = integer_field
    choice_field = choice_field
    ip_field = ip_field
    gen_ip_field = gen_ip_field
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

    def test_schema(self):
        schema = form_to_schema(test_form)
        self.assertIsNone(Draft4Validator.check_schema(schema))

    def test_boolean_field(self):
        field_schema = field_to_schema(boolean_field)
        self.assertTrue(dict_in_dict(field_schema, boolean_field_js))

    def test_text_field(self):
        field_schema = field_to_schema(text_field)
        self.assertTrue(dict_in_dict(field_schema, text_field_js))
        
    def test_text_area_field(self):
        field_schema = field_to_schema(text_area_field)
        self.assertTrue(dict_in_dict(field_schema, text_area_field_js))
        
    def test_email_field(self):
        field_schema = field_to_schema(email_field)
        self.assertTrue(dict_in_dict(field_schema, email_field_js))
        
    def test_decimal_field(self):
        field_schema = field_to_schema(decimal_field)
        self.assertTrue(dict_in_dict(field_schema, decimal_field_js))
        
    def test_float_field(self):
        field_schema = field_to_schema(float_field)
        self.assertTrue(dict_in_dict(field_schema, float_field_js))
        
    def test_integer_field(self):
        field_schema = field_to_schema(integer_field)
        self.assertTrue(dict_in_dict(field_schema, integer_field_js))
        
    def test_choice_field(self):
        field_schema = field_to_schema(choice_field)
        self.assertTrue(dict_in_dict(field_schema, choice_field_js))
        
    def test_ip_field(self):
        field_schema = field_to_schema(ip_field)
        self.assertTrue(dict_in_dict(field_schema, ip_field_js))
        
    def test_gen_ip_field(self):
        field_schema = field_to_schema(gen_ip_field)
        self.assertTrue(dict_in_dict(field_schema, gen_ip_field_js))

    def test_date_field(self):
        field_schema = field_to_schema(date_field)
        self.assertTrue(dict_in_dict(field_schema, date_field_js))

    def test_date_field_validation(self):
        field_schema = field_to_schema(date_field)
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
        field_schema = field_to_schema(time_field)
        self.assertTrue(dict_in_dict(field_schema, time_field_js))

    def test_time_field_validation(self):
        field_schema = field_to_schema(time_field)
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
        field_schema = field_to_schema(date_time_field)
        self.assertTrue(dict_in_dict(field_schema, date_time_field_js))

    def test_slug_field(self):
        field_schema = field_to_schema(slug_field)
        self.assertTrue(dict_in_dict(field_schema, slug_field_js))

    def test_slug_field_validation(self):
        field_schema = field_to_schema(slug_field)
        self.assertIsNone(validate('th1s-is-a-v4l1d-slug', field_schema))
        try:
            validate('this_IS_not:a/valid-slug!', field_schema)
            self.fail('Invalid value was accepted')
        except ValidationError: pass

    def test_url_field(self):
        field_schema = field_to_schema(url_field)
        self.assertTrue(dict_in_dict(field_schema, url_field_js))

    def test_url_field_validation(self):
        field_schema = field_to_schema(url_field)

        self.assertIsNone(validate('http://example.org/resource.txt', field_schema))
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
        test_form.fields = {'boolean_field':boolean_field,
                            'text_field':text_field,
                            'text_area_field':text_area_field,
                            'email_field':email_field,
                            'decimal_field':decimal_field,
                            'float_field':float_field,
                            'integer_field':integer_field,
                            'choice_field':choice_field,
                            'ip_field':ip_field,
                            'gen_ip_field':gen_ip_field,
                            'date_field':date_field,
                            'time_field':time_field,
                            'date_time_field':date_time_field,
                            'slug_field':slug_field,
                            'url_field':url_field,
                        }

    def test_form_to_schema_to_form(self):
        """
        Translates a form to a schema and back to a form and checks if the 
        form fields are the same in both forms. In this case, the __django_form_field_cls
        keyword is being used as it is set in the form_to_schema function. 
        """
        schema = form_to_schema(test_form)
        recovered_form = schema_to_form(schema)
        rffi = [i[1].__class__.__name__ for i in sorted(recovered_form.fields.items())]
        tffi = [i[1].__class__.__name__ for i in sorted(test_form.fields.items())]
        self.assertEquals(rffi, tffi)

    def test_boolean_field(self):
        field = schema_to_field(boolean_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), boolean_field_js))

    def test_text_field(self):
        field = schema_to_field(text_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), text_field_js))
        
    def test_text_area_field(self):
        field = schema_to_field(text_area_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), text_area_field_js))

    def test_email_field(self):
        field = schema_to_field(email_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), email_field_js))
        
    def test_number_field(self):
        field = schema_to_field(float_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), float_field_js))
        
    def test_integer_field(self):
        field = schema_to_field(integer_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), integer_field_js))
        
    def test_choice_field(self):
        field = schema_to_field(choice_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), choice_field_js))
        
    def test_ipv4_field(self):
        ip_field_js['format'] = 'ipv4'
        field = schema_to_field(ip_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), ip_field_js))
    
    def test_ipv6_field(self):
        ip_field_js['format'] = 'ipv6'
        field = schema_to_field(ip_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), ip_field_js))
        
    def test_date_time_field(self):
        field = schema_to_field(date_time_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), date_time_field_js))
    
    def test_slug_field(self):
        field = schema_to_field(slug_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), slug_field_js))
    
    def test_url_field(self):
        field = schema_to_field(url_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), url_field_js))


