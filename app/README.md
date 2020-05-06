
# Flask Application

This application presents a user-friendly interface for interacting with our curated dataset of multiple pharmacological databases. This README outlines the functional parts of the code base and where they can be found.

## Configuration

Before the application will run, the **database.conf** file needs credentials and host information for the Postgres backend. If you did not set up your database instance, credentials will be provided to a shared instance by the team. The following fields must be completed:

```
host = 
user = 
password = 
```

## Python Files

Back-end functionality is provided by the following `.py` files.

* **app.py** - This is the main application, and it contains all the routes for the website, as well as supporting logic for querying the database and formatting replies to the frontend.
* **test_responses.py** - In the course of building the frontend or any other application that interacts with the API, it can be useful to have test data. This file contains variables with sample API responses to support development.
* **visualization_setup.py** - Imports information about the various visualizations included with the application into the database. This allows visualization pages to be generated dynamically.

## HTML Templates

There are six HTML templates included in the project, found in the `templates/` directory. These will all be rendered by the routes in `app.py`.

* **api.html** - Provides documentation for the API endpoints for any developers who might want to explore data programmatically.
* **explore.html** - This template is the main interface for users to browse and export data from the curated database. Note that most of the functionality on this page comes from `../static/js/explore.js`.
* **home.html** - The homepage. Users are directed here by the `/` route. This will include an introduction to the project.
* **master.html** - This is the master layout template, extended by all the other templates. It includes the navbar and links to external resources including Bootstrap 4.
* **visualization.html** - This template is used to display a single visualization.
* **visualizations.html** - This page presents a grid of all the visualizations the user can browse.

## Static Resources

There are several resources in the `static` directory, including CSS styles and Javascript.

* **css/** contains all CSS, including both frameworks and custom styles.
* **img/** contains any images used through the site, including preview thumbnails of visualizations.
* **js/** contains general-purpose javascript files.
* **js-visualizations/** contains D3 Javascript files used to generate visualizations.

### CSS

Within the `css` directory, most of the files are from Bootstrap or other frameworks. However, some files are worth noting:

* **visualizations/** - This directory contains hand-writtenstyles for the visualizations.
* **styles.css** - This file containers any hand-written styles used to override the normal Bootstrap or Argon framework behavior.

### JavaScript

Within the `js` directory, most of the scripts are from various frameworks. You should pay attention to the following files:

* **explore.js** - This file contains all the code used by the `/explore` page to interact with the API backend and present a user-friendly interface for browsing and exporting the curated dataset.
