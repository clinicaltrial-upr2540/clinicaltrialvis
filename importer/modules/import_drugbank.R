#!/usr/bin/env Rscript

#The provided R script leverages the out of the box DrugBank Database XML Parser R Library to parse the entire extracted DrugBank.xml and restore and persists the entire drugbank database into the targeted central PostgreSQL. For detailed information about the library, please refer to following article.  
#https://cran.r-project.org/web/packages/dbparser/vignettes/dbparser.html

# Includes modifications by Gabe Sanna to integrate with Python
# Usage:
#  ./import_drugbank.R <host> <port> <dbname> <username> <password> <filepath>

args = commandArgs(trailingOnly=TRUE)

if (length(args)<6) {
    stop("SYNTAX ERROR: Not enough arguments provided.", call.=FALSE)
}

#the following section installs and loads all required libraries including the out of the box dbparser
if (!require('XML')) install.packages('XML',repos = "http://cran.us.r-project.org"); library('XML')
if (!require('RPostgreSQL')) install.packages('RPostgreSQL',repos = "http://cran.us.r-project.org"); library('RPostgreSQL')
if (!require('DBI')) install.packages('DBI',repos = "http://cran.us.r-project.org"); library('DBI')
if (!require('rlang')) install.packages('rlang',repos = "http://cran.us.r-project.org"); library('rlang')
if (!require('odbc')) install.packages('odbc',repos = "http://cran.us.r-project.org"); library('odbc')
if (!require('dbparser')) install.packages('dbparser',dependencies=TRUE,repos = "http://cran.us.r-project.org"); library('dbparser')

print('script started')

# Read the entire xml database and store it into memory
print('loading data file')
read_drugbank_xml_db(args[6])

# the following section, connects to target database and persists the entire database
print('connecting to database')
pg = dbDriver("PostgreSQL")

# Please provide your database credential 
con = dbConnect(pg, user=args[4], password=args[5], host=args[1], port=args[2], dbname=args[3])

print('starting import')
drug_all(save_table = TRUE, database_connection = con)
DBI::dbListTables(con)
DBI::dbDisconnect(con)

print('script ended')
