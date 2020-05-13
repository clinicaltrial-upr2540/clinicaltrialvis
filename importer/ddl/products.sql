
-- =============================================
-- Materialized View Name: product
-- Nonmaterialized View Name: products
-- Description: this material view is designed to  to show major characteristics and descriptors of a branded product in a single view
-- PROGRAMMING NOTES
--      this materialized view can be modified by adding additional characteristics as long the drug_id will stay as primary key
-- =============================================

-- Drop the existing non-materialized view
drop view if exists curated.products;

-- Drop materialized view
drop materialized view if exists curated.product;

-- Generate the materialized view
create materialized view curated.product as
WITH t200ppbp2016 AS (
    SELECT DISTINCT t200ppbp2016_1.index    AS by_nbr_presc_rank_2016,
                    t200ppbp2016_1.drug_name,
                    t200ppbp2016_1.drug_brand_name,
                    t200ppbp2016_1.target_d AS disease_target
    FROM top200.t200_pharm_prd_by_pres_2016 t200ppbp2016_1
),
     t200ppbrs2018 AS (
         SELECT DISTINCT t200ppbrs2018_1.index          AS by_nbr_retail_sales_rank_2018,
                         t200ppbrs2018_1.drug_name,
                         t200ppbrs2018_1.drug_brand_name,
                         t200ppbrs2018_1.scripts_number AS retail_sales_revenue_2018,
                         t200ppbrs2018_1.target_d       AS disease_target
         FROM top200.t200_pharm_prd_by_rtl_sls_2018 t200ppbrs2018_1
     ),
     t200smprs2018 AS (
         SELECT DISTINCT t200smprs2018_1.index          AS small_mole_retail_sales_rank_2018,
                         t200smprs2018_1.drug_name,
                         t200smprs2018_1.drug_brand_name,
                         t200smprs2018_1.scripts_number AS small_mole_revenue_2018,
                         t200smprs2018_1.target_d       AS disease_target
         FROM top200.t200_sm_mol_pharm_rtl_sls_2018 t200smprs2018_1
     )
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
                drug_products.source,
                t200ppbp2016.by_nbr_presc_rank_2016,
                t200ppbrs2018.by_nbr_retail_sales_rank_2018,
                t200smprs2018.small_mole_retail_sales_rank_2018,
                t200smprs2018.small_mole_revenue_2018,
                t200ppbrs2018.retail_sales_revenue_2018,
                t200ppbp2016.disease_target
FROM drug_bank.drug drug
         JOIN drug_bank.drug_products drug_products ON drug.primary_key = drug_products.parent_key
         LEFT JOIN t200ppbp2016 t200ppbp2016 ON t200ppbp2016.drug_name = drug_products.name
         LEFT JOIN t200ppbrs2018 t200ppbrs2018 ON t200ppbrs2018.drug_name = drug_products.name
         LEFT JOIN t200smprs2018 t200smprs2018 ON t200smprs2018.drug_name = drug_products.name;

alter materialized view curated.product owner to postgres;

-- Generate the non-matieralized view
create view curated.products(drug_id, product_name, labeller, "ndc-product-code", "dpd-id", "ema-product-code", "ema-ma-number", "started-marketing-on", "ended-marketing-on", "dosage-form", strength, route, "fda-application-number", generic, "over-the-counter", approved, country, source, by_nbr_presc_rank_2016, by_nbr_retail_sales_rank_2018, small_mole_retail_sales_rank_2018, small_mole_revenue_2018, retail_sales_revenue_2018, disease_target) as
SELECT product.drug_id,
       product.product_name,
       product.labeller,
       product."ndc-product-code",
       product."dpd-id",
       product."ema-product-code",
       product."ema-ma-number",
       product."started-marketing-on",
       product."ended-marketing-on",
       product."dosage-form",
       product.strength,
       product.route,
       product."fda-application-number",
       product.generic,
       product."over-the-counter",
       product.approved,
       product.country,
       product.source,
       product.by_nbr_presc_rank_2016,
       product.by_nbr_retail_sales_rank_2018,
       product.small_mole_retail_sales_rank_2018,
       product.small_mole_revenue_2018,
       product.retail_sales_revenue_2018,
       product.disease_target
FROM curated.product;

alter table curated.products owner to postgres;
