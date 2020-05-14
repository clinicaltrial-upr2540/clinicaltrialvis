-- Drop materialized view
drop materialized view if exists curated.compound_statistics;

-- Generate the materialized view
create materialized view curated.compound_statistics as
SELECT compound.therapeutic_code,
       compound.atc_level_4,
       count(DISTINCT compound.drug_id)                    AS samples,
       avg(compound.molecular_weight::double precision)    AS avg_molecular_weight,
       stddev(compound.molecular_weight::double precision) AS stddev_molecular_weight,
       avg(compound.clogp::double precision)               AS avg_clogp,
       stddev(compound.clogp::double precision)            AS stddev_clogp,
       avg(compound.hbd::double precision)                 AS avg_hbd,
       stddev(compound.hbd::double precision)              AS stddev_hbd,
       avg(compound.hba::double precision)                 AS avg_hba,
       stddev(compound.hba::double precision)              AS stddev_hba,
       avg(compound.psa::double precision)                 AS avg_psa,
       stddev(compound.psa::double precision)              AS stddev_psa,
       avg(compound.apka::double precision)                AS avg_apka,
       stddev(compound.apka::double precision)             AS stddev_apka,
       avg(compound.aromatic_rings::double precision)      AS avg_aromatic_rings,
       stddev(compound.aromatic_rings::double precision)   AS stddev_aromatic_rings,
       avg(compound.rotatable_bonds::double precision)     AS avg_rotatable_bonds,
       stddev(compound.rotatable_bonds::double precision)  AS stddev_rotatable_bonds
FROM curated.compound
GROUP BY compound.therapeutic_code, compound.atc_level_4;

alter materialized view curated.compound_statistics owner to postgres;

