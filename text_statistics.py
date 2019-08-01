# -*- coding: utf-8 -*-
'''
Run stats on abstracts and generate plots
'''
# %%
import numpy as np
import matplotlib.pyplot as plt

# %%

YEARS = DF['effDate'].dt.strftime("%Y").astype(int).to_numpy()
XMIN = YEARS.min()
XMAX = YEARS.max()
CMIN = DF['statConsensus'].min()
CMAX = DF['statConsensus'].max()
NDCMIN = DF['statNDC'].min()
NDCMAX = DF['statNDC'].max()

FIG, AXS = plt.subplots(ncols=2, sharey=False, figsize=(7, 4))
FIG.subplots_adjust(hspace=0.5, left=0.07, right=1)
AX = AXS[0]
HB = AX.hist(DF['statConsensus'], bins=100)
AX.set(xlim=(CMIN, CMAX))
AX.set_title("Consensus Stats")
# CB = FIG.colorbar(HB, ax=AX)
#CB.set_label('counts')

AX = AXS[1]
HB = AX.hexbin(YEARS, DF['statConsensus'], gridsize=200, cmap='inferno')
AX.set(xlim=(XMIN, XMAX), ylim=(CMIN, 30))
AX.set_title("NDC Consensus Stats")
CB = FIG.colorbar(HB, ax=AX)
CB.set_label('counts')

plt.show()

#%%
