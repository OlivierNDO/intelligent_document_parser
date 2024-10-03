"""


"""

### Configuration and Imports
##########################################################################################################
import datetime
import json
import nlpcloud
import pandas as pd
import re
import tqdm

from src import text_extraction as te
from src import intelligent_parsing as ip





extractor = te.FileTextExtractor()
intelligent_parser = ip.IntelligentDocumentParser()



extracted_text = extractor.extract_text('./data/n.o. witness participant statement.pdf')
output_record = intelligent_parser.parse(extracted_text)
print(output_record)

#print(extractor.extract_text('./data/n.o. witness participant statement.pdf'))

#print(extractor.extract_text('./data/email_screen_shot.png'))













