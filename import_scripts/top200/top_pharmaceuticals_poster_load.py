# Description: this The top 200 records are the result of the analysis performed by Jon Tryggiv from department of
# Chemistry and Biochemistry at University of Arizona. please follow the instructions in read_me.pdf

import numbers
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# please provide YOUR OWN database credential
DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@DB_URL:5432/drugdata"


# this function reads and parse the data frame produced from pdf/excel file
def pdf_table_parser(df):
    drug_name = pd.DataFrame()
    drug_brand_name = pd.DataFrame()
    scripts_number = pd.DataFrame()
    target_d = pd.DataFrame()
    for i in range(0, len(df.index), 4):
        drug_name = pd.concat([drug_name, df.iloc[i]], sort=False)
        drug_brand_name = pd.concat([drug_brand_name, df.iloc[i + 1]], sort=False)
        scripts_number = pd.concat([scripts_number, df.iloc[i + 2]], sort=False)
        target_d = pd.concat([target_d, df.iloc[i + 3]], sort=False)

        drug_name.reset_index(drop=True, inplace=True)
        drug_brand_name.reset_index(drop=True, inplace=True)
        scripts_number.reset_index(drop=True, inplace=True)
        target_d.reset_index(drop=True, inplace=True)

    drug_name.dropna(inplace=True)
    drug_name.reset_index(drop=True, inplace=True)
    drug_brand_name.dropna(inplace=True)
    drug_brand_name.reset_index(drop=True, inplace=True)
    scripts_number.dropna(inplace=True)
    scripts_number.reset_index(drop=True, inplace=True)
    target_d.dropna(inplace=True)
    target_d.reset_index(drop=True, inplace=True)
    drug_name = drug_name[~drug_name.applymap(np.isreal).all(1)]
    drug_name.reset_index(drop=True, inplace=True)
    final_df = pd.concat([drug_name, drug_brand_name, scripts_number, target_d], axis=1)
    final_df.columns = ["drug_name", "drug_brand_name", "scripts_number", "target_d"]

    final_df['drug_brand_name'] = final_df['drug_brand_name'].str.replace("(", "")
    final_df['drug_brand_name'] = final_df['drug_brand_name'].str.replace(")", "")

    return final_df


# the following lines read excel information from excel sheet and converts them into readable dataframes.
t200_sm_mol_pharm_rtl_sls_2018 = pd.read_excel(r'top_pharmaceuticals_poster_data.xlsx',
                                               sheet_name='t200_sm_mol_pharm_rtl_sls_2018', header=None)
t200_pharm_prd_by_pres_2016 = pd.read_excel(r'top_pharmaceuticals_poster_data.xlsx',
                                            sheet_name='t200_pharm_prd_by_pres_2016', header=None)
t_200_pharm_prd_by_rtl_sls_2018 = pd.read_excel(r'top_pharmaceuticals_poster_data.xlsx',
                                                sheet_name='t_200_pharm_prd_by_rtl_sls_2018', header=None)

# Parse and converts excel sheets to data frames
t200_sm_mol_pharm_rtl_sls_2018_df = pdf_table_parser(t200_sm_mol_pharm_rtl_sls_2018)
t200_pharm_prd_by_pres_2016_df = pdf_table_parser(t200_pharm_prd_by_pres_2016)
t_200_pharm_prd_by_rtl_sls_2018_df = pdf_table_parser(t_200_pharm_prd_by_rtl_sls_2018)

# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# Writes the dataframes to PostgreSQL DB
t200_sm_mol_pharm_rtl_sls_2018_df.to_sql('t200_sm_mol_pharm_rtl_sls_2018', con=engine, if_exists='replace',
                                         schema='top200')
t200_pharm_prd_by_pres_2016_df.to_sql('t200_pharm_prd_by_pres_2016', con=engine, if_exists='replace', schema='top200')
t_200_pharm_prd_by_rtl_sls_2018_df.to_sql('t200_pharm_prd_by_rtl_sls_2018', con=engine, if_exists='replace',
                                          schema='top200')

print('top 200 records are successfully inserted')

# Set up database
db.commit()
db.close()
