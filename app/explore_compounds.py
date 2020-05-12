import pandas as pd
from sqlalchemy.sql import text
import io
from flask import make_response

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Set TkAgg backend on MacOS to prevent crashes
from sys import platform

if platform == 'darwin':
    import matplotlib

    matplotlib.use("TkAgg")

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


def get_descriptor_payload(compound_name):
    request_payload = {
        "data_list":
            [

                {
                    "view_name": "compounds",
                    "column_list":
                        [
                            "molecular_weight",
                            "clogp",
                            "hbd",
                            "hba",
                            "psa",
                            "apka",
                            "aromatic_rings",
                            "rotatable_bonds",
                        ],
                    "filters":
                        [
                            {
                                "column_name": "compound_name",
                                "operator": "matches",
                                "target": compound_name,
                            }
                        ]
                }
            ],
        "join_style": "left",
        "export": "false",
        "single_file": "true",
        "limit": 1
    }

    return request_payload


def get_similar_dict(engine, compound_name, descriptor_dict):
    similar_dict = {}

    for descriptor in descriptors:
        descriptor_similar_list = get_similar_compounds_by_descriptor(engine, compound_name, descriptor)
        similar_dict[descriptor] = descriptor_similar_list

    return similar_dict


def get_plot_png_test(compound_name, engine):
    return "test successful"


def get_similar_compounds_by_descriptor(engine, compound_name, descriptor):
    params = {"compound_name": compound_name}

    sql_str = f"""
        WITH refs AS
        (
          SELECT DISTINCT compound_name,
                 "{descriptor}"::float, 
                 therapeutic_code
          FROM curated.compounds
          WHERE compound_name LIKE :compound_name
        ), 
        group_stats as (
          select * from curated.compound_statistics 
          WHERE therapeutic_code in (select therapeutic_code from refs) 
        ), 
        theragroup as 
        (
          select distinct compound_name,
                 "{descriptor}"::float, 
                 therapeutic_code
          FROM curated.compounds
          WHERE therapeutic_code in (select therapeutic_code from refs) 
        ), 
        stats as (
        SELECT 
        theragroup.compound_name, 
        atc_level_4,
        theragroup."{descriptor}", 
        abs((refs."{descriptor}"-theragroup."{descriptor}")/group_stats."stddev_{descriptor}") as norm_diff, 
        refs.therapeutic_code
        from refs 
        inner join theragroup on ( theragroup.therapeutic_code = refs.therapeutic_code) 
        inner join group_stats on ( group_stats.therapeutic_code = refs.therapeutic_code)
        ), 
        ranked as (
        select 
        *, 
        rank() over (PARTITION BY therapeutic_code ORDER BY norm_diff) as rank_w_in_group
         from 
        stats 
        ) 
        select 
        compound_name, 
        CASE when  TRUNC("{descriptor}"::numeric) <> "{descriptor}"::numeric THEN round("{descriptor}"::numeric, 3) ELSE "{descriptor}" END,  
        CASE when TRUNC(norm_diff::numeric, 3) <> norm_diff::numeric THEN round(norm_diff::numeric, 3) ELSE norm_diff END AS difference_score,
        atc_level_4
        from ranked where rank_w_in_group < 5
        order by therapeutic_code, rank_w_in_group, norm_diff
        limit 10
        ; 
        """
    with engine.connect() as conn:
        cursor = conn.execute(text(sql_str), params)

    data = [dict(row) for row in cursor]
    return data


def get_ba_dict(engine, compound_name):
    sql_str = """
            SELECT 
            DISTINCT 
            bioavailability::bool as drugank_is_BA_truefalse, 
            bioavailability_percent as freetext_BA_lookup, 
            bioavailability_percent as predicted_BA_percent_if_possible
            FROM curated.compound 
            WHERE compound_name ILIKE :compound_name
            """
    params = {"compound_name": compound_name}

    with engine.connect() as conn:
        cursor = conn.execute(text(sql_str), params)

    results = [dict(row) for row in cursor]

    return results


def get_compounds_data(engine):
    with engine.connect() as conn:
        dataset = conn.execute("""
        select 
            -- smiles,
            substring(atc_code, 1, 1) as therapeutic_code, 
            compound_name, 
            bioavailability, 
            TRUNC(molecular_weight::numeric, 3) as molecular_weight, 
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
            TRUNC(molecular_weight::numeric, 3) as molecular_weight, 
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
    if len(compound_data) == 0:
        return "Compound not found"
    compound_dict = compound_data[0]

    data = get_compounds_data(engine)
    df = pd.DataFrame(data)

    # get distinct therapeutic groups
    ther_codes = df["therapeutic_code"].unique()

    # make a new dataframe for therapeutic group histograms by looping
    ther_objs = []

    for code in ther_codes:
        ther_df = df[df["therapeutic_code"] == code]
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
            ther_obj = obj
            break
        fig.suptitle("Compound Descriptors", fontsize=15)

    if compound_ther_code is None:
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
        ba_plot_df = plot_df[ther_df["bioavailability"] == '1']
        nba_plot_df = plot_df[ther_df["bioavailability"] == '0']
        try:
            ax.hist(ba_plot_df, 10, color='blue', alpha=0.1)
            ax.hist(nba_plot_df, 10, color='red', alpha=0.2)
            dot_x = [float(compound_dict.get(descriptor))]
            dot_y = [-1]
            ax.scatter(dot_x, dot_y, color=compound_color)
            ax.set_title(f"{descriptor} of thera code {ther_code}")
        except TypeError as e:
            print(e)
        i += 1

        # plt.show()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
