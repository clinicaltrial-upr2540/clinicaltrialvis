# Clinical Trial and Pharmaceutical Chemical Space Visualization
This is the main repository for the Clinical Trial and Pharmaceutical Chemical Space Visualization team. There are three key deliverables to our project:

- An **aggregated database** of various sets of drug and pharmacological data. The code in this repository includes A. a set of import scripts with instructions for users to gather the various datasets into a single PostgresSQL instance and B. a set of SQL scripts to condense the dispirate datasets into a set of easily-navigated views.
- A **Python web application** that presents a user-friendly interface for navigating and exporting data from the database. This database will also expose several API endpoints so users can access the data programmatically. Finally, this application includes several sample visualizations to demonstrate applications of the curated dataset.
- A **machine learning** model that will hope to predict drug candidates that will be bioavailable or perform well in clinical trials.

There are two steps required to getting the application running: **building the database** and **running the application**.

## Building the database
There are two ways to build a ChemDataExplorer database instance. On Windows or Linux, you can pull a Docker container that includes all the dependencies and will run the scripts for you. On macOS, you will need to install a number of dependencies and run the scripts yourself.

### To set up the database on Linux or Windows

See detailed instructions [here](https://hub.docker.com/repository/docker/chemdataexplorer/chemdataimporter).

### To set up the database on MacOS

See detailed instructions [here](https://github.com/clinicaltrial-upr2540/clinicaltrialvis/tree/master/importer).

## Running the Application

After the database build is complete, it will print the command to start the application. For more detailed instructions, see the [ChemDataExplorer page on Docker Hub](https://hub.docker.com/repository/docker/chemdataexplorer/chemdataexplorer).
