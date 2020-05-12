WITH table1 as(SELECT DISTINCT compound_structures.molregno as id,
                mol_dict.pref_name as name,
                compound_structures.canonical_smiles as smiles,
                compound_properties.full_mwt as mw,
                compound_properties.cx_logp as clogp,
                compound_properties.aromatic_rings as arom,
                compound_properties.hba as hba,
                compound_properties.hbd as hbd,
                compound_properties.rtb as rotb,
                compound_properties.psa as psa,
                compound_properties.cx_most_bpka as bpka,
                compound_properties.cx_most_apka as apka
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
JOIN chembl_26.compound_records as compound_records ON compound_records.molregno=compound_structures.molregno
JOIN chembl_26.formulations as formulations ON formulations.molregno=compound_structures.molregno
JOIN chembl_26.products as products ON formulations.product_id=products.product_id
WHERE max_phase=4
AND mol_dict.oral=1
AND mol_dict.withdrawn_flag=0
AND products.ad_type!='DISCN'
AND mol_dict.pref_name IS NOT NULL
AND canonical_smiles IS NOT NULL),
table2 as(SELECT DISTINCT compound_structures.molregno as id,
                mol_dict.pref_name as name,
                compound_structures.canonical_smiles as smiles,
                compound_properties.full_mwt as mw,
                compound_properties.cx_logp as clogp,
                compound_properties.aromatic_rings as arom,
                compound_properties.hba as hba,
                compound_properties.hbd as hbd,
                compound_properties.rtb as rotb,
                compound_properties.psa as psa,
                compound_properties.cx_most_bpka as bpka,
                compound_properties.cx_most_apka as apka
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=1
AND mol_dict.pref_name IS NOT NULL
AND canonical_smiles IS NOT NULL),
table3 as(SELECT DISTINCT compound_structures.molregno as id,
                mol_dict.pref_name as name,
                compound_structures.canonical_smiles as smiles,
                compound_properties.full_mwt as mw,
                compound_properties.cx_logp as clogp,
                compound_properties.aromatic_rings as arom,
                compound_properties.hba as hba,
                compound_properties.hbd as hbd,
                compound_properties.rtb as rotb,
                compound_properties.psa as psa,
                compound_properties.cx_most_bpka as bpka,
                compound_properties.cx_most_apka as apka
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=2
AND mol_dict.pref_name IS NOT NULL
AND canonical_smiles IS NOT NULL),
table4 as(SELECT DISTINCT compound_structures.molregno as id,
                mol_dict.pref_name as name,
                compound_structures.canonical_smiles as smiles,
                compound_properties.full_mwt as mw,
                compound_properties.cx_logp as clogp,
                compound_properties.aromatic_rings as arom,
                compound_properties.hba as hba,
                compound_properties.hbd as hbd,
                compound_properties.rtb as rotb,
                compound_properties.psa as psa,
                compound_properties.cx_most_bpka as bpka,
                compound_properties.cx_most_apka as apka
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=3
AND mol_dict.pref_name IS NOT NULL
AND canonical_smiles IS NOT NULL),
unified_data as (
SELECT * FROM table1
UNION
SELECT * FROM table2
UNION
SELECT * FROM table3
UNION
SELECT * FROM table4
)
SELECT distinct id, name, smiles, mw, clogp, arom, hba, hbd, rotb, psa FROM unified_data
ORDER BY name
