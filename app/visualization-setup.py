#!/usr/bin/env python3

import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker

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
        "scripts": "bubble-plot-3d.js"
    },
    {
        "name": "box-whisker",
        "title": "Drug Targets by Companies",
        "description": "Box and Whisker Chart",
        "thumbnail": "box-whisker.png",
        "classes": "box-whisker-plotly",
        "dataset": "heatmapdata",
        "data_format": "csv",
        "scripts": "box-whisker.js"
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

DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
# DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@localhost:54320/postgres"
SCHEMA_NAME = "application"

# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# # Does the schema exist? If not, create
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
db.commit()

# Create the table if necessary
db.execute(f"set search_path to {SCHEMA_NAME};")
db.execute("DROP TABLE IF EXISTS visualizations;")
db.execute("CREATE TABLE visualizations (id SERIAL PRIMARY KEY, \
                                name VARCHAR NOT NULL, \
                                title VARCHAR NOT NULL, \
                                description VARCHAR, \
                                thumbnail VARCHAR, \
                                classes VARCHAR, \
                                dataset VARCHAR, \
                                data_format VARCHAR, \
                                scripts VARCHAR);")
db.commit()

for visualization in visualization_list:
    db.execute(f"INSERT INTO {SCHEMA_NAME}.visualizations (\"name\", title, description, thumbnail, classes, dataset, data_format, scripts) VALUES \
                (\'{visualization['name']}\', \'{visualization['title']}\', \'{visualization['description']}\', \'{visualization['thumbnail']}\', \'{visualization['classes']}\', \'{visualization['dataset']}\', \'{visualization['data_format']}\', \'{visualization['scripts']}\')")
    db.commit()

db.close()
