from django.test import TestCase
from django import forms

from schemulator import form_to_schema, field_to_schema, schema_to_form, schema_to_field
 

# A form to test 
TestForm = forms.Form()

# A schema to test
schema = {
    'title': u'JSON Schema',
    'description': u'This is a JSON Schema describing a form',
    'type': 'object', 
    'properties': {}
}

# These are FIELDS to test within the form and their equivalent representation
# as PROPERTIES within the schema

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
float_field = forms.FloatField(   label="Float Field",
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
    'type': 'array', 
    'title': 'Choice Field',
    'description': 'This is a choice field', 
    'items': [{'enum': ["choice_1", "choice_2", "choice_3"]}],
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
date_field = forms.DateField(  label="Date Field",
                               help_text="This is a date field")

date_field_js = {
    'type': 'string', 
    'title': 'Date Field',
    'description': 'This is a date field', 
}

# DATE TIME FIELD
date_time_field = forms.DateTimeField(  label="Date-Time Field",
                                        help_text="This is a date-time field")

date_time_field_js = {
    'type': 'string', 
    'title': 'Date-Time Field',
    'description': 'This is a date-time field', 
    'format': 'date-time', 
}


def dict_in_dict(d, subset_d):
    """
    Checks if the items in a dictionary are all contained within some other
    dictionary. This is used to check if the schema created contains all the
    expected information.
    """
    return all([i in d.items() for i in subset_d.items()])

class FormToSchemaTestCase(TestCase):
    
    def setUp(self):
        TestForm.base_fields = {} 

    def test_schema(self):
        TestForm.base_fields = {'boolean_field':boolean_field,
                                'text_field':text_field, }
        schema = form_to_schema(TestForm)
    
    def test_boolean_field(self):
        field_schema = field_to_schema(boolean_field)
        self.assertTrue(dict_in_dict(field_schema, boolean_field_js))

    def test_text_field(self):
        field_schema = field_to_schema(text_field)
        self.assertTrue(dict_in_dict(field_schema, text_field_js))
        
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
        choice_field_copy = choice_field_js.copy()
        it1 = choice_field_copy.pop('items')[0]
        it2 = field_schema.pop('items')[0]
        self.assertTrue(dict_in_dict(it2, it1))
        self.assertTrue(dict_in_dict(field_schema, choice_field_copy))
        
    def test_ip_field(self):
        field_schema = field_to_schema(ip_field)
        self.assertTrue(dict_in_dict(field_schema, ip_field_js))
        
    def test_gen_ip_field(self):
        field_schema = field_to_schema(gen_ip_field)
        self.assertTrue(dict_in_dict(field_schema, gen_ip_field_js))
        
    def test_date_field(self):
        field_schema = field_to_schema(date_field)
        self.assertTrue(dict_in_dict(field_schema, date_field_js))
        
    def test_date_time_field(self):
        field_schema = field_to_schema(date_time_field)
        self.assertTrue(dict_in_dict(field_schema, date_time_field_js))
        

class SchemaToFormTestCase(TestCase):

    TestSchema = {}
    
    def setUp(self):
        pass

    def test_boolean_field(self):
        field = schema_to_field(boolean_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), boolean_field_js))

    def test_text_field(self):
        field = schema_to_field(text_field_js)
        self.assertTrue(dict_in_dict(field_to_schema(field), text_field_js))
        
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
        field_schema = field_to_schema(choice_field)
        choice_field_copy = choice_field_js.copy()
        it1 = choice_field_copy.pop('items')[0]
        it2 = field_schema.pop('items')[0]
        self.assertTrue(dict_in_dict(it2, it1))
        self.assertTrue(dict_in_dict(field_to_schema(field), choice_field_copy))
        
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

