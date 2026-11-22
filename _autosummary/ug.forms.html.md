# ug.forms

Working with Google Forms in Python

\*\*IMPORTANT NOTE: Getting the credentials right for this function can be tricky.
At the time of writing this, the forms API isn’t as easy as setting up than the maps or search API,
which in itself isn’t as easy as most APIs I know.
Thankfully, there’s now AI to help out with the UX mess that is the Google API credentials setup!

I won’t give instructions here, because AI will help you better than I.

Just try the function out, and get AI to help your through the credentials hell.
\*\*

### Functions

| [`dataframe_to_form`](#ug.forms.dataframe_to_form)(form_table, \*[, ...])   | Converts each row of a DataFrame into a Google Form with fields pre-populated with the row's values.   |
|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|

### ug.forms.dataframe_to_form(form_table, , field_element_types=None, field_extra_info=None, static_texts=None, client_secrets_file=None)

Converts each row of a DataFrame into a Google Form with fields pre-populated
with the row’s values.

IMPORTANT NOTE: Getting the credentials right for this function can be tricky.
At the time of writing this, the forms API isn’t as easy as setting up than the maps or search API,
which in itself isn’t as easy as most APIs I know.
Thankfully, there’s now AI to help out with the UX mess that is the Google API credentials setup!
I won’t give instructions here, because AI will help you better than I.

* **Parameters:**
  * **form_table** (pandas.DataFrame) – The DataFrame containing the form data.
  * **field_element_types** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)[`'TEXT'`, `'PARAGRAPH_TEXT'`, `'MULTIPLE_CHOICE'`, `'CHECKBOXES'`, `'DROPDOWN'`, `'DATE'`, `'TIME'`]] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Optional dict mapping fields to Google Forms element types.
  * **field_extra_info** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Optional dict mapping fields to extra information/instructions.
  * **static_texts** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`int`](https://docs.python.org/3/builtins/functions.html#int), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – Optional dict mapping positions to static text content.
* **Returns:**
  A list of dicts containing form IDs and URLs.

Example usage:

```pycon
>>> import pandas as pd
```

```pycon
>>> # Sample DataFrame
>>> data = {
...     'Name': ['Alice', 'Bob'],
...     'Age': [30, 25],
...     'Email': ['alice@example.com', 'bob@example.com']
... }
>>> df = pd.DataFrame(data)
>>>
>>> # Field types and extra info
>>> field_types = {
...     'Name': 'TEXT',
...     'Age': 'TEXT',
...     'Email': 'TEXT'
... }
>>> field_info = {
...     'Name': 'Please confirm your name.',
...     'Age': 'Please confirm your age.',
...     'Email': 'Please confirm your email address.'
... }
```

```pycon
>>> # Create forms
>>> forms = dataframe_to_form(df, field_element_types=field_types, field_extra_info=field_info)
```

```pycon
>>> # Output form URLs
>>> for form in forms:
...     print(f"Form ID: {form['form_id']}")
...     print(f"Edit URL: {form['form_edit_url']}")
...     print(f"Response URL: {form['form_response_url']}\n")
>>>
```
