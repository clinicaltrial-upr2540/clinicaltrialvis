# Description: this script import and persists the data from FDA

import glob
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# get data file names
path = r'C:\Development\School\CSCI-E 599\data\drugsatfda20200225'
filenames = glob.glob(path + "/*.txt")
DATABASE_URL = "postgresql://YOUR_USER:YOUR_PASS@localhost:5432/postgres"

SCHEMA_NAME = "fda"

# # Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

with engine.connect() as conn:
    # Create the table if necessary
    conn.execute(f"CREATE SCHEMA  IF NOT EXISTS {SCHEMA_NAME};")
    conn.execute(f"set search_path to {SCHEMA_NAME};")
    conn.close()

dfs = []
for filename in filenames:
    if "Products.txt" in filename or "Products.txt" in filename:
        if "ActionTypes_Lookup.txt" in filename:
            data = pd.read_csv(filename, header=0, error_bad_lines=False, sep='\t')
            data["ActionTypes_LookupID"] = data.ActionTypes_LookupID.astype(int)
            data.to_sql('actiontypeslookup', con=engine, if_exists='replace', schema='fda')
            db.commit()
            print('actiontypeslookup inserted')
        if "Products.txt" in filename:
            data = pd.read_csv(filename, header=0, error_bad_lines=False, sep='\t')
            data["ApplNo"] = data.ApplNo.astype(int)
            data["ProductNo"] = pd.to_numeric(data["ProductNo"], downcast='integer')
            data.to_sql('products', con=engine, if_exists='replace', schema='fda')
            db.commit()
            print('Products inserted')
    else:
        d = []
        with open(filename, 'r') as source:
            for line in source:
                fields = line.split('\t')
                cleansed = [s.strip(';') for s in fields]
                d.append(cleansed)
            df = pd.DataFrame(d, columns=d[0])
            df = df.iloc[1:]

            df = df.replace('\n', '', regex=True)
            df = df.replace(r'\\n', '', regex=True)
            df = df.dropna()
            if "ApplicationDocs.txt" in filename:
                df.to_sql('applicationdocs', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('applicationdocs inserted')
            if "Applications.txt" in filename:
                df.to_sql('applications', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('applications inserted')
            if "ApplicationsDocsType_Lookup.txt" in filename:
                df.to_sql('applicationsdocstypelookup', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('applicationsdocstypelookup inserted')
            if "MarketingStatus.txt" in filename:
                df.to_sql('marketingstatus', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('marketingstatus inserted')
            if "MarketingStatus_Lookup.txt" in filename:
                df.to_sql('marketingstatuslookup', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('marketingstatuslookup inserted')
            if "SubmissionClass_Lookup.txt" in filename:
                df.to_sql('submissionclasslookup', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('submissionclasslookup inserted')
            if "Submissions.txt" in filename:
                df.to_sql('submissions', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('submissions inserted')
            if "SubmissionPropertyType.txt" in filename:
                df.to_sql('submissionpropertytype', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('submissionpropertytype inserted')
            if "TE.txt" in filename:
                df.to_sql('te', con=engine, if_exists='replace', schema='fda')
                db.commit()
                print('te inserted')
