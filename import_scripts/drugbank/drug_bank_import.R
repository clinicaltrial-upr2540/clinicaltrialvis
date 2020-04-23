#The provided R script leverages the out of the box DrugBank Database XML Parser R Library to parse the entire extracted DrugBank.xml and restore and persists the entire drugbank database into the targeted central PostgreSQL. For detailed information about the library, please refer to following article.  
#https://cran.r-project.org/web/packages/dbparser/vignettes/dbparser.html


#the following section installs all required libraries including the out of the box dbparser
install.packages('XML')
install.packages('RPostgreSQL')
install.packages("rlang")
install.packages("dbparser",dependencies=TRUE)

#the following section loads all required libraries
library(dbparser)
library(XML)
library(odbc)
library(dbparser)
library('RPostgreSQL')

print('script started')

#the following line read the entire xml database and store it into memory
read_drugbank_xml_db("C:/Development/School/CSCI-E 599/data/drugbank_all_full_database.xml/full database.xml")


# the following section, connects to target database and persists the entire database
pg = dbDriver("PostgreSQL")

# Please provide your database credential 
con = dbConnect(pg, user="YOUR_USER", password="YOUR_PASS!",host="DB_URL", port=5432, dbname="drugbank")


drug_all(save_table = TRUE, database_connection = con,  override = TRUE)
DBI::dbListTables(con)
DBI::dbDisconnect(con)

print('script ended')


