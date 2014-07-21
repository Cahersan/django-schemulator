from django.test import TestCase
from django import forms

from schemulator import form_to_schema
        
class TestForm(forms.Form):

#    boolean_field = forms.BooleanField( label="Boolean Field",
#                                        help_text="This is a boolean field",
#                                        initial=True,
#                                        required=False)
#
#    text_field = forms.CharField(   label="Text Field",
#                                    help_text="This is a text field",
#                                    required=False,
#                                    max_length=100,
#                                    min_length=20)
#
#    email_field = forms.EmailField( label="Email Field",
#                                    help_text="This is an email field",
#                                    initial="email@example.com",
#                                    max_length=100,
#                                    required=False)
#
#    decimal_field = forms.DecimalField( label="Decimal Field",
#                                        help_text="This is a decimal field",
#                                        initial=10.04,
#                                        max_value=100,
#                                        min_value=0,
#                                        required=False)
#
#    integer_field = forms.IntegerField( label="Integer Field",
#                                        help_text="This is an integer field",
#                                        initial=10,
#                                        max_value=100,
#                                        min_value=0,
#                                        required=False)

    choice_field = forms.ChoiceField(   label="Choice Field",
                                        help_text="This is choice field",
                                        choices=["choice_1", "choice_2", "choice_3"],
                                        required=False)


schema = {
    'description': 'a test schema',
    'properties': {
        'email': {
            'default': None,
            'description': 'an email field',
            'format': 'email',
            'null': False,
            'optional': False,
            'pattern': None,
            'properties': {},
            'title': 'email',
            'type': 'string'
        },
        'text': {
            'default': None,
            'description':'a text field',
            'null': False,
            'optional': False,
            'pattern': None,
            'properties': {},
            'title': 'text',
            'type': 'string'}
    },
    'title': 'TestForm',
    'type': 'object'
}


class FormToSchemaTestCase(TestCase):

    def SetUp(self):
        pass

    def test_stuff(self):
        schema = form_to_schema(TestForm)
        print schema
