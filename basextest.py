# %%

import re
import xml.etree.ElementTree as ET
import pandas as pd
import textstat
#import numpy as np
from BaseXClient import BaseXClient
# %%
# create session
SESSION = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
try:
    QRY = SESSION.query(
        """element root { (for $x_0 in db:text("2018", "Standard Grant")/
        parent::*:Value/parent::*:AwardInstrument/parent::*:Award order by
        $x_0/descendant::*:AwardEffectiveDate empty least return element award
        { (($x_0/descendant::*:AbstractNarration, $x_0/descendant::*:
        AwardEffectiveDate)) }) }"""
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
TAG_RE = re.compile(r'<[^>]+>;')
# Parse XML into lists
ROOT = ET.fromstring(RESPONSE)
ABSTRACT = []
EFFDATE = []
for i in enumerate(ROOT):
     # apply regex then remove nsf standard verbiage
    TEMP = TAG_RE.sub(' ', ROOT[i][0].text)
    TEMP = TEMP.split(
        '''This award reflects NSF's statutory mission''', 1)[0]
    ABSTRACT.append(TEMP)
    EFFDATE.append(ROOT[i][1].text)
# place lists into dataframe for easier manipulation
DF = pd.DataFrame({'effDate': EFFDATE,
                   'abstract': ABSTRACT})
# convert from text to date
DF['effDate'] = pd.to_datetime(DF['effDate'])

# %%

STAT = []
for index, row in DF.iterrows():
    STAT.append(textstat.flesch_reading_ease(row[1]))


# %%
