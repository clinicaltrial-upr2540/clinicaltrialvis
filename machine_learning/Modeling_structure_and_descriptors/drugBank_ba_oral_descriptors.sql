with ba as (
select
parent_key,
value as ba
from drug_bank.drug_calculated_properties
where kind = 'Bioavailability'
),

mw as (
select
parent_key,
value as molecular_weight
from drug_bank.drug_calculated_properties
where kind = 'Molecular Weight'
),
clogp as (
select
parent_key,
value as clogp
from drug_bank.drug_calculated_properties
where kind = 'logP'
AND source='ChemAxon'
),
psa as (
select
parent_key,
value as psa
from drug_bank.drug_calculated_properties
where kind = 'Polar Surface Area (PSA)'
),
hba as (
select
parent_key,
value as hba
from drug_bank.drug_calculated_properties
where kind = 'H Bond Acceptor Count'
),
hbd as (
select
parent_key,
value as hbd
from drug_bank.drug_calculated_properties
where kind = 'H Bond Donor Count'
),
rb as (
select
parent_key,
value as rotatable_bonds
from drug_bank.drug_calculated_properties
where kind = 'Rotatable Bond Count'
),
ar as (
select
parent_key,
value as aromatic_rings
from drug_bank.drug_calculated_properties
where kind = 'Number of Rings'
),
bpka as (
select
parent_key,
value as pka_basic
from drug_bank.drug_calculated_properties
where kind = 'pKa (strongest basic)'
),
apka as (
select
parent_key,
value as pka_asicid
from drug_bank.drug_calculated_properties
where kind = 'pKa (strongest acidic)'
)
SELECT DISTINCT
drug_products.parent_key,
ba.ba,
mw.molecular_weight,
clogp.clogp,
psa.psa,
hba.hba,
hbd.hbd,
rb.rotatable_bonds,
ar.aromatic_rings,
bpka.pka_basic,
apka.pka_asicid
FROM drug_bank.drug_products AS drug_products
INNER JOIN mw ON mw.parent_key=drug_products.parent_key
INNER JOIN ba ON ba.parent_key=drug_products.parent_key
INNER JOIN clogp ON clogp.parent_key=drug_products.parent_key
INNER JOIN psa ON psa.parent_key=drug_products.parent_key
INNER JOIN hba ON hba.parent_key=drug_products.parent_key
INNER JOIN hbd ON hbd.parent_key=drug_products.parent_key
INNER JOIN rb ON rb.parent_key=drug_products.parent_key
INNER JOIN ar ON ar.parent_key=drug_products.parent_key
INNER JOIN bpka ON bpka.parent_key=drug_products.parent_key
INNER JOIN apka ON apka.parent_key=drug_products.parent_key
WHERE drug_products.route LIKE '%Oral%'
AND ba.ba = '1'