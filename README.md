# Clinical Trial and Pharmaceutical Chemical Space Visualization
This is the main repository for the Clinical Trial and Pharmaceutical Chemical Space Visualization team. There are three key deliverables to our project:

- An **aggregated database** of various sets of drug and pharmacological data. The code in this repository includes A. a set of import scripts with instructions for users to gather the various datasets into a single PostgresSQL instance and B. a set of SQL scripts to condense the dispirate datasets into a set of easily-navigated views.
- A **Python web application** that presents a user-friendly interface for navigating and exporting data from the database. This database will also expose several API endpoints so users can access the data programmatically. Finally, this application includes several sample visualizations to demonstrate applications of the curated dataset.
- A **machine learning** model that will hope to predict drug candidates that will be bioavailable or perform well in clinical trials.

## Prerequisites
Before running this application locally, you will need to install the following:

- **Python3** - This application requires python3.6 or later. The easiest way to install this on a Mac is via Homebrew.
- Run the following command to install Python packages: `python3 -m pip install -r requirements.txt`
- To run import scripts, you will also need a postgres client and R installed.

## Directories
This repository is structured with the following directories:

- **ansible** - This contains Ansible code for configuring our shared development environment. It is not relevant to users who wish to run the application locally.
- **app** - This directory contains the Python web application with the user interface for exploring data and viewing visualizations. For information on how to configure and run the application, see the README.md file in the `app` directory.
- **import_scripts** - Contains the scripts needed to import datasets and build a new database. NOTE: These will be combined to a more automated process. We do not currently recommend end users attempt to import data.
