
-- =============================================
-- Materialized View Name: patent
-- Nonmaterialized View Name: patents
-- Description: this material view is designed to  to show major characteristics and descriptors of a patent with respect to a drug
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding additional characteristics as long the drug_patents.number will stay as primary key
-- =============================================

-- Drop materialized view
drop materialized view if exists curated.patent;

-- Generate the materialized view
create materialized view curated.patent as
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

alter materialized view curated.patent owner to postgres;

-- Drop the existing non-materialized view
drop view if exists curated.patents;

-- Generate the non-matieralized view
create view curated.patents(number, country, approved, expires, drug_id) as
SELECT patent.number,
       patent.country,
       patent.approved,
       patent.expires,
       patent.drug_id
FROM curated.patent;

alter table curated.patents owner to postgres;
