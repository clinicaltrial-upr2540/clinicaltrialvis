
-- =============================================
-- Materialized View Name: disease
-- Description: this material view is designed to show the disease classification from mesh term database in association which compounds
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding the additional a characteristic as long the SMILES will stay as primary key
-- =============================================

create materialized view disease as
with mesh_info as (
select DISTINCT drug_indication.mesh_id AS mesh_id,
                compound_records.compound_name AS compound_name,
                compound_records.molregno AS molregno,
                compound_structures.canonical_smiles AS canonical_smiles,
                mesh_term.disease AS disease
from drugdata.chembl_26.drug_indication
inner join drugdata.chembl_26.compound_records compound_records on compound_records.record_id = drug_indication.record_id
inner join drugdata.chembl_26.compound_structures compound_structures on compound_records.molregno = compound_structures.molregno
inner join drugdata.mesh.mesh_term mesh_term on mesh_term.mesh_id = drug_indication.mesh_id )
select mesh_id,
       compound_name,
       canonical_smiles,
       disease
 from mesh_info

