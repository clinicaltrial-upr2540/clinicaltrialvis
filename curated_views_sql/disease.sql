DROP MATERIALIZED VIEW IF EXISTS curated.disease CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.disease
(
  mesh_id,
  compound_name,
  canonical_smiles,
  disease
)
AS 
 WITH mesh_info AS (
         SELECT DISTINCT drug_indication.mesh_id,
            compound_records.compound_name,
            compound_records.molregno,
            compound_structures.canonical_smiles,
            mesh_term.disease
           FROM chembl_26.drug_indication
             JOIN chembl_26.compound_records compound_records ON compound_records.record_id = drug_indication.record_id
             JOIN chembl_26.compound_structures compound_structures ON compound_records.molregno = compound_structures.molregno
             JOIN mesh.mesh_term mesh_term ON mesh_term.mesh_id::text = drug_indication.mesh_id::text
        )
 SELECT mesh_info.mesh_id,
    mesh_info.compound_name,
    mesh_info.canonical_smiles,
    mesh_info.disease
   FROM mesh_info;

