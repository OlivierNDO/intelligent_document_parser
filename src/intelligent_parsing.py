"""
Module for few-shot text generation
"""

### Configuration and Imports
##########################################################################################################
# Imports
import ast
import datetime
from dotenv import load_dotenv
import json
import nlpcloud
import os
import pandas as pd
import re
import tqdm

# Script configuration
load_dotenv()


### Define functions and classes
##########################################################################################################
def generate_few_shot_string(input_text : str):
    out_str = f"""
    Input:
    This morning, I decided to go for a walk in the park. The weather was lovely, and I stopped by the cafe for a cup of coffee.
    After that, I visited the bookstore nearby and bought a new novel. The day went by peacefully without any issues or disturbances.
    I returned home and spent the afternoon reading and relaxing.
    Output:
        {{
            'arrest_made': 'Unknown',
            'injury_reported': 'Unknown',
            'three_or_more_vehicles': 'Unknown',
            'police_report_filed': 'Unknown',
            'ticket_given': 'Unknown'
        }}
    ###

    Input:
    Incident Report #34567
    I was driving home when another vehicle hit me from behind at the traffic light.
    It was around 5:30 PM on a Tuesday. The police arrived shortly after and took our statements.
    The other driver seemed fine, but my back was a bit sore.
    They gave the other driver a ticket because he wasn't paying attention.
    I don't think anyone was arrested, and there were only two cars involved.
    Output:
        {{
            'arrest_made': 'Unknown',
            'injury_reported': 'True',
            'three_or_more_vehicles': 'False',
            'police_report_filed': 'True',
            'ticket_given': 'True'
        }}
    ###

    Input:
    Witness Statement:
    I was waiting at the intersection when I saw two cars collide. The accident occurred at around 3 PM. 
    An ambulance arrived at the scene shortly after, but I don't think anyone was seriously hurt.
    The police were there too, but I don't know if they filed a report.
    I didn't see anyone being arrested, but I did hear one of the drivers got a ticket for speeding.
    Output:
        {{
            'arrest_made': 'Unknown',
            'injury_reported': 'False',
            'three_or_more_vehicles': 'False',
            'police_report_filed': 'Unknown',
            'ticket_given': 'True'
        }}
    ###

    Input:
    {input_text}
    Output:
    """
    return out_str



class IntelligentDocumentParser:
    def __init__(self,
                 api_token = os.getenv('token'),
                 model = 'gpt-j',
                 use_gpu = True):
        self.api_token = api_token
        self.model = model
        self.use_gpu = use_gpu
        self._get_client()

    def _get_client(self):
        self.client = nlpcloud.Client(self.model, self.api_token, gpu = self.use_gpu)

    def parse(self, input_string : str):

        model_input = generate_few_shot_string(input_string)
        generation = self.client.generation(
            model_input,
            length_no_input=True,
            end_sequence='###',
            remove_end_sequence=True,
            remove_input=True)
        generated_text = generation['generated_text'].strip()
        try:
            record_dict = ast.literal_eval(generated_text)
            return record_dict
        except (SyntaxError, ValueError) as e:
            print(f'Error parsing string to dictionary: {e}')




int_parser = IntelligentDocumentParser()

new_str = """
Participant / Witness Statement
ACCIDENT REPORT 987654321
Name: Nick Olivier
When did the accident occur?
    Today at 4pm.
Did any emergency services come to the scene?
    Yea - California Highway Patrol. They wrote a report.  

Did anyone go to the hospital or receive treatment at the scene?
    An ambulance arrived a bit later, but no, they shouldn't have even come. Everyone is fine.

Is there anything else you want to mention?
    Cop gave the other driver a speeding ticket for driving 45 in a 20, so they should be at fault.
"""

output_record = int_parser.parse(new_str)
print(output_record)

#print(os.environ)
