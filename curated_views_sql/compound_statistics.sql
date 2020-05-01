DROP MATERIALIZED VIEW IF EXISTS curated.compound_statistics CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.compound_statistics
(
  therapeutic_code,
  samples,
  avg_molecular_weight,
  stddev_molecular_weight,
  avg_clogp,
  stddev_clogp,
  avg_hbd,
  stddev_hbd,
  avg_hba,
  stddev_hba,
  avg_psa,
  stddev_psa,
  avg_apka,
  stddev_apka,
  avg_aromatic_rings,
  stddev_aromatic_rings,
  avg_rotatable_bonds,
  stddev_rotatable_bonds
)
AS 
 SELECT "substring"(compound.atc_code, 1, 1) AS therapeutic_code,
    count(DISTINCT compound.drug_id) AS samples,
    avg(compound.molecular_weight::double precision) AS avg_molecular_weight,
    stddev(compound.molecular_weight::double precision) AS stddev_molecular_weight,
    avg(compound.clogp::double precision) AS avg_clogp,
    stddev(compound.clogp::double precision) AS stddev_clogp,
    avg(compound.hbd::double precision) AS avg_hbd,
    stddev(compound.hbd::double precision) AS stddev_hbd,
    avg(compound.hba::double precision) AS avg_hba,
    stddev(compound.hba::double precision) AS stddev_hba,
    avg(compound.psa::double precision) AS avg_psa,
    stddev(compound.psa::double precision) AS stddev_psa,
    avg(compound.apka::double precision) AS avg_apka,
    stddev(compound.apka::double precision) AS stddev_apka,
    avg(compound.aromatic_rings::double precision) AS avg_aromatic_rings,
    stddev(compound.aromatic_rings::double precision) AS stddev_aromatic_rings,
    avg(compound.rotatable_bonds::double precision) AS avg_rotatable_bonds,
    stddev(compound.rotatable_bonds::double precision) AS stddev_rotatable_bonds
   FROM curated.compound
  GROUP BY ("substring"(compound.atc_code, 1, 1));

COMMIT;
