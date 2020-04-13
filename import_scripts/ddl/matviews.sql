DROP MATERIALIZED VIEW IF EXISTS curated.compound CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.compound
(
  drug_id,
  iupac,
  smiles,
  bioavailability,
  molecular_weight,
  molecular_formula,
  clogp,
  psa,
  hba,
  hbd,
  rotatable_bonds,
  aromatic_rings,
  pharmacology,
  compound_name,
  drug_class,
  other_keys,
  type,
  description,
  cas_number,
  unii,
  average_mass,
  monoisotopic_mass,
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
  international_brands,
  pdb_entries,
  fda_label,
  msds,
  food_interactions,
  drug_interactions_count,
  toxicity,
  atc_code
)
AS 
 WITH iupac AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS iupac
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'IUPAC Name'::text
        ), smiles AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS smiles
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'SMILES'::text
        ), mw AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.kind,
            drug_calculated_properties.value AS mw
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Monoisotopic Weight'::text
        ), mf AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS mf
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Molecular Formula'::text
        ), drug_class AS (
         SELECT uspclass.drugname,
            uspclass.uspclassification AS drug_class
           FROM kegg.uspclass
        ), ba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.kind,
            drug_calculated_properties.value
           FROM drug_bank.drug_calculated_properties drug_calculated_properties
          WHERE drug_calculated_properties.kind ~~ 'Bioavailability'::text
        ), clogp AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS clogp
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'logP'::text AND drug_calculated_properties.source = 'ChemAxon'::text
        ), psa AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS psa
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Polar Surface Area (PSA)'::text
        ), hba AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS hba
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'H Bond Acceptor Count'::text
        ), hbd AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS hbd
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'H Bond Donor Count'::text
        ), rb AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS rotatable_bonds
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Rotatable Bond Count'::text
        ), ar AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS aromatic_rings
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'Number of Rings'::text
        ), pkab AS (
         SELECT drug_calculated_properties.parent_key AS drug_id,
            drug_calculated_properties.value AS pka_basic
           FROM drug_bank.drug_calculated_properties
          WHERE drug_calculated_properties.kind = 'pKa (strongest basic)'::text
        )
 SELECT DISTINCT drug.primary_key AS drug_id,
    iupac.iupac,
    smiles.smiles,
    ba.value AS bioavailability,
    mw.mw AS molecular_weight,
    mf.mf AS molecular_formula,
    clogp.clogp,
    psa.psa,
    hba.hba,
    hbd.hbd,
    rb.rotatable_bonds,
    ar.aromatic_rings,
    'pending'::text AS pharmacology,
    drug.name AS compound_name,
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
    drug_atc_codes.atc_code
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
     LEFT JOIN pkab ON pkab.drug_id = drug.primary_key;

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

DROP MATERIALIZED VIEW IF EXISTS curated.product CASCADE;

CREATE OR REPLACE MATERIALIZED VIEW curated.product
(
  drug_id,
  product_name,
  labeller,
  "ndc-product-code",
  "dpd-id",
  "ema-product-code",
  "ema-ma-number",
  "started-marketing-on",
  "ended-marketing-on",
  "dosage-form",
  strength,
  route,
  "fda-application-number",
  generic,
  "over-the-counter",
  approved,
  country,
  source
)
AS
 SELECT DISTINCT drug.primary_key AS drug_id,
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

