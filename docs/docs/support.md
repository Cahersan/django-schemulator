## What's Supported?

&nbsp;

#### Django Form to JSON Schema

&nbsp;

A Django Form containing any number of the following Django Forms field classes.
 
* `BooleanField` 
* `CharField`	
* `ChoiceField`
* `DateField`	
* `TimeField`
* `DateTimeField`	
* `DecimalField`	
* `EmailField`	
* `FloatField`	
* `IntegerField`	
* `IPAddressField`	
* `GenericIPAddressField`
* `SlugField`
* `URLField`

&nbsp;

These field take a series of arguments. Here is a list of the field arguments supported so far:

__Arguments common to all field classes__

* `help_text`
* `label`
* `initial`
* `required`

__Arguments common to string-based field classes__

* `min_length`
* `max_length`

__Arguments common to number-based field classes__

* `min_value`
* `max_value`

__ChoiceField argument__

* `choices`

&nbsp;

#### WTForm to JSON Schema

&nbsp;

A WTForm containing any of the following WTForms field classes.

* `BooleanField`
* `DateField`
* `DateTimeField`
* `DecimalField`
* `FloatField` 
* `IntegerField`
* `RadioField`
* `SelectField`
* `SelectMultipleField`
* `StringField`
* `TextField` (deprecated, will be removed in WTForms 3.0)
* `TextAreaField`

Unsupported:

* `Field`
* `FieldList`
* `FileField`
* `FormField`
* `HiddenField`
* `PasswordField`
* `SelectFieldBase`
* `SubmitField`

These field take a series of __arguments__. Here is a list of the field arguments supported so far:

* `description`
* `label`
* `default`
* `validators`

The following __validators__ are supported:

* `Length`
* `NumberRange`
* `Optional`
* `Regexp`

