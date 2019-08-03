# -*- coding: utf-8 -*-
'''
Query baseX database and generating dataframe of abstracts
'''
# %%
from time import time
import xml.etree.ElementTree as ET
import pandas as pd
import textstat
from BaseXClient import BaseXClient
import abstract_cleanup as AC

# %%
# create session
SESSION = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
try:
    QRY = SESSION.query(
        """element root { (for $x_1 in db:text("nsf_awards", "Standard Grant")/
        parent::*:Value/parent::*:AwardInstrument/parent::*:Award order by
         $x_1/descendant::*:AwardEffectiveDate empty least return
         if(((normalize-space(((: xs:string?, true :)
         $x_1/descendant::*:AbstractNarration)) != "")
         and (normalize-space(((: xs:string?, true :)
         $x_1/descendant::*:AwardEffectiveDate)) != "")))
         then element award { (($x_1/descendant::*:AbstractNarration,
         $x_1/descendant::*:AwardEffectiveDate)) }
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
# Parse XML into lists
ROOT = ET.fromstring(RESPONSE)
start = time()
ABSTRACT = [AC.cleanup_pretagger_all(i.text) for i in ROOT.iter(tag='AbstractNarration')]
print('\n'+f"Total time to download: {time() - start}")

EFFDATE = [i.text for i in ROOT.iter(tag='AwardEffectiveDate')]

# place lists into dataframe for easier manipulation
DF = pd.DataFrame({'effDate': EFFDATE,
                   'abstract': ABSTRACT})
# convert from text to date
DF['effDate'] = pd.to_datetime(DF['effDate'])
# drop duplicate abstracts from dataset
DF.drop_duplicates(subset='abstract', keep='first', inplace=True)
# %%
with open('cleaned_abstracts.txt', 'w', encoding='utf-8') as text_file:
    for abstract in DF['abstract']:
        text_file.write(abstract+'\n\n')
# STAT_FLESCH = []
# STAT_NDC = []
STAT_CONSENSUS = []
for index, row in DF.iterrows():
    # STAT_FLESCH.append(textstat.flesch_reading_ease(row[1]))
    # STAT_NDC.append(textstat.dale_chall_readability_score(row[1]))
    STAT_CONSENSUS.append(textstat.text_standard(row[1], float_output=True))


# %%
