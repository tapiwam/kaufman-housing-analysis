---
layout: default
title: Data Dictionary
nav_order: 3
description: "Field definitions for Kaufman CAD property data"
---

# Kaufman CAD Data Dictionary

Complete reference for all fields in the Kaufman County Central Appraisal District database.

**Version:** 2.0.0  
**Tax Year:** 2025  
**Source:** Kaufman CAD 2025 Certified Full Roll (Supplement 5)  
**Last Updated:** December 2025

## Table of Contents

- [Overview](#overview)
- [Important Parsing Notes](#important-parsing-notes)
- [Main Tables](#main-tables)
  - [appraisal_info](#appraisal_info)
  - [appraisal_entity_info](#appraisal_entity_info)
  - [appraisal_land_detail](#appraisal_land_detail)
  - [appraisal_improvement_info](#appraisal_improvement_info)
  - [appraisal_improvement_detail](#appraisal_improvement_detail)
- [Reference Tables](#reference-tables)
- [Field Mappings](#field-mappings)
- [Known Issues](#known-issues)

## Overview

This data dictionary documents all fields in the Kaufman CAD property appraisal database. The data originates from fixed-width text files that are parsed and loaded into PostgreSQL.

**Key Concepts:**

- **Property (prop_id):** Unique identifier for each parcel
- **Entity:** Taxing jurisdiction (City, County, School District, etc.)
- **Homesite:** Primary residence designation (affects taxation)
- **Appraised Value:** Official value for tax purposes
- **Assessed Value:** Value used for tax calculation (may include caps/exemptions)

## Important Parsing Notes

### Assessed Value Correction

**Field:** `assessed_val` in `appraisal_entity_info`  
**Issue:** Original fixed-width file had incorrect column positions causing value scrambling

**Correction Formula:**

```python
corrected_value = (value % 100) * 10000 + ((value - (value % 100)) / 1000000000) / 100
```

**Example:**

- Raw value: `991200000000036`
- Corrected: `$369,912`
- Calculation: `(36 × 10,000) + (991,200 ÷ 100) = 360,000 + 9,912 = 369,912`

**Implementation:** `app/services/file_reader.py` - `parse_value()` function

### Character Encoding

All files use **Latin-1 (ISO-8859-1)** encoding, not UTF-8. This is critical for proper parsing.

### Fixed-Width Format

Each record is a single line with fields at specific character positions. See `config/file_layouts.json` for exact positions.

## Main Tables

### appraisal_info

Main property information including owner and address details.

**Table:** `cad.appraisal_info`  
**Primary Key:** `id` (auto-increment)  
**Source File:** `APPRAISAL_INFO.TXT`  
**Records:** ~207,000

| Column            | Type         | Nullable | Description                | Notes                                 |
| ----------------- | ------------ | -------- | -------------------------- | ------------------------------------- |
| id                | SERIAL       | NO       | Auto-increment primary key | Database-generated                    |
| prop_id           | BIGINT       | YES      | Property ID                | Main identifier, links to all tables  |
| prop_type_cd      | VARCHAR(1)   | YES      | Property type code         | R=Real, P=Personal, M=Mineral, A=Auto |
| prop_val_yr       | INTEGER      | YES      | Property value year        | Tax year (2025)                       |
| owner_id          | BIGINT       | YES      | Owner ID                   | Internal CAD owner identifier         |
| owner_name        | VARCHAR(70)  | YES      | Owner name                 | As recorded by CAD                    |
| confidential_flag | VARCHAR(1)   | YES      | Confidential flag          | Privacy indicator                     |
| mail_addr_line1   | VARCHAR(80)  | YES      | Mailing address line 1     | Primary mailing address               |
| mail_addr_line2   | VARCHAR(40)  | YES      | Mailing address line 2     | Additional address info               |
| mail_city         | VARCHAR(50)  | YES      | Mailing city               | Important for occupancy analysis      |
| mail_state        | VARCHAR(50)  | YES      | Mailing state              | Usually "TX" or "TEXAS"               |
| mail_country      | VARCHAR(5)   | YES      | Mailing country code       | Usually blank (US assumed)            |
| mail_zip          | VARCHAR(10)  | YES      | Mailing ZIP code           | 5 or 9 digit format                   |
| situs_street      | VARCHAR(60)  | YES      | Property street address    | Physical location                     |
| situs_city        | VARCHAR(30)  | YES      | Property city              | Physical location city                |
| situs_zip         | VARCHAR(10)  | YES      | Property ZIP code          | Physical location ZIP                 |
| legal_desc        | VARCHAR(340) | YES      | Legal description          | Subdivision, block, lot details       |
| created_at        | TIMESTAMP    | NO       | Record creation timestamp  | Database timestamp                    |

**Key Relationships:**

- `prop_id` → `appraisal_entity_info.prop_id`
- `prop_id` → `appraisal_land_detail.prop_id`
- `prop_id` → `appraisal_improvement_info.prop_id`

**Common Queries:**

```sql
-- Find properties by subdivision
SELECT * FROM cad.appraisal_info
WHERE UPPER(legal_desc) LIKE '%GATEWAY PARK%';

-- Owner-occupied vs investor (mailing city match)
SELECT
    CASE
        WHEN mail_city = situs_city THEN 'Owner-Occupied'
        ELSE 'Investor'
    END as occupancy_type,
    COUNT(*)
FROM cad.appraisal_info
GROUP BY occupancy_type;
```

---

### appraisal_entity_info

Property values by taxing entity (jurisdiction).

**Table:** `cad.appraisal_entity_info`  
**Primary Key:** None (composite: prop_id, tax_year, entity_cd)  
**Source File:** `APPRAISAL_ENTITY_INFO.TXT`  
**Records:** ~511,000

| Column       | Type        | Nullable | Description               | Notes                                                                 |
| ------------ | ----------- | -------- | ------------------------- | --------------------------------------------------------------------- |
| prop_id      | BIGINT      | NO       | Property ID               | Links to appraisal_info                                               |
| tax_year     | INTEGER     | NO       | Tax year                  | 2025 for current dataset                                              |
| entity_id    | VARCHAR(5)  | NO       | Entity ID                 | Internal entity identifier                                            |
| entity_cd    | VARCHAR(10) | YES      | Entity code               | CF=City of Forney, KC=Kaufman County, SF=Forney ISD, RB=Road & Bridge |
| entity_name  | VARCHAR(50) | YES      | Entity name               | Full jurisdiction name                                                |
| taxable_val  | BIGINT      | YES      | Taxable value             | Value subject to tax                                                  |
| exempt_val   | BIGINT      | YES      | Exempt value              | Exemptions (homestead, etc.)                                          |
| freeze_val   | BIGINT      | YES      | Freeze value              | Senior/disabled freeze amount                                         |
| assessed_val | BIGINT      | YES      | Assessed value            | **CORRECTED** - See parsing notes                                     |
| created_at   | TIMESTAMP   | NO       | Record creation timestamp | Database timestamp                                                    |

**Entity Code Reference:**

| Code | Entity Name    | Description                                 |
| ---- | -------------- | ------------------------------------------- |
| CF   | CITY OF FORNEY | City tax jurisdiction                       |
| KC   | KAUFMAN COUNTY | County tax jurisdiction                     |
| SF   | FORNEY ISD     | School district (may differ from entity_cd) |
| RB   | ROAD & BRIDGE  | County road district                        |

**Important Notes:**

1. **Multiple Records Per Property:** Each property has one record per taxing entity
2. **Assessed Value:** Use `MAX(assessed_val)` to get official appraised value
3. **Parsing Correction:** Values corrected on load - see [parsing notes](#assessed-value-correction)

**Common Queries:**

```sql
-- Get official appraised value
SELECT
    prop_id,
    MAX(assessed_val) as appraised_value
FROM cad.appraisal_entity_info
GROUP BY prop_id;

-- Values by entity
SELECT
    entity_cd,
    entity_name,
    COUNT(*) as property_count,
    SUM(assessed_val) as total_value
FROM cad.appraisal_entity_info
GROUP BY entity_cd, entity_name;
```

---

### appraisal_land_detail

Land parcel details including acreage and valuations.

**Table:** `cad.appraisal_land_detail`  
**Primary Key:** Composite (prop_id, tax_year, land_seg_id)  
**Source File:** `APPRAISAL_LAND_DETAIL.TXT`  
**Records:** ~230,000

| Column         | Type        | Nullable | Description               | Notes                          |
| -------------- | ----------- | -------- | ------------------------- | ------------------------------ |
| prop_id        | BIGINT      | NO       | Property ID               | Links to appraisal_info        |
| tax_year       | INTEGER     | NO       | Tax year                  | 2025                           |
| land_seg_id    | BIGINT      | NO       | Land segment ID           | Multiple segments per property |
| land_type_cd   | VARCHAR(8)  | YES      | Land type code            | Residential, commercial, etc.  |
| land_type_desc | VARCHAR(25) | YES      | Land type description     | Text description               |
| state_cd       | VARCHAR(5)  | YES      | State code                | **HS**=Homesite, others vary   |
| ag_flag        | VARCHAR(1)  | YES      | Agricultural flag         | Y/N                            |
| land_sqft      | BIGINT      | YES      | Land square feet          | Area in sq ft                  |
| land_acres     | BIGINT      | YES      | Land acres                | Area in acres                  |
| mkt_val        | BIGINT      | YES      | Market value              | Market value of land           |
| prod_val       | BIGINT      | YES      | Productivity value        | Agricultural use value         |
| land_class     | VARCHAR(5)  | YES      | Land classification       | Classification code            |
| soil_cd        | VARCHAR(10) | YES      | Soil code                 | Soil type identifier           |
| appraised_val  | BIGINT      | YES      | Appraised value           | Official land value            |
| ag_apply_cd    | VARCHAR(5)  | YES      | Ag application code       | Agricultural use code          |
| adj_cd         | VARCHAR(10) | YES      | Adjustment code           | Value adjustments              |
| created_at     | TIMESTAMP   | NO       | Record creation timestamp | Database timestamp             |

**State Code Reference:**

| Code     | Description                       |
| -------- | --------------------------------- |
| HS       | Homesite - primary residence land |
| (others) | Various non-homesite designations |

**Common Queries:**

```sql
-- Aggregate land values by homesite status
SELECT
    prop_id,
    SUM(CASE WHEN state_cd = 'HS' THEN appraised_val ELSE 0 END) as homesite_land_value,
    SUM(CASE WHEN state_cd != 'HS' THEN appraised_val ELSE 0 END) as non_homesite_land_value,
    SUM(land_acres) as total_acres
FROM cad.appraisal_land_detail
GROUP BY prop_id;
```

---

### appraisal_improvement_info

Building and structure information.

**Table:** `cad.appraisal_improvement_info`  
**Primary Key:** Composite (prop_id, tax_year, impr_id)  
**Source File:** `APPRAISAL_IMPROVEMENT_INFO.TXT`  
**Records:** ~175,000

| Column            | Type        | Nullable | Description                  | Notes                            |
| ----------------- | ----------- | -------- | ---------------------------- | -------------------------------- |
| prop_id           | BIGINT      | NO       | Property ID                  | Links to appraisal_info          |
| tax_year          | INTEGER     | NO       | Tax year                     | 2025                             |
| impr_id           | BIGINT      | NO       | Improvement ID               | Unique per structure             |
| impr_type_cd      | VARCHAR(10) | YES      | Improvement type code        | Structure type                   |
| impr_type_desc    | VARCHAR(25) | YES      | Improvement type description | E.g., "Residential"              |
| state_cd          | VARCHAR(5)  | YES      | State code                   | Similar to land state codes      |
| homesite_flag     | VARCHAR(1)  | YES      | Homesite flag                | **Y**=Primary residence, N=Other |
| year_built        | INTEGER     | YES      | Year built                   | **Often NULL** in this dataset   |
| percent_complete  | DECIMAL     | YES      | Percent complete             | Construction completion %        |
| depreciation_flag | VARCHAR(1)  | YES      | Depreciation flag            | Depreciation indicator           |
| appraised_val     | BIGINT      | YES      | Appraised value              | Value of improvement             |
| created_at        | TIMESTAMP   | NO       | Record creation timestamp    | Database timestamp               |

**Important Notes:**

1. **year_built NULL:** This field is rarely populated in the Kaufman CAD dataset
2. **homesite_flag:** Critical for distinguishing primary residence from other structures

**Common Queries:**

```sql
-- Improvement values by homesite status
SELECT
    prop_id,
    SUM(CASE WHEN homesite_flag = 'Y' THEN appraised_val ELSE 0 END) as homesite_improvement_value,
    SUM(CASE WHEN homesite_flag != 'Y' THEN appraised_val ELSE 0 END) as non_homesite_improvement_value
FROM cad.appraisal_improvement_info
GROUP BY prop_id;
```

---

### appraisal_improvement_detail

Detailed breakdown of building components.

**Table:** `cad.appraisal_improvement_detail`  
**Primary Key:** Composite (prop_id, tax_year, impr_id, detail_id)  
**Source File:** `APPRAISAL_IMPROVEMENT_DETAIL.TXT`  
**Records:** ~610,000

| Column         | Type        | Nullable | Description               | Notes                         |
| -------------- | ----------- | -------- | ------------------------- | ----------------------------- |
| prop_id        | BIGINT      | NO       | Property ID               | Links to appraisal_info       |
| tax_year       | INTEGER     | NO       | Tax year                  | 2025                          |
| impr_id        | BIGINT      | NO       | Improvement ID            | Links to improvement_info     |
| detail_id      | BIGINT      | NO       | Detail ID                 | Unique component ID           |
| component_cd   | VARCHAR(10) | YES      | Component code            | Type of component             |
| component_desc | VARCHAR(30) | YES      | Component description     | E.g., "Living Area", "Garage" |
| living_area    | INTEGER     | YES      | Living area sqft          | Square footage                |
| component_val  | BIGINT      | YES      | Component value           | Value of this component       |
| created_at     | TIMESTAMP   | NO       | Record creation timestamp | Database timestamp            |

**Common Components:**

- Living Area (main house square footage)
- Garage
- Porch/Deck
- Additional structures

**Common Queries:**

```sql
-- Total living area and value
SELECT
    i.prop_id,
    i.owner_name,
    SUM(d.living_area) as total_sqft,
    SUM(d.component_val) as total_improvement_value
FROM cad.appraisal_info i
JOIN cad.appraisal_improvement_detail d ON i.prop_id = d.prop_id
GROUP BY i.prop_id, i.owner_name;
```

---

## Reference Tables

### appraisal_header

Export metadata and information.

| Column            | Type        | Description           |
| ----------------- | ----------- | --------------------- |
| export_date       | VARCHAR(10) | Date of export        |
| export_time       | VARCHAR(6)  | Time of export        |
| tax_year          | INTEGER     | Tax year              |
| roll_description  | VARCHAR(30) | Roll type description |
| supplement_number | VARCHAR(10) | Supplement number     |
| cad_name          | VARCHAR(50) | CAD district name     |

### appraisal_entity

Taxing entity codes and descriptions.

| Column      | Type       | Description      |
| ----------- | ---------- | ---------------- |
| prop_id     | BIGINT     | Property ID      |
| entity_type | VARCHAR(1) | Entity type code |

### appraisal_entity_totals

Aggregate totals by taxing entity.

| Column          | Type        | Description           |
| --------------- | ----------- | --------------------- |
| entity_cd       | VARCHAR(10) | Entity code           |
| entity_name     | VARCHAR(50) | Entity name           |
| total_appraised | BIGINT      | Total appraised value |
| total_taxable   | BIGINT      | Total taxable value   |
| property_count  | INTEGER     | Count of properties   |

### appraisal_state_code

State classification codes (Homesite, agricultural, etc.)

### appraisal_country_code

Country codes for mailing addresses.

### appraisal_abstract_subdv

Abstract and subdivision information.

---

## Field Mappings

### Property Type Codes

| Code | Description       |
| ---- | ----------------- |
| R    | Real Property     |
| P    | Personal Property |
| M    | Mineral Interest  |
| A    | Automobile        |

### Entity Codes (Common)

| Code | Name           | Type            |
| ---- | -------------- | --------------- |
| CF   | CITY OF FORNEY | City            |
| KC   | KAUFMAN COUNTY | County          |
| SF   | FORNEY ISD     | School District |
| RB   | ROAD & BRIDGE  | Road District   |

### State Codes

| Code      | Description           | Use                                 |
| --------- | --------------------- | ----------------------------------- |
| HS        | Homesite              | Primary residence land/improvements |
| A1        | Agricultural          | Farm/ranch land                     |
| (various) | Other classifications | Non-homesite designations           |

---

## Known Issues

### 1. Assessed Value Parsing Error

**Affected:** `appraisal_entity_info.assessed_val`  
**Status:** ✅ FIXED  
**Fix:** Correction formula applied during parsing  
**Details:** See [Assessed Value Correction](#assessed-value-correction)

### 2. Year Built Data Missing

**Affected:** `appraisal_improvement_info.year_built`  
**Status:** ⚠️ DATA LIMITATION  
**Impact:** Field is NULL for most properties  
**Workaround:** Use other date fields or external sources

### 3. Legal Description Truncation

**Affected:** `appraisal_info.legal_desc`  
**Status:** ✅ FIXED  
**Fix:** Increased VARCHAR length from 150 to 340  
**Details:** Some legal descriptions exceed original schema limit

### 4. Mailing Address Variations

**Affected:** `appraisal_info.mail_city`  
**Status:** ⚠️ DATA QUALITY  
**Impact:** City names may have variations (e.g., "FARMERS" vs "FARMERS BRANCH")  
**Workaround:** Use UPPER() and normalization in queries

---

## Cross-Reference with Source Files

This data dictionary is derived from:

1. **PDF Documentation:** Original CAD export format specification
2. **config/file_layouts.json:** Actual parsing configuration used
3. **Database Schema:** `sql/001_create_schema.sql`

**Differences from PDF:**

- **assessed_val:** Column positions corrected in JSON config
- **legal_desc:** Length increased from 150 to 340 characters
- **Additional fields:** Some filler fields excluded for clarity

---

## Version History

| Version | Date     | Changes                                                            |
| ------- | -------- | ------------------------------------------------------------------ |
| 2.0.0   | Dec 2025 | Major update: assessed_val correction, increased legal_desc length |
| 1.0.0   | Oct 2025 | Initial version based on CAD documentation                         |

---

**For questions or corrections, see project README or contact maintainer.**
