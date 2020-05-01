DROP MATERIALIZED VIEW IF EXISTS curated.compound CASCADE;

CREATE  MATERIALIZED VIEW curated.compound 
(
  drug_id,
  iupac,
  smiles,
  bioavailability,
  bioavailability_phrase,
  bioavailability_percent,
  molecular_weight,
  molecular_formula,
  clogp,
  psa,
  hba,
  hbd,
  rotatable_bonds,
  aromatic_rings,
  bpka,
  apka,
  compound_name,
  drug_class,
  other_keys,
  type,
  description,
  cas_number,
  unii,
  average_mass,
  monoisotopic_mass,
  state,
  synthesis_reference,
  indication,
  pharmacodynamics,
  mechanism_of_action,
  metabolism,
  absorption,
  half_life,
  protein_binding,
  route_of_elimination,
  volume_of_distribution,
  clearance,
  international_brands,
  pdb_entries,
  fda_label,
  msds,
  food_interactions,
  drug_interactions_count,
  toxicity,
  atc_code,
  atc_level_4,
  therapeutic_code
)
AS 
 WITH iupac AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS iupac
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'IUPAC Name'::text
        ), smiles AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS smiles
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'SMILES'::text
        ), mw AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.kind,
            drug_calculated_properties.value AS mw
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Monoisotopic Weight'::text
        ), mf AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS mf
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Molecular Formula'::text
        ), drug_class AS (
         SELECT uspclass.drugname,
            uspclass.uspclassification AS drug_class
           FROM kegg.uspclass
        ), ba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.kind,
            drug_calculated_properties.value
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Bioavailability'::text
        ), clogp AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS clogp
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'logP'::text AND drug_calculated_properties.source = 'ChemAxon'::text
        ), psa AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS psa
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Polar Surface Area (PSA)'::text
        ), hba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS hba
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'H Bond Acceptor Count'::text
        ), hbd AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS hbd
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'H Bond Donor Count'::text
        ), rb AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS rotatable_bonds
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Rotatable Bond Count'::text
        ), ar AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS aromatic_rings
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Number of Rings'::text
        ), bpka AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS bpka
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'pKa (strongest basic)'::text
        ), apka AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS apka
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'pKa (strongest acidic)'::text
        ), 
        oral_perc_ba as (
    SELECT distinct primary_key, 
       
         COALESCE(
           substring(lower(absorption) from 'oral bioavailability [a-z. (0-9]+ [0-9.]+%'), 
           substring(lower(absorption) FROM 'bioavailability [a-z. (-]+ [0-9.]+%'), 
           substring(lower(absorption) FROM 'bioavailability .+ [0-9.]+%')
       ) AS bioavailability_phrase, 
       substring( 
          substring(
             COALESCE(
               substring(lower(absorption) from 'oral bioavailability [a-z. (0-9]+ [0-9.]+%'), 
               substring(lower(absorption) FROM 'bioavailability [a-z. (-]+ [0-9.]+%'), 
               substring(lower(absorption) FROM 'bioavailability .+ [0-9.]+%')
             ) 
          from '[0-9.]+%' 
          ) 
       from '[0-9.]+'
       ) AS bioavailability_percent, 
       absorption
FROM   drug_bank.drug 
where absorption like '%bioavailab%'
and absorption like '%oral%'    

  ) 
 SELECT DISTINCT drug.primary_key AS drug_id,
    iupac.iupac,
    smiles.smiles,
    ba.value AS bioavailability,
    oral_perc_ba.bioavailability_phrase, 
        oral_perc_ba.bioavailability_percent, 
    mw.mw AS molecular_weight,
    mf.mf AS molecular_formula,
    clogp.clogp,
    psa.psa,
    hba.hba,
    hbd.hbd,
    rb.rotatable_bonds,
    ar.aromatic_rings,
    bpka.bpka,
    apka.apka,
    drug.name AS compound_name,
    drug_class.drug_class,
    drug.other_keys,
    drug.type,
    drug.description,
    drug.cas_number,
    drug.unii,
    drug.average_mass,
    drug.monoisotopic_mass,
    drug.state,
    drug.synthesis_reference,
    drug.indication,
    drug.pharmacodynamics,
    drug.mechanism_of_action,
    drug.metabolism,
    drug.absorption,
    drug.half_life,
    drug.protein_binding,
    drug.route_of_elimination,
    drug.volume_of_distribution,
    drug.clearance,
    drug.international_brands,
    drug.pdb_entries,
    drug.fda_label,
    drug.msds,
    drug.food_interactions,
    drug.drug_interactions_count,
    drug.toxicity,
    drug_atc_codes.atc_code,
    drug_atc_codes.level_4 AS atc_level_4,
    drug_atc_codes.code_4 AS therapeutic_code
   FROM drug_bank.drug drug
     LEFT JOIN drug_bank.drug_atc_codes drug_atc_codes ON drug_atc_codes.parent_key = drug.primary_key
     LEFT JOIN iupac ON drug.primary_key = iupac.drug_id
     LEFT JOIN smiles ON drug.primary_key = smiles.drug_id
     LEFT JOIN mw ON drug.primary_key = mw.drug_id
     LEFT JOIN mf ON drug.primary_key = mf.drug_id
     LEFT JOIN drug_class ON drug_class.drugname ~~ drug.name
     LEFT JOIN ba ON ba.drug_id = drug.primary_key
     LEFT JOIN clogp ON clogp.drug_id = drug.primary_key
     LEFT JOIN psa ON psa.drug_id = drug.primary_key
     LEFT JOIN hba ON hba.drug_id = drug.primary_key
     LEFT JOIN hbd ON hbd.drug_id = drug.primary_key
     LEFT JOIN rb ON rb.drug_id = drug.primary_key
     LEFT JOIN ar ON ar.drug_id = drug.primary_key
     LEFT JOIN bpka ON bpka.drug_id = drug.primary_key
     LEFT JOIN apka ON apka.drug_id = drug.primary_key
     left join oral_perc_ba on oral_perc_ba.primary_key = drug.primary_key ;

COMMIT;
/*
DROP MATERIALIZED VIEW IF EXISTS curated.compound_statistics CASCADE;

CREATE  MATERIALIZED VIEW curated.compound_statistics
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
 SELECT compound.therapeutic_code,
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
  GROUP BY compound.therapeutic_code;

COMMIT;

create view curated.compounds as select * from curated.compound
;

COMMIT;
*/ 
