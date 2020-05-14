# ChemDataExplorer Import Tool

This tool is provided to build a Postgres database instance used as a backend for the ChemDataExplorer application. It automates the process of downloading and importing data from several datasets, including CheMBL, DrugBank, and PubChem.

## Running the tool

If you are building the database with a Linux or Windows computer, follow the instructions [provided here](https://hub.docker.com/repository/docker/chemdataexplorer/chemdataimporter) to run the setup using a prepackaged Docker container.

If you are using MacOS, unfortunately there is a bug with Docker Desktop that will break the setup process. Instead, you will need to use the following instructions to download and run the scripts yourself.

### Installing requirements

1. If you haven't already, install the XCode Command Line Tools with the following Terminal command:

`sudo xcode-select --install`

2. Install Homebrew, a package manager to download additional build tools on MacOS:

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`

3. Install required tools and languages with Homebrew:

`brew install r python3 unixodbc mariadb-connector-c psqlodbc`

4. Clone this repository and change directory:

`git clone https://github.com/clinicaltrial-upr2540/clinicaltrialvis.git`
`cd clinicaltrialvis/importer`

5. Install Python and R dependencies (this will take a while):

`python3 -m pip install -r requirements.txt`
`Rscript modules/install_dependencies.R`

### Set up a Postgres database

ChemDataExplorer requires a PostgresSQL database instance in which to store the data. You can install a local instance using Homebrew or a Docker container, but we recommend setting up an instance in the cloud using [Amazon Web Services](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html) or [Heroku](https://devcenter.heroku.com/articles/heroku-postgresql), or working with your organization's IT department.

Once you have a database instance set up and administrator credentials created, rename `database.conf.sample` to `database.conf` and fill in the imformation to connect to the database.

### Running the import

After you've installed all the requirements, you can run the import with the following command:

`python3 database_setup.py`

This is a long process—**four to eight hours**. In the event that it fails, it is safe to re-run the script—it will only attempt to import data sources that have no already completed successfully. After it is complete, the script will print a command to start to start the [ChemDataExplorer application](https://hub.docker.com/repository/docker/chemdataexplorer/chemdataexplorer).
