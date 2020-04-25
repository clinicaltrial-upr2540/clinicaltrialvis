#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json 
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.sql import text 
import matplotlib.pyplot as plt

from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser


# In[3]:


config = ConfigParser()
config.read("database.conf")
config.sections()
host = config["drugdata"]["host"]
port = config["drugdata"]["port"]
database = config["drugdata"]["database"]
user = config["drugdata"]["user"]
password = config["drugdata"]["password"]
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = sqlalchemy.create_engine(DATABASE_URL)


# In[10]:


# set up descriptors 

descriptors = [
    'molecular_weight', 
     'clogp',
        'hbd',
        'hba',
        'psa',
        'apka',
        'aromatic_rings',
        'rotatable_bonds'
]

compound_name = 'Leuprolide'
# compound_name = 'Phenylalanine'


# In[11]:


with engine.connect() as conn: 
    dataset = conn.execute("""
    select 
        -- smiles,
        substring(atc_code, 1, 1) as therapeutic_code, 
        compound_name, 
        bioavailability, 
        molecular_weight, 
        clogp,
        hbd,
        hba,
        psa,
        apka,
        -- fsp3, 
        aromatic_rings,
        rotatable_bonds
    from curated.compounds
    where molecular_weight is not null 
        and clogp is not null 
        and hbd is not null
        and hba is not null 
        and psa is not null 
        and apka is not null
        and aromatic_rings is not null
        and rotatable_bonds is not null 
    """)

with engine.connect() as conn: 
    compound_dataset = conn.execute(text("""
    select 
        smiles,
        substring(atc_code, 1, 1) as therapeutic_code, 
        compound_name, 
        bioavailability, 
        molecular_weight, 
        clogp,
        hbd,
        hba,
        psa,
        apka,
        -- fsp3, 
        aromatic_rings,
        rotatable_bonds
    from curated.compounds
    where compound_name like :compound_name
    """), {"compound_name": compound_name})


# In[12]:


data = [dict(row) for row in dataset]
compound_data = [dict(row) for row in compound_dataset][0]
compound_data


# In[13]:


df = pd.DataFrame(data)
df.head()


# In[14]:


# get distinct therapeutic groups 
ther_codes = df["therapeutic_code"].unique()

# make a new dataframe for therapeutic group histograms by looping
ther_objs = []

for code in ther_codes: 
    ther_df = df[df["therapeutic_code"]==code]
    ther_dict = {"ther_code": code, "ther_df": ther_df}
    ther_objs.append(ther_dict)


# In[15]:


# plot same therapeutic group, different descriptors 
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15), constrained_layout=True)
list_o_axes = axes.flatten()

fig.suptitle("Information about Therap Group 1", fontsize=15)

# get a therapeutic group 

ther_obj = ther_objs[0]
ther_df = ther_obj.get("ther_df")
ther_code = ther_obj.get("ther_code")

# prep the compound in question
if compound_data.get("bioavailability") == '1': 
    compound_color = "blue"
else: 
    compound_color = 'red'
    
# create a subplot for that descriptor
i = 0
for descriptor in descriptors: 
    ax = list_o_axes[i]
    plot_df = pd.to_numeric(ther_df[descriptor])
    ba_plot_df = plot_df[ther_df["bioavailability"]=='1']
    nba_plot_df = plot_df[ther_df["bioavailability"]=='0']
    try: 
        ax.hist(ba_plot_df, 10, color='blue', alpha=0.1)
        ax.hist(nba_plot_df, 10, color='red', alpha=0.2)
        dot_x=[float(compound_data.get(descriptor))]
        dot_y=[-1]
        ax.scatter(dot_x, dot_y, color=compound_color)
        ax.set_title(f"{descriptor} of thera code {ther_code}")
    except TypeError as e: 
        print(e)
    i+=1 


plt.show()


# In[ ]:




