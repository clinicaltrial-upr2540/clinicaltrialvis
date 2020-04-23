#!/usr/bin/env python3

# This module imports information about the visualizations included with the application
# as a demonstration for applications of the dataset

import sqlalchemy

from configparser import ConfigParser

visualization_list = [
    {
        "name": "radar",
        "title": "Drug Targets by Companies",
        "description": "Radar Chart",
        "thumbnail": "radar.png",
        "classes": "radarChart",
        "dataset": "cdcdata",
        "data_format": "json",
        "scripts": "chartSetup.js,dotMatrix.js,radarChart.js"
    },
    {
        "name": "dotmatrix",
        "title": "Drug Targets by Companies",
        "description": "Dot Matrix Diagram",
        "thumbnail": "dotmatrix.png",
        "classes": "dotMatrixChart",
        "dataset": "cdcdata",
        "data_format": "json",
        "scripts": "chartSetup.js,dotMatrix.js,radarChart.js"
    },
    {
        "name": "3d_bubbles",
        "title": "Molecular Descriptors",
        "description": "3D Bubble Chart",
        "thumbnail": "3d_bubbles.png",
        "classes": "bubble-plot-3d",
        "dataset": "splomdata",
        "data_format": "csv",
        "scripts": "bubble_plot_3d.js"
    },
    {
        "name": "box-whisker",
        "title": "Drug Targets by Companies",
        "description": "Box and Whisker Chart",
        "thumbnail": "box-whisker.png",
        "classes": "box-whisker-plotly",
        "dataset": "heatmapdata",
        "data_format": "csv",
        "scripts": "box_whisker_plotly.js"
    },
    {
        "name": "heatmap",
        "title": "Drug Targets by Companies",
        "description": "Heat Map",
        "thumbnail": "heatmap.png",
        "classes": "heatmap,dataset-picker",
        "dataset": "heatmapdata",
        "data_format": "csv",
        "scripts": "heatmap.js"
    },
    {
        "name": "splom",
        "title": "Molecular Descriptors",
        "description": "Scatterplot Matrix",
        "thumbnail": "splom.png",
        "classes": "splom-plot",
        "dataset": "splomdata",
        "data_format": "csv",
        "scripts": "splom.js"
    }
]

# Import database configuration
config = ConfigParser()
config.read("database.conf")

# Set up and establish database engine
# URL format: postgresql://<username>:<password>@<hostname>:<port>/<database>
DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
SCHEMA_NAME = "application"

engine = sqlalchemy.create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Refreshing visualization data...")

    # Create the table if necessary
    conn.execute(f"set search_path to {SCHEMA_NAME};")
    conn.execute("TRUNCATE TABLE visualizations;")
    # conn.execute("CREATE TABLE visualizations (id SERIAL PRIMARY KEY, \
    #                                 name VARCHAR NOT NULL, \
    #                                 title VARCHAR NOT NULL, \
    #                                 description VARCHAR, \
    #                                 thumbnail VARCHAR, \
    #                                 classes VARCHAR, \
    #                                 dataset VARCHAR, \
    #                                 data_format VARCHAR, \
    #                                 scripts VARCHAR);")

    for visualization in visualization_list:
        conn.execute(f"INSERT INTO {SCHEMA_NAME}.visualizations (\"name\", title, description, thumbnail, classes, dataset, data_format, scripts) VALUES \
                    (\'{visualization['name']}\', \'{visualization['title']}\', \'{visualization['description']}\', \'{visualization['thumbnail']}\', \'{visualization['classes']}\', \'{visualization['dataset']}\', \'{visualization['data_format']}\', \'{visualization['scripts']}\')")
