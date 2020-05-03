
There is a portfolio of six interactive visualizations. Each of the visualizations show one of the following relationship: 
company, disease class and a number of approved drug within a disease class (dotmatrix, radar) or
company, disease class and a top parameter of drugs within a disease class (box-whisker, heatmap, 3d_bubbles and splom).
Each of the visualizations consist of a javascript file (-s), a custom css file and a data file.
A data file has been pre-processed because it is necessary to generate a disease class and group the data prior to visualizing it. Besides, the data itself does not need to be queried from the DB directly in real-time, since the data collection is predefined by the customer and has no need to be updated.
The structure of the directories for the visualizations that are deployed via Flask is as follows.
.js files -   app/static/js-visualizations/[name_of_visualization]/
.css files -   app/static/css/visualizations/[one css file per visualization named similarly to the name_of_visualization]
data and import scripts – import_scripts/visualization-loader/[name_of_visualization]


In order to run visualizations locally, there is a need for a web server (MAMP or any other), all three files per visualization: .js .css, data file (or more than three files, if there is more than one .js file) and index.html files have to be placed in the same directory. Please reach out to the team to receive index.html files for each of the visualizations.
