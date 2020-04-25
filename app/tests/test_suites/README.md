
# How to Run Test Cases

1. Navigate to app.py
2. Comment out DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
3. Specify DATABASE_URL with YOUR OWN CREDENTIAL 
DATABASE_URL = postgresql://<username>:<password>@<hostname>:<port>/<database>
4. run app.py
5. Right click on test_suites and run the entire test suites
