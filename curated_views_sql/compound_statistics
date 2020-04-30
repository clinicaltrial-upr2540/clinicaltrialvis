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
 SELECT "substring"(compounds.atc_code, 1, 1) AS therapeutic_code,
    count(DISTINCT compounds.drug_id) AS samples,
    avg(compounds.molecular_weight::double precision) AS avg_molecular_weight,
    stddev(compounds.molecular_weight::double precision) AS stddev_molecular_weight,
    avg(compounds.clogp::double precision) AS avg_clogp,
    stddev(compounds.clogp::double precision) AS stddev_clogp,
    avg(compounds.hbd::double precision) AS avg_hbd,
    stddev(compounds.hbd::double precision) AS stddev_hbd,
    avg(compounds.hba::double precision) AS avg_hba,
    stddev(compounds.hba::double precision) AS stddev_hba,
    avg(compounds.psa::double precision) AS avg_psa,
    stddev(compounds.psa::double precision) AS stddev_psa,
    avg(compounds.apka::double precision) AS avg_apka,
    stddev(compounds.apka::double precision) AS stddev_apka,
    avg(compounds.aromatic_rings::double precision) AS avg_aromatic_rings,
    stddev(compounds.aromatic_rings::double precision) AS stddev_aromatic_rings,
    avg(compounds.rotatable_bonds::double precision) AS avg_rotatable_bonds,
    stddev(compounds.rotatable_bonds::double precision) AS stddev_rotatable_bonds
   FROM curated.compounds
  GROUP BY ("substring"(compounds.atc_code, 1, 1));

COMMIT;
