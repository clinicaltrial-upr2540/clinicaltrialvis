SELECT DISTINCT
compound_name,
smiles
FROM curated.compounds
WHERE smiles is not null