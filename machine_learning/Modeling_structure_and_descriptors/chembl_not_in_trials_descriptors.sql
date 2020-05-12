SELECT DISTINCT compound_structures.molregno as id,
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
WHERE max_phase=0
AND mol_dict.pref_name IS NOT NULL
AND canonical_smiles IS NOT NULL
AND full_mwt IS NOT NULL
AND cx_logp IS NOT NULL
AND aromatic_rings IS NOT NULL
AND hba IS NOT NULL
AND hbd IS NOT NULL
AND rtb IS NOT NULL
AND psa IS NOT NULL
AND cx_most_apka IS NOT NULL
AND cx_most_bpka IS NOT NULL