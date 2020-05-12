WITH table1 as(SELECT DISTINCT compound_structures.molregno as id, mol_dict.pref_name as name, compound_structures.canonical_smiles as smiles
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=0
AND compound_properties.qed_weighted<0.3
AND mol_dict.pref_name IS NOT NULL
AND compound_properties.num_ro5_violations>2),
table2 as(SELECT DISTINCT compound_structures.molregno as id, mol_dict.pref_name as name, compound_structures.canonical_smiles as smiles
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=1
AND compound_properties.qed_weighted<0.3
AND mol_dict.pref_name IS NOT NULL
AND compound_properties.num_ro5_violations>2),
table3 as(SELECT DISTINCT compound_structures.molregno as id, mol_dict.pref_name as name, compound_structures.canonical_smiles as smiles
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=2
AND compound_properties.qed_weighted<0.3
AND mol_dict.pref_name IS NOT NULL
AND compound_properties.num_ro5_violations>2),
table4 as(SELECT DISTINCT compound_structures.molregno as id, mol_dict.pref_name as name, compound_structures.canonical_smiles as smiles
FROM chembl_26.compound_structures as compound_structures
JOIN chembl_26.molecule_dictionary as mol_dict ON mol_dict.molregno=compound_structures.molregno
JOIN chembl_26.compound_properties as compound_properties ON compound_properties.molregno=compound_structures.molregno
WHERE max_phase=3
AND compound_properties.qed_weighted<0.3
AND mol_dict.pref_name IS NOT NULL
AND compound_properties.num_ro5_violations>2),
unified_data as (
SELECT * FROM table1
UNION
SELECT * FROM table2
UNION
SELECT * FROM table3
UNION
SELECT * FROM table4
)
SELECT distinct id, name, smiles FROM unified_data
ORDER BY name
