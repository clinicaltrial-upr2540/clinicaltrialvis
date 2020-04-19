-- =============================================
-- Materialized View Name: patent
-- Description: this material view is designed to  to show major characteristics and descriptors of a patent with respect to a drug
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding the additional a characteristic as long the drug_patents.number will stay as primary key
-- =============================================

create materialized view patent as
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

alter materialized view patent owner to postgres;

