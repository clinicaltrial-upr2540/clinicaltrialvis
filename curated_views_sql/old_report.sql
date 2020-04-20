DROP MATERIALIZED VIEW IF EXISTS curated.commondescriptor CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.commondescriptor
(
  primary_key,
  drug_name,
  name,
  labeller,
  ndc_product_code,
  dpd_id,
  ema_product_code,
  ema_ma_number,
  started_marketing_on,
  ended_marketing_on,
  dosage_form,
  strength,
  route,
  fda_application_number,
  generic,
  over_the_counter,
  approved,
  country,
  source,
  type,
  description,
  c_number,
  unii,
  average_ms,
  monoisotopic_ms,
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
  international_brands
)
AS 
 WITH temp_table AS (
         SELECT DISTINCT drug.primary_key,
            drug.name AS drug_name,
            drug_products.name,
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
            drug.toxicity
           FROM drug_bank.drug_products drug_products
             JOIN drug_bank.drug drug ON drug_products.parent_key = drug.primary_key
        )
 SELECT temp_table.primary_key,
    string_agg(DISTINCT temp_table.drug_name, '||'::text) AS drug_name,
    string_agg(DISTINCT temp_table.name, '||'::text) AS name,
    string_agg(DISTINCT temp_table.labeller, '||'::text) AS labeller,
    string_agg(DISTINCT temp_table."ndc-product-code", '||'::text) AS ndc_product_code,
    string_agg(DISTINCT temp_table."dpd-id", '||'::text) AS dpd_id,
    string_agg(DISTINCT temp_table."ema-product-code", '||'::text) AS ema_product_code,
    string_agg(DISTINCT temp_table."ema-ma-number", '||'::text) AS ema_ma_number,
    string_agg(DISTINCT temp_table."started-marketing-on", '||'::text) AS started_marketing_on,
    string_agg(DISTINCT temp_table."ended-marketing-on", '||'::text) AS ended_marketing_on,
    string_agg(DISTINCT temp_table."dosage-form", '||'::text) AS dosage_form,
    string_agg(DISTINCT temp_table.strength, '||'::text) AS strength,
    string_agg(DISTINCT temp_table.route, '||'::text) AS route,
    string_agg(DISTINCT temp_table."fda-application-number", '||'::text) AS fda_application_number,
    string_agg(DISTINCT temp_table.generic, '||'::text) AS generic,
    string_agg(DISTINCT temp_table."over-the-counter", '||'::text) AS over_the_counter,
    string_agg(DISTINCT temp_table.approved, '||'::text) AS approved,
    string_agg(DISTINCT temp_table.country, '||'::text) AS country,
    string_agg(DISTINCT temp_table.source, '||'::text) AS source,
    string_agg(DISTINCT temp_table.type, '||'::text) AS type,
    string_agg(DISTINCT temp_table.description, '||'::text) AS description,
    string_agg(DISTINCT temp_table.cas_number, '||'::text) AS c_number,
    string_agg(DISTINCT temp_table.unii, '||'::text) AS unii,
    string_agg(DISTINCT temp_table.average_mass, '||'::text) AS average_ms,
    string_agg(DISTINCT temp_table.monoisotopic_mass, '||'::text) AS monoisotopic_ms,
    string_agg(DISTINCT temp_table.state, '||'::text) AS state,
    string_agg(DISTINCT temp_table.synthesis_reference, '||'::text) AS synthesis_reference,
    string_agg(DISTINCT temp_table.indication, '||'::text) AS indication,
    string_agg(DISTINCT temp_table.pharmacodynamics, '||'::text) AS pharmacodynamics,
    string_agg(DISTINCT temp_table.mechanism_of_action, '||'::text) AS mechanism_of_action,
    string_agg(DISTINCT temp_table.metabolism, '||'::text) AS metabolism,
    string_agg(DISTINCT temp_table.absorption, '||'::text) AS absorption,
    string_agg(DISTINCT temp_table.half_life, '||'::text) AS half_life,
    string_agg(DISTINCT temp_table.protein_binding, '||'::text) AS protein_binding,
    string_agg(DISTINCT temp_table.route_of_elimination, '||'::text) AS route_of_elimination,
    string_agg(DISTINCT temp_table.volume_of_distribution, '||'::text) AS volume_of_distribution,
    string_agg(DISTINCT temp_table.clearance, '||'::text) AS clearance,
    string_agg(DISTINCT temp_table.international_brands, '||'::text) AS international_brands
   FROM temp_table
  GROUP BY temp_table.primary_key;

