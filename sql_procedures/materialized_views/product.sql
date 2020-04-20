-- =============================================
-- Materialized View Name: product
-- Description: this material view is designed to  to show major characteristics and descriptors of a branded product in a single view
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding the additional a characteristic as long the drug_id will stay as primary key
-- =============================================

create materialized view product as
SELECT DISTINCT drug.primary_key   AS drug_id,
                drug_products.name AS product_name,
                drug_products.labeller,
                drug_products."ndc-product-code",
                drug_products."dpd-id",
                drug_products."ema-product-code",
                drug_products."ema-ma-number",
                drug_products."started-marketing-on",
                drug_products."ended-marketing-on",
                drug_products."dosage-form",
                drug_products.strength,
                drug_products.route,
                drug_products."fda-application-number",
                drug_products.generic,
                drug_products."over-the-counter",
                drug_products.approved,
                drug_products.country,
                drug_products.source
FROM drug_bank.drug drug
         JOIN drug_bank.drug_products drug_products ON drug.primary_key = drug_products.parent_key;

alter materialized view product owner to postgres;

