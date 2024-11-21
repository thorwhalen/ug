"""
Working with Google Forms in Python

**IMPORTANT NOTE: Getting the credentials right for this function can be tricky.
At the time of writing this, the forms API isn't as easy as setting up than the maps or search API, 
which in itself isn't as easy as most APIs I know. 
Thankfully, there's now AI to help out with the UX mess that is the Google API credentials setup!

I won't give instructions here, because AI will help you better than I. 

Just try the function out, and get AI to help your through the credentials hell.
**


"""

from typing import Optional, Dict
from typing import Literal
import os

import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


# Define valid Google Forms element types
ElementType = Literal[
    'TEXT',
    'PARAGRAPH_TEXT',
    'MULTIPLE_CHOICE',
    'CHECKBOXES',
    'DROPDOWN',
    'DATE',
    'TIME',
]
Field = str
ExtraInfo = str


def dataframe_to_form(
    form_table: 'pandas.DataFrame',
    field_element_types: Optional[Dict[Field, ElementType]] = None,
    field_extra_info: Optional[Dict[Field, ExtraInfo]] = None,
    client_secrets_file: Optional[str] = None,
):
    r"""
    Converts each row of a DataFrame into a Google Form with fields pre-populated
    with the row's values.

    IMPORTANT NOTE: Getting the credentials right for this function can be tricky.
    At the time of writing this, the forms API isn't as easy as setting up than the maps or search API,
    which in itself isn't as easy as most APIs I know.
    Thankfully, there's now AI to help out with the UX mess that is the Google API credentials setup!
    I won't give instructions here, because AI will help you better than I.

    :param form_table: The DataFrame containing the form data.
    :param field_element_types: Optional dict mapping fields to Google Forms element types.
    :param field_extra_info: Optional dict mapping fields to extra information/instructions.
    :return: A list of dicts containing form IDs and URLs.

    Example usage:

    >>> import pandas as pd  # doctest: +SKIP

    >>> # Sample DataFrame
    >>> data = {
    ...     'Name': ['Alice', 'Bob'],
    ...     'Age': [30, 25],
    ...     'Email': ['alice@example.com', 'bob@example.com']
    ... }
    >>> df = pd.DataFrame(data)  # doctest: +SKIP
    >>>
    >>> # Field types and extra info
    >>> field_types = {    # doctest: +SKIP
    ...     'Name': 'TEXT',
    ...     'Age': 'TEXT',
    ...     'Email': 'TEXT'
    ... }
    >>> field_info = {
    ...     'Name': 'Please confirm your name.',
    ...     'Age': 'Please confirm your age.',
    ...     'Email': 'Please confirm your email address.'
    ... }  # doctest: +SKIP


    >>> # Create forms
    >>> forms = dataframe_to_form(df, field_element_types=field_types, field_extra_info=field_info)  # doctest: +SKIP

    >>> # Output form URLs
    >>> for form in forms:  # doctest: +SKIP
    ...     print(f"Form ID: {form['form_id']}")
    ...     print(f"Edit URL: {form['form_edit_url']}")
    ...     print(f"Response URL: {form['form_response_url']}\n")
    >>>

    """

    import pandas as pd

    if not client_secrets_file:
        if not (client_secrets_file := os.getenv('HFN_GOOGLE_CLIENT_JSON_PATH')):
            raise ValueError(
                'Please set the HFN_GOOGLE_CLIENT_JSON_PATH environment variable to the path of your Google client JSON file.'
            )

    def authenticate():
        # Authenticate and build the Google Forms API service
        SCOPES = ['https://www.googleapis.com/auth/forms.body']
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('forms', 'v1', credentials=creds)
        return service

    def create_question_item(question_title, question_type, extra_info):
        # Map the question_type to Google Forms API item types
        question_item = {}
        if question_type == 'TEXT':
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "description": extra_info,
                        "questionItem": {"question": {"textQuestion": {}}},
                    },
                    "location": {"index": 0},
                }
            }
        elif question_type == 'PARAGRAPH_TEXT':
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "description": extra_info,
                        "questionItem": {"question": {"paragraphQuestion": {}}},
                    },
                    "location": {"index": 0},
                }
            }
        elif question_type in ['MULTIPLE_CHOICE', 'CHECKBOXES', 'DROPDOWN']:
            # Extract options from extra_info, if provided
            options = (
                [{"value": opt.strip()} for opt in extra_info.split(',')]
                if extra_info
                else [{"value": "Option 1"}, {"value": "Option 2"}]
            )
            choice_type = {
                'MULTIPLE_CHOICE': 'RADIO',
                'CHECKBOXES': 'CHECKBOX',
                'DROPDOWN': 'DROP_DOWN',
            }[question_type]
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "questionItem": {
                            "question": {
                                "choiceQuestion": {
                                    "type": choice_type,
                                    "options": options,
                                }
                            }
                        },
                    },
                    "location": {"index": 0},
                }
            }
        elif question_type == 'DATE':
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "description": extra_info,
                        "questionItem": {"question": {"dateQuestion": {}}},
                    },
                    "location": {"index": 0},
                }
            }
        elif question_type == 'TIME':
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "description": extra_info,
                        "questionItem": {"question": {"timeQuestion": {}}},
                    },
                    "location": {"index": 0},
                }
            }
        else:
            # Default to TEXT if unknown type
            question_item = {
                "createItem": {
                    "item": {
                        "title": question_title,
                        "description": extra_info,
                        "questionItem": {"question": {"textQuestion": {}}},
                    },
                    "location": {"index": 0},
                }
            }
        return question_item

    # Authenticate with the Google Forms API
    service = authenticate()

    forms_info = []

    for index, row in form_table.iterrows():
        # Create a new form for each row
        form_title = f"Form for Row {index + 1}"
        form = {"info": {"title": form_title, "documentTitle": form_title}}
        form_response = service.forms().create(body=form).execute()
        form_id = form_response['formId']

        requests = []

        for field in form_table.columns:
            existing_value = row[field]
            if pd.isna(existing_value):
                existing_value = ''
            else:
                existing_value = str(existing_value)

            question_type = (
                field_element_types.get(field, 'TEXT')
                if field_element_types
                else 'TEXT'
            )
            extra_info = field_extra_info.get(field, '') if field_extra_info else ''

            # Include existing value in the question description
            question_title = f"{field}"
            question_description = (
                f"{extra_info}\nCurrent value: {existing_value}"
                if extra_info
                else f"Current value: {existing_value}"
            )

            question_item = create_question_item(
                question_title, question_type, question_description
            )
            requests.append(question_item)

        # Update the form with the new questions
        body = {'requests': requests}
        service.forms().batchUpdate(formId=form_id, body=body).execute()

        # Collect form information
        forms_info.append(
            {
                'form_id': form_id,
                'form_edit_url': f"https://docs.google.com/forms/d/{form_id}/edit",
                'form_response_url': f"https://docs.google.com/forms/d/{form_id}/viewform",
            }
        )

    return forms_info
