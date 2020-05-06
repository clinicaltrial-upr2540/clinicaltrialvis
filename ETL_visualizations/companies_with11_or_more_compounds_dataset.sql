with descr as (SELECT DISTINCT
       formulations.molregno,
       drug_indication.mesh_id,
       molecule_dictionary.pref_name as pref_name,
       products.applicant_full_name as company,
       products.approval_date,
       compound_properties.mw_freebase,
       compound_properties.cx_logp,
       compound_properties.aromatic_rings,
       compound_properties.hba,
       compound_properties.hbd,
       compound_properties.rtb,
       compound_properties.psa,
       compound_properties.cx_most_bpka,
       compound_properties.cx_most_apka
FROM products AS products
  LEFT JOIN formulations AS formulations ON formulations.product_id = products.product_id
  INNER JOIN compound_records AS compound_records
          ON compound_records.record_id = formulations.record_id
         AND compound_records.molregno = formulations.molregno
  INNER JOIN drug_indication AS drug_indication ON compound_records.record_id = drug_indication.record_id
  INNER JOIN molecule_dictionary AS molecule_dictionary ON compound_records.molregno = molecule_dictionary.molregno
  INNER JOIN compound_properties AS compound_properties ON compound_properties.molregno = molecule_dictionary.molregno
WHERE molecule_dictionary.max_phase=4
AND products.oral = 1
AND products.ad_type != 'DISCN'
--AND products.applicant_full_name LIKE 'PF%'
--AND product_patents.patent_expire_date >current_date
AND molecule_dictionary.withdrawn_flag=0)
SELECT DISTINCT * from descr
WHERE company not in ('ABHAI INC',
 'ACIC PHARMACEUTICALS INC',
 'ACORDA THERAPEUTICS INC',
 'ACTAVIS INC',
 'ACTAVIS LLC',
 'ACTAVIS TOTOWA LLC AN INDIRECT WHOLLY OWNED SUB OF TEVA PHARMACEUTICALS USA INC',
 'ACTIENT PHARMACEUTICALS LLC',
 'ADAMAS PHARMA LLC',
 'ADARE PHARMACEUTICALS INC',
 'ADDMEDICA SAS',
 'ADHERA THERAPEUTICS INC',
 'AGOURON PHARMACEUTICALS LLC',
 'AIZANT DRUG RESEARCH SOLUTIONS PRIVATE LTD',
 'ALEMBIC LTD',
 'ALKALOIDA CHEMICAL CO ZRT',
 'ALLEGIS HOLDINGS LLC',
 'ALVOGEN GROUP HOLDINGS 2 LLC',
 'ALVOGEN GROUP HOLDINGS 3 LLC',
 'ALVOGEN GROUP HOLDINGS 4 LLC',
 'ALVOGEN GROUP HOLDINGS LLC',
 'ALVOGEN PINE BROOK INC',
 'ALVOGEN PINE BROOK LLC',
 'AMARIN PHARMACEUTICALS IRELAND LTD',
 'AMERICAN ANTIBIOTICS INC',
 'AMGEN INC',
 'AMICI PHARMACEUTICALS LLC',
 'AMNEAL PHARMACEUTICALS HOLDINGS GMBH',
 'ANBEX INC',
 'ANBISON LABORATORY CO LTD',
 'ANCHEN PHARMACEUTICALS TAIWAN INC',
 'ANDA REPOSITORY LLC',
 'ANDOR PHARMACEUTICALS LLC',
 'ANTRIM PHARMACEUTICALS LLC',
 'APEX PHARMACEUTICALS INC',
 'APICORE US LLC',
 'APOPHARMA INC',
 'APOTEX INC RICHMOND HILL',
 'APOTEX INC.',
 'APOTEX TECHNOLOGIES INC',
 'APRECIA PHARMACEUTICALS LLC',
 'AQUESTIVE THERAPEUTICS',
 'ARCO PHARMACEUTICALS LLC',
 'ASTELLAS PHARMA GLOBAL DEVELOPMENT INC',
 'ASTELLAS PHARMA US INC',
 'ASTRAZENECA AB',
 'ASTRAZENECA LP',
 'ASTRAZENECA UK LTD',
 'ATHENA BIOSCIENCES LLC',
 'ATLAS PHARMACEUTICALS LLC',
 'ATON PHARMA INC',
 'AUCTA PHARMACEUTICALS INC',
 'AUROBINDO PHARMA LTD INC',
 'AUXILIUM PHARMACEUTICALS INC',
 'AVANIR PHARMACEUTICALS INC',
 'AYTU BIOSCIENCE INC',
 'BARR LABORATORIES INC SUB TEVA PHARMACEUTICALS USA',
 'BARR PHARMACEUTICALS',
 'BAUSCH HEALTH AMERICAS INC',
 'BAXTER HEALTHCARE CORP',
 'BAYER HEALTHCARE CONSUMER CARE',
 'BAYSHORE PHARMACEUTICALS LLC',
 'BIOCON LTD',
 'BIOMARIN PHARMACEUTICAL INC',
 'BRISTOL MYERS SQUIBB',
 'BRISTOL MYERS SQUIBB CO PHARMACEUTICAL RESEARCH INSTITUTE',
 'BRISTOL MYERS SQUIBB PHARMA CO',
 'BRISTOL-MYERS SQUIBB CO',
 'CAPELLON PHARMACEUTICALS LLC',
 'CEDIPROF INC',
 'CERECOR INC',
 'CEYONE PHARMA LLC',
 'CHANGZHOU PHARMACEUTICAL FACTORY',
 'CHARTWELL LIFE MOLECULES LLC',
 'CHATTEM INC',
 'CHEMI SPA',
 'CHEPLAPHARM ARZNEIMITTEL GMBH',
 'CHIESI USA INC',
 'CHINA RESOURCES SAIKE PHARMACEUTICAL CO LTD',
 'CLOVER PHARMACEUTICALS CORP',
 'CLOVIS ONCOLOGY INC',
 'CMP DEVELOPMENT LLC',
 'CMP PHARMA INC',
 'COBALT LABORATORIES INC',
 'COEPTIS PHARMACEUTICALS INC',
 'CORCEPT THERAPEUTICS INC',
 'CORDEN PHARMA LATINA SPA',
 'CP PHARMACEUTICALS INTERNATIONAL CV',
 'CROSSMEDIKA SA',
 'CUBIST PHARMACEUTICALS INC',
 'CUBIST PHARMACEUTICALS LLC',
 'CURRAX PHARMACEUTICALS LLC',
 'CYCLE PHARMACEUTICALS LTD',
 'DANCO LABORATORIES LLC',
 'DAVA INTERNATIONAL INC',
 'DBL PHARMACEUTICALS INC',
 'DEPO NF SUB LLC A SUB OF ASSERTIO THERAPEUTICS INC',
 'DEVA HOLDING AS',
 'DEXCEL LTD',
 'DOUGLAS PHARMACEUTICALS AMERICA LTD',
 'DOW PHARMACEUTICAL SCIENCES',
 'DR REDDYS LABORATORIES LIMITED',
 'DUCHESNAY INC',
 'EMD SERONO INC',
 'EPI HEALTH LLC',
 'EXALENZ BIOSCIENCE LTD',
 'EXELA PHARMA SCIENCES LLC',
 'EXELTIS USA INC',
 'EYWA PHARMA PTE LTD',
 'FOREST LABORATORIES LLC',
 'FOUGERA PHARMACEUTICALS INC',
 'FOUNDATION CONSUMER HEALTHCARE LLC',
 'FRESENIUS KABI AUSTRIA GMBH',
 'FRESENIUS MEDICAL CARE NORTH AMERICA',
 'FRONTIDA BIOPHARM INC',
 'G AND W LABORATORIES INC',
 'GATE PHARMACEUTICALS',
 'GE HEALTHCARE',
 'GENBIOPRO INC',
 'GENENTECH INC',
 'GENZYME CORP',
 'GILEAD SCIENCES LLC',
 'GLENMARK GENERICS INC USA',
 'GLENMARK PHARMACEUTICALS INC',
 'GLENMARK PHARMACEUTICALS INC USA',
 'GRANULES PHARMACEUTICALS INC',
 'HANGZHOU MINSHENG BINJIANG PHARMACEUTICAL CO LTD',
 'HARRIS PHARMACEUTICAL INC',
 'HELSINN HEALTHCARE SA',
 'HERITAGE LIFE SCIENCES BARBADOS INC',
 'HIGH TECHNOLOGY PHARMACAL CO INC',
 'HOFFMANN-LA ROCHE INC',
 'HORIZON THERAPEUTICS LLC',
 'IDT AUSTRALIA LTD',
 'INCYTE CORP',
 'INSTITUT BIOCHIMIQUE SA (IBSA)',
 'INSYS DEVELOPMENT CO INC',
 'INTERGEL PHARMACEUTICAL INC',
 'INTERGEL PHARMACEUTICALS INC',
 'INTERPHARMA PRAHA AS',
 'IPR PHARMACEUTICALS INC',
 'IRONSHORE PHARMACEUTICALS AND DEVELOPMENT INC',
 'ITALFARMACO SPA',
 'IVAX PHARMACEUTICALS INC',
 'JACOBUS PHARMACEUTICAL CO',
 'JANSSEN BIOTECH INC',
 'JANSSEN PRODUCTS LP',
 'JANSSEN RESEARCH AND DEVELOPMENT LLC',
 'JAZZ PHARMACEUTICALS INC',
 'JAZZ PHARMACEUTICALS IRELAND LTD',
 'JIANGSU HANSOH PHARMACEUTICAL GROUP CO LTD',
 'JIANGXI BOYA SEEHOT PHARMACEUTICAL CO LTD',
 'JUBILANT DRAXIMAGE INC',
 'KADMON PHARMACEUTICALS LLC',
 'KOWA CO LTD',
 'KYOWA KIRIN INC',
 'LABORATOIRE HRA PHARMA',
 'LABORATORIE HRA PHARMA',
 'LABORATORIOUS LICONSA SA',
 'LANDELA PHARMACEUTICAL',
 'LAX PHARMA LLC',
 'LG CHEM LTD',
 'LIFEPHARMA FZE',
 'LOTUS PHARMACEUTICAL CO LTD',
 'LUNDBECK PHARMACEUTICALS LLC',
 'MAINPOINTE PHARMACEUTICALS LLC',
 'MALLINCKRODT INC',
 'MANKIND PHARMA LTD',
 'MCNEIL CONSUMER HEALTHCARE',
 'MEDICIS PHARMACEUTICAL CORP',
 'MEDTECH PRODUCTS INC',
 'MERCK RESEARCH LABORATORIES DIV MERCK CO INC',
 'MERZ PHARMACEUTICALS LLC',
 'METUCHEN PHARMACEUTICALS LLC',
 'MILLENNIUM PHARMACEUTICALS INC',
 'MOUNTAIN LLC',
 'MURTY PHARMACEUTICALS INC',
 'MYLAN PHARMACEUTICALS INC.',
 'NALPROPION PHARMACEUTICALS INC',
 'NATCO PHARMA LIMITED',
 'NAVINTA LLC',
 'NEOS THERAPEUTICS',
 'NEOS THERAPEUTICS INC',
 'NEXTWAVE PHARMACEUTICALS INC',
 'NEXTWAVE PHARMACEUTICALS INC A SUB OF TRIS PHARMA INC',
 'NODEN PHARMA DAC',
 'NORTEC DEVELOPMENT ASSOC INC',
 'NOVA LABORATORIES LTD',
 'NOVARTIS PHARMACEUTICAL CORP',
 'NOVAST LABORATORIES CHINA LTD',
 'NOVELGENIX THERAPEUTICS PVT LTD',
 'NUVO PHARMACEUTICAL INC',
 'NX DEVELOPMENT CORP',
 'ODYSSEY PHARMACEUTICALS INC',
 'OPKO IRELAND GLOBAL HOLDINGS LTD',
 'ORGANON USA INC',
 'ORIENT PHARMA CO LTD',
 'OSI PHARMACEUTICALS LLC',
 'OSMOTICA KERESKEDELMI ES SZOLGALTATO KFT',
 'OSMOTICA PHARMACEUTICAL',
 'OSMOTICA PHARMACEUTICAL CORP',
 'OSMOTICA PHARMACEUTICAL US LLC',
 'OTSUKA AMERICA PHARMACEUTICAL INC',
 'OUTLOOK PHARMACEUTICALS INC',
 'PANACEA BIOTEC LTD',
 'PAR FORMULATIONS PRIVATE LTD',
 'PAR STERILE PRODUCTS LLC',
 'PARKE-DAVIS DIVISION OF PFIZER INC',
 'PD PARTNERS IV LLC',
 'PERRIGO LLC',
 'PERRIGO PHARMA INTERNATIONAL DESIGNATED ACTIVITY CO',
 'PFIZER CONSUMER HEALTHCARE',
 'PFIZER PHARMACEUTICALS INC',
 'PFIZER PHARMACEUTICALS PRODUCTION CORP LTD',
 'PHARMACIA AND UPJOHN',
 'PHARMTAK INC',
 'PIERRE FABRE DERMATOLOGIE',
 'PIRAMAL HEALTHCARE UK LTD',
 'PLD ACQUISITIONS LLC',
 'PLD ACQUISITIONS LLC DBA AVEMA PHARMA SOLUTIONS',
 'PLIVA HRVATSKA DOO',
 'PLIVA PHARMACEUTICAL INDUSTRY INC',
 'POLYGEN PHARMACEUTICALS INC',
 'PRAGMA PHARMACEUTICALS LLC',
 'PROVELL PHARMACEUTICALS LLC',
 'PUMA BIOTECHNOLOGY INC',
 'PURDUE GMP CENTER LLC DBA THE CHAO CENTER INDUSTRIAL PHARMACY',
 'QUAGEN PHARMACEUTICALS LLC',
 'RECIP AB',
 'RECIPHARM PHARMASERVICES PRIVATE LTD',
 'RECKITT BENCKISER LLC',
 'RECORDATI RARE DISEASES INC',
 'RECRO GAINESVILLE LLC',
 'RENATA LTD',
 'ROMARK LABORATORIES',
 'ROMEG THERAPEUTICS LLC',
 'ROUSES POINT PHARMACEUTICALS LLC',
 'RP SCHERER TECHNOLOGIES LLC',
 'RXMTM THERAPEUTICS LLC A WHOLLY OWNED SUB OF CUTISPHARMA INC',
 'SAGENT PHARMACEUTICALS INC',
 'SAI LIFE SCIENCES LTD',
 'SANOFI GENZYME',
 'SANOFI US',
 'SAWAI USA INC',
 'SCHERING CORP',
 'SCIECURE PHARMA INC',
 'SECAN PHARMACEUTICALS INC',
 'SECURA BIO INC',
 'SETON PHARMACEUTICAL LLC',
 'SHANDONG NEW TIME PHARMACEUTICAL CO LTD',
 'SHANGHAI DESANO BIO-PHARMACEUTICALS CO LTD',
 'SHIONOGI INC',
 'SIDMAK LABORATORIES INDIA PVT LTD',
 'SILVERGATE PHARMACEUTICALS INC',
 'SINOTHERAPEUTICS INC',
 'SKYEPHARMA AG',
 'SOFGEN PHARMACEUTICALS',
 'SQUARE PHARMACEUTICALS LTD',
 'STASON PHARMACEUTICALS INC',
 'STIEFEL LABORATORIES INC',
 'STRIDES VIVIMED PTE LTD',
 'STRONGBRIDGE US INC',
 'SUCAMPO PHARMA AMERICAS LLC',
 'SUN PHARMA ADVANCED RESEARCH CO LTD',
 'SUN PHARMA GLOBAL INC',
 'SUNNY PHARMTECH INC',
 'SUNOVION PHARMACEUTICALS INC',
 'SVC PHARMA LP',
 'SWEDISH ORPHAN BIOVITRUM AB PUBL',
 'SYNTHON PHARMACEUTICALS INC',
 'TAIHO ONCOLOGY INC',
 'TASMAN PHARMA INC',
 'TERSERA THERAPEUTICS LLC',
 'TESARO INC',
 'TEVA NEUROSCIENCE INC',
 'TEVA PHARMACEUTICALS INTERNATIONAL GMBH',
 'THE ACME LABORATORIES LTD',
 'TIME-CAP LABORATORIES INC',
 'TOLMAR INC',
 'TOPROL ACQUISITION LLC',
 'TORPHARM INC',
 'TORRENT PHARMACEUTICALS LTD.',
 'TULEX PHARMACEUTICALS INC',
 'UMEDICA LABORATORIES PRIVATE LTD',
 'UNICHEM LABORATORIES LIMITED',
 'UNICHEM PHARMACEUTICALS (USA) INC',
 'UNIMARK REMEDIES LTD',
 'UPSHER SMITH LABORATORIES INC',
 'US WORLDMEDS LLC',
 'USPHARMA WINDLAS LLC',
 'VALEANT INTERNATIONAL BARBADOS SRL',
 'VALEANT PHARMACEUTICALS INTERNATIONAL',
 'VALEANT PHARMACEUTICALS INTERNATIONAL INC',
 'VALEANT PHARMACEUTICALS LUXEMBOURG SARL',
 'VALEANT PHARMACEUTICALS NORTH AMERICA',
 'VALIDUS PHARMACEUTICALS INC',
 'VANDA PHARMACEUTICALS INC',
 'VELOXIS PHARMACEUTICALS INC',
 'VEROSCIENCE LLC',
 'VERTEX PHARMACEUTICALS INC',
 'VIRTUS PHARMACEUTICAL INC',
 'VIVUS INC',
 'VKT PHARMA PRIVATE LTD',
 'VYERA PHARMACEUTICALS LLC',
 'WATSON LABS INC',
 'WILSHIRE PHARMACEUTICALS INC',
 'WINDLAS HEALTHCARE PVT LTD',
 'WOCKHARDT USA LLC',
 'XIAMEN LP PHARMACUETICAL CO LTD',
 'YABAO PHARMACEUTICAL CO LTD BEIJING',
 'YAOPHARMA CO LTD',
 'YILING PHARMACEUTICAL LTD',
 'ZAMBON SPA ITALY')
ORDER BY molregno

