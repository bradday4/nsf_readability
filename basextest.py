# %%

import re
from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
import pandas as pd
import textstat
import numpy as np
# %%
# create session
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
try:
    qry = session.query(
        """element root { (for $x_0 in db:text("2018", "Standard Grant")/parent::*:Value/parent::*:AwardInstrument/parent::*:Award order by $x_0/descendant::*:AwardEffectiveDate empty least return element award { (($x_0/descendant::*:AbstractNarration, $x_0/descendant::*:AwardEffectiveDate)) }) }""")
# run query on database
    response = qry.execute()

finally:
    # close session
    if session:
        session.close()
        del session

# %%
# unicode specific regex to remove <br/> and any other html tags
#TAG_RE = re.compile(r'&lt[^&gt]+&gt;', re.UNICODE)
TAG_RE = re.compile(r'<[^>]+>;')
# Parse XML into lists
root = ET.fromstring(response)
abstract = []
effDate = []
for i in range(len(root)):
     # apply regex then remove nsf standard verbiage
    temp = TAG_RE.sub(' ', root[i][0].text)
    temp = temp.split(
        '''This award reflects NSF's statutory mission''', 1)[0]
    abstract.append(temp)
    effDate.append(root[i][1].text)
# place lists into dataframe for easier manipulation
df = pd.DataFrame({'effDate': effDate,
                   'abstract': abstract})
# convert from text to date
df['effDate'] = pd.to_datetime(df['effDate'])
# %%

stat = []
for index, row in df.iterrows():
     stat.append(textstat.flesch_reading_ease(row[1]))


#%%
