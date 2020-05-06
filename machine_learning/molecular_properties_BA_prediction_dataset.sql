with data as (
select 
distinct  
bioavailability, 
(route = 'Oral')::int as is_oral_route, 
compound_name, 
smiles,
molecular_weight, 
clogp, 
aromatic_rings, 
hba, 
hbd,
rotatable_bonds, 
psa, 
bpka, 
apka
from compound
LEFT JOIN product using (drug_id) 
where bioavailability is not null 
order by 1 
), 
classes as (
select 
-- this section is up to us to decide. it depends on how want to define classes
case 
when bioavailability='1' and is_oral_route=1 then 1 
when bioavailability='1' and is_oral_route=0 then null  
when bioavailability='1' and is_oral_route is null then null  
when bioavailability='0' then 0 
else null 
end as class, 
*
from data)

select * from classes
-- this section is also up to us, depending on whether or not we permit nulls as param inputs. I would think not because by the time you want to evaluate a drug compound, these params should be known. 
where molecular_weight is not null 
and clogp is not null 
and aromatic_rings is not null 
and hba is not null 
and hbd is not null 
and rotatable_bonds is not null 
and psa is not null 
and bpka is not null 
and apka is not null 

