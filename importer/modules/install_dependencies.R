#!/usr/bin/env Rscript

if (!require('XML')) install.packages('XML',repos = "http://cran.us.r-project.org"); library('XML')
if (!require('RPostgreSQL')) install.packages('RPostgreSQL',repos = "http://cran.us.r-project.org"); library('RPostgreSQL')
if (!require('rlang')) install.packages('rlang',repos = "http://cran.us.r-project.org"); library('rlang')
if (!require('odbc')) install.packages('odbc',repos = "http://cran.us.r-project.org"); library('odbc')
if (!require('RMariaDB')) install.packages('RMariaDB',repos = "http://cran.us.r-project.org"); library('RMariaDB')
if (!require('dbparser')) install.packages('dbparser',dependencies=TRUE,repos = "http://cran.us.r-project.org"); library(dbparser)
