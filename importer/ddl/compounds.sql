
-- =============================================
-- Materialized View Name: compound
-- Nonmaterialized View Name: compounds
-- Description: this material view is designed to show the descriptors of chemical compounds in drugs
-- PROGRAMMING NOTES
--      This materialized view can be modified by adding the additional a characteristic as long the primary key is unchanged
--      Any new fields must be added to both the materialized view and the corresponding nonmaterialized view below
-- =============================================

-- Drop materialized view
drop materialized view if exists curated.compound;

-- Generate the materialized view
create materialized view curated.compound as
WITH iupac AS (
    SELECT drug_calculated_properties.parent_key AS drug_id,
           drug_calculated_properties.value      AS iupac
    FROM drug_bank.drug_calculated_properties drug_calculated_properties
    WHERE drug_calculated_properties.kind ~~ 'IUPAC Name'::text
),
     smiles AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS smiles
         FROM drug_bank.drug_calculated_properties drug_calculated_properties
         WHERE drug_calculated_properties.kind ~~ 'SMILES'::text
     ),
     mw AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.kind,
                drug_calculated_properties.value      AS mw
         FROM drug_bank.drug_calculated_properties drug_calculated_properties
         WHERE drug_calculated_properties.kind ~~ 'Monoisotopic Weight'::text
     ),
     mf AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS mf
         FROM drug_bank.drug_calculated_properties drug_calculated_properties
         WHERE drug_calculated_properties.kind ~~ 'Molecular Formula'::text
     ),
     drug_class AS (
         SELECT uspclass.drugname,
                uspclass.uspclassification AS drug_class
         FROM kegg.uspclass
     ),
     ba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.kind,
                drug_calculated_properties.value
         FROM drug_bank.drug_calculated_properties drug_calculated_properties
         WHERE drug_calculated_properties.kind ~~ 'Bioavailability'::text
     ),
     clogp AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS clogp
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'logP'::text
           AND drug_calculated_properties.source = 'ChemAxon'::text
     ),
     psa AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS psa
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'Polar Surface Area (PSA)'::text
     ),
     hba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS hba
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'H Bond Acceptor Count'::text
     ),
     hbd AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS hbd
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'H Bond Donor Count'::text
     ),
     rb AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS rotatable_bonds
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'Rotatable Bond Count'::text
     ),
     ar AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS aromatic_rings
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'Number of Rings'::text
     ),
     bpka AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS bpka
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'pKa (strongest basic)'::text
     ),
     apka AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
                drug_calculated_properties.value      AS apka
         FROM drug_bank.drug_calculated_properties
         WHERE drug_calculated_properties.kind = 'pKa (strongest acidic)'::text
     ),
     oral_perc_ba AS (
         SELECT DISTINCT drug_1.primary_key,
                         COALESCE("substring"(lower(drug_1.absorption),
                                              'oral bioavailability [a-z. (0-9]+ [0-9.]+%'::text),
                                  "substring"(lower(drug_1.absorption), 'bioavailability [a-z. (-]+ [0-9.]+%'::text),
                                  "substring"(lower(drug_1.absorption),
                                              'bioavailability .+ [0-9.]+%'::text))  AS bioavailability_phrase,
                         "substring"("substring"(COALESCE("substring"(lower(drug_1.absorption),
                                                                      'oral bioavailability [a-z. (0-9]+ [0-9.]+%'::text),
                                                          "substring"(lower(drug_1.absorption),
                                                                      'bioavailability [a-z. (-]+ [0-9.]+%'::text),
                                                          "substring"(lower(drug_1.absorption),
                                                                      'bioavailability .+ [0-9.]+%'::text)),
                                                 '[0-9.]+%'::text), '[0-9.]+'::text) AS bioavailability_percent,
                         drug_1.absorption
         FROM drug_bank.drug drug_1
         WHERE drug_1.absorption ~~ '%bioavailab%'::text
           AND drug_1.absorption ~~ '%oral%'::text
     )
SELECT DISTINCT drug.primary_key       AS drug_id,
                iupac.iupac,
                smiles.smiles,
                ba.value               AS bioavailability,
                oral_perc_ba.bioavailability_phrase,
                oral_perc_ba.bioavailability_percent,
                mw.mw                  AS molecular_weight,
                mf.mf                  AS molecular_formula,
                clogp.clogp,
                psa.psa,
                hba.hba,
                hbd.hbd,
                rb.rotatable_bonds,
                ar.aromatic_rings,
                bpka.bpka,
                apka.apka,
                drug.name              AS compound_name,
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
                drug_atc_codes.code_4  AS therapeutic_code
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
         LEFT JOIN oral_perc_ba ON oral_perc_ba.primary_key = drug.primary_key;

alter materialized view curated.compound owner to postgres;

-- Drop the existing non-matieralized view
drop view if exists curated.compounds;

-- Generate the non-matieralized view
create view curated.compounds(drug_id, iupac, smiles, bioavailability, bioavailability_phrase, bioavailability_percent, molecular_weight, molecular_formula, clogp, psa, hba, hbd, rotatable_bonds, aromatic_rings, bpka, apka, compound_name, drug_class, other_keys, type, description, cas_number, unii, average_mass, monoisotopic_mass, state, synthesis_reference, indication, pharmacodynamics, mechanism_of_action, metabolism, absorption, half_life, protein_binding, route_of_elimination, volume_of_distribution, clearance, international_brands, pdb_entries, fda_label, msds, food_interactions, drug_interactions_count, toxicity, atc_code, atc_level_4, therapeutic_code) as
SELECT compound.drug_id,
       compound.iupac,
       compound.smiles,
       compound.bioavailability,
       compound.bioavailability_phrase,
       compound.bioavailability_percent,
       compound.molecular_weight,
       compound.molecular_formula,
       compound.clogp,
       compound.psa,
       compound.hba,
       compound.hbd,
       compound.rotatable_bonds,
       compound.aromatic_rings,
       compound.bpka,
       compound.apka,
       compound.compound_name,
       compound.drug_class,
       compound.other_keys,
       compound.type,
       compound.description,
       compound.cas_number,
       compound.unii,
       compound.average_mass,
       compound.monoisotopic_mass,
       compound.state,
       compound.synthesis_reference,
       compound.indication,
       compound.pharmacodynamics,
       compound.mechanism_of_action,
       compound.metabolism,
       compound.absorption,
       compound.half_life,
       compound.protein_binding,
       compound.route_of_elimination,
       compound.volume_of_distribution,
       compound.clearance,
       compound.international_brands,
       compound.pdb_entries,
       compound.fda_label,
       compound.msds,
       compound.food_interactions,
       compound.drug_interactions_count,
       compound.toxicity,
       compound.atc_code,
       compound.atc_level_4,
       compound.therapeutic_code
FROM curated.compound;

alter table curated.compounds owner to postgres;
