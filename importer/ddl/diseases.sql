
-- =============================================
-- Materialized View Name: disease
-- Nonmaterialized View Name: diseases
-- Description: this material view is designed to show the disease classification from mesh term database in association which compounds
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding additional characteristics as long as the SMILES will stay as primary key
-- =============================================

-- Drop materialized view
drop materialized view if exists curated.disease;

-- Generate the materialized view
create materialized view curated.disease as
WITH smiles AS (
    SELECT drug_calculated_properties.parent_key AS drug_id,
           drug_calculated_properties.value      AS smiles
    FROM drug_bank.drug_calculated_properties drug_calculated_properties
    WHERE drug_calculated_properties.kind ~~ 'SMILES'::text
)
SELECT DISTINCT smiles.drug_id,
                drug_indication.mesh_id,
                compound_records.compound_name,
                compound_records.molregno,
                compound_structures.canonical_smiles,
                mesh_term.disease
FROM chembl_26.drug_indication
         JOIN chembl_26.compound_records compound_records ON compound_records.record_id = drug_indication.record_id
         JOIN chembl_26.compound_structures compound_structures
              ON compound_records.molregno = compound_structures.molregno
         JOIN mesh.mesh_term mesh_term ON mesh_term.mesh_id::text = drug_indication.mesh_id::text
         LEFT JOIN smiles ON smiles.smiles = compound_structures.canonical_smiles::text
WHERE smiles.drug_id IS NOT NULL;

alter materialized view curated.disease owner to postgres;

-- Drop the existing non-materialized view
drop view if exists curated.diseases;

-- Generate the non-matieralized view
create view curated.diseases(drug_id, mesh_id, compound_name, molregno, canonical_smiles, disease) as
SELECT disease.drug_id,
       disease.mesh_id,
       disease.compound_name,
       disease.molregno,
       disease.canonical_smiles,
       disease.disease
FROM curated.disease;

alter table curated.diseases owner to postgres;
