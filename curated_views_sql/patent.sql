DROP MATERIALIZED VIEW IF EXISTS curated.patent CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.patent
(
  number,
  country,
  approved,
  expires,
  drug_id
)
AS 
 WITH drug_bank_patents AS (
         SELECT drug_patents.number,
            drug_patents.country,
            drug_patents.approved,
            drug_patents.expires,
            drug_patents.parent_key AS drug_id
           FROM drug_bank.drug_patents
        )
 SELECT drug_bank_patents.number,
    drug_bank_patents.country,
    drug_bank_patents.approved,
    drug_bank_patents.expires,
    drug_bank_patents.drug_id
   FROM drug_bank_patents;

