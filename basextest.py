# %%

import xml.etree.ElementTree as ET
import pandas as pd
import textstat
import abstract_cleanup as AC
#import numpy as np
from BaseXClient import BaseXClient
# %%
# create session
SESSION = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
try:
    QRY = SESSION.query(
        """element root { (for $x_1 in db:text("nsf_awards", "Standard Grant")/
        parent::*:Value/parent::*:AwardInstrument/parent::*:Award order by 
        $x_1/descendant::*:AwardEffectiveDate empty least return 
        if(((normalize-space(((: xs:string?, true :) $x_1/descendant::*:AbstractNarration)) != "") 
        and (normalize-space(((: xs:string?, true :) $x_1/descendant::*:AwardEffectiveDate)) != ""))) 
        then element award { (($x_1/descendant::*:AbstractNarration, $x_1/descendant::*:AwardEffectiveDate)) } 
        else ()) }"""
        )
# run query on database
    RESPONSE = QRY.execute()

finally:
    # close session
    if SESSION:
        SESSION.close()
        del SESSION

# %%
# unicode specific regex to remove <br/> and any other html tags
#TAG_RE = re.compile(r'&lt[^&gt]+&gt;', re.UNICODE)

# Parse XML into lists
ROOT = ET.fromstring(RESPONSE)
ABSTRACT = []
EFFDATE = []
for i in range(len(ROOT)):
     # apply regex then remove nsf standard verbiage
    TEMP = ROOT[i][0].text
    TEMP = AC.cleanup_pretagger_all(TEMP)
    ABSTRACT.append(TEMP)
    EFFDATE.append(ROOT[i][1].text)
# place lists into dataframe for easier manipulation
DF = pd.DataFrame({'effDate': EFFDATE,
                   'abstract': ABSTRACT})
# convert from text to date
DF['effDate'] = pd.to_datetime(DF['effDate'])
# drop duplicate abstracts from dataset
DF.drop_duplicates(subset= 'abstract',keep='first', inplace=True)
# %%
with open('cleaned_abstracts.txt', 'w', encoding='utf-8') as text_file:
    for abstract in DF['abstract']:
        text_file.write(abstract+'\n\n')
STAT = []
for index, row in DF.iterrows():
    STAT.append(textstat.flesch_reading_ease(row[1]))


# %%
