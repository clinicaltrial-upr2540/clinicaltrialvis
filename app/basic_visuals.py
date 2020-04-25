import json 
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.sql import text 
import io 
import matplotlib.pyplot as plt

from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

def get_plot_png_test(compound_name, engine): 
    return "test successful" 

def get_compounds_data(engine): 

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

    data = [dict(row) for row in dataset]
    return data 


def get_compound_data(compound_name, engine): 
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

    compound_data = [dict(row) for row in compound_dataset]
    return compound_data 


def get_plot_png(compound_name, engine): 

    compound_data = get_compound_data(compound_name, engine) 
    if len(compound_data ) == 0: 
        return "Compound not found" 
    compound_dict = compound_data[0]

    data = get_compounds_data(engine) 
    df = pd.DataFrame(data)

    # get distinct therapeutic groups 
    ther_codes = df["therapeutic_code"].unique()

    # make a new dataframe for therapeutic group histograms by looping
    ther_objs = []

    for code in ther_codes: 
        ther_df = df[df["therapeutic_code"]==code]
        ther_dict = {"ther_code": code, "ther_df": ther_df}
        ther_objs.append(ther_dict)

    # plot same therapeutic group, different descriptors 
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15), constrained_layout=True)
    list_o_axes = axes.flatten()


    # get compound's therapeutic group 

    compound_ther_code = compound_dict.get("therapeutic_code")
    for obj in ther_objs: 
        ther_code = obj.get("ther_code")
        if ther_code == compound_ther_code:  
            fig.suptitle(f"{compound_name}'s Therap Group {ther_code} Compound Descriptors", fontsize=15)
            break 
        fig.suptitle("Compound Descriptors", fontsize=15)

    ther_obj = ther_objs[0]
    ther_df = ther_obj.get("ther_df")
    ther_code = ther_obj.get("ther_code")

    # prep the compound in question
    if compound_dict.get("bioavailability") == '1': 
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
            dot_x=[float(compound_dict.get(descriptor))]
            dot_y=[-1]
            ax.scatter(dot_x, dot_y, color=compound_color)
            ax.set_title(f"{descriptor} of thera code {ther_code}")
        except TypeError as e: 
            print(e)
        i+=1 


    # plt.show()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue()) 
    response.mimetype = 'image/png'
    return response 
