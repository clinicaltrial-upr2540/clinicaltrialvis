SELECT DISTINCT
compounds.drug_id,
compound_name,
smiles,
bioavailability,
molecular_weight,
clogp,
psa,
hba,
hbd,
rotatable_bonds,
aromatic_rings,
apka,
bpka
FROM curated.compounds As compounds
JOIN curated.product as product ON product.drug_id = compounds.drug_id
WHERE smiles is not null
AND molecular_weight is not null
AND clogp is not null
AND psa is not null
AND hba is not null
AND hbd is not null
AND rotatable_bonds is not null
AND aromatic_rings is not null
AND apka is not null
AND bpka is not null
AND bioavailability ='1'
AND product.route like '%Oral'
