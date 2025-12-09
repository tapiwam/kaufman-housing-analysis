---
layout: default
title: Data Layout
nav_order: 4
description: "Technical specifications for CAD data files"
---

# Kaufman CAD Data Export Layout Documentation

> **Note**: This document was created based on analysis of the data files.
> The original layout comes from "Export Totals 2025 Roll through Sup 5.pdf".
> Fields may need adjustment based on the actual PDF specifications.

## Overview

The Kaufman County Appraisal District (CAD) data export consists of multiple fixed-width text files containing property appraisal information. All files share a common prefix pattern: `YYYY-MM-DD_NNNNNN_APPRAISAL_*.TXT`

## File Types

| File Suffix             | Description                            | Record Count |
| ----------------------- | -------------------------------------- | ------------ |
| HEADER                  | Export metadata and header information | 1            |
| INFO                    | Main property/parcel information       | ~104,369     |
| ENTITY                  | Taxing entity codes                    | 65           |
| ENTITY_INFO             | Property-entity relationships          | ~511,086     |
| ENTITY_TOTALS           | Aggregate totals by entity             | 65           |
| LAND_DETAIL             | Land segment details                   | ~102,733     |
| IMPROVEMENT_INFO        | Improvement (building) summary         | ~101,635     |
| IMPROVEMENT_DETAIL      | Detailed improvement data              | ~347,682     |
| IMPROVEMENT_DETAIL_ATTR | Improvement attributes                 | ~408,609     |
| ABSTRACT_SUBDV          | Abstract and subdivision codes         | 2,458        |
| AGENT                   | Agent/representative information       | 998          |
| LAWSUIT                 | Legal/lawsuit information              | 333          |
| MOBILE_HOME_INFO        | Mobile home specific data              | 7,767        |
| TAX_DEFERRAL_INFO       | Tax deferral records                   | 959          |
| STATE_CODE              | State classification codes             | 79           |
| COUNTRY_CODE            | Country codes                          | 7            |
| UDI                     | Undivided interest data                | 16           |

---

## File Layouts

### 1. APPRAISAL_HEADER

Export header containing metadata about the export.

| Position | Length | Field Name        | Type | Description              |
| -------- | ------ | ----------------- | ---- | ------------------------ |
| 1        | 10     | export_date       | CHAR | Export date (MM/DD/YYYY) |
| 11       | 6      | export_time       | CHAR | Export time (HH:MM)      |
| 17       | 4      | tax_year          | CHAR | Tax year                 |
| 21       | 30     | roll_description  | CHAR | Roll description         |
| 51       | 10     | supplement_number | CHAR | Supplement number        |
| 61       | 4      | record_count      | NUM  | Number of records        |
| 65       | 10     | export_type       | CHAR | Export type (MULT)       |
| 75       | 50     | property_types    | CHAR | Property type codes      |
| 125      | 50     | cad_name          | CHAR | CAD district name        |
| 175      | 20     | exported_by       | CHAR | User who exported        |
| 195      | 30     | version_info      | CHAR | Software version         |

---

### 2. APPRAISAL_INFO

Main property information file - contains comprehensive parcel data.

| Position | Length | Field Name         | Type | Description                     |
| -------- | ------ | ------------------ | ---- | ------------------------------- |
| 1        | 12     | prop_id            | NUM  | Property ID                     |
| 13       | 1      | prop_type_cd       | CHAR | Property type code              |
| 14       | 5      | prop_val_yr        | NUM  | Property value year             |
| 19       | 15     | sup_num            | NUM  | Supplement number               |
| 34       | 10     | exemption_cd       | CHAR | Exemption code                  |
| 44       | 80     | exemption_desc     | CHAR | Exemption description           |
| 124      | 200    | filler_1           | CHAR | Reserved space                  |
| 324      | 30     | geo_id             | CHAR | Geographic ID                   |
| 354      | 12     | owner_id           | NUM  | Owner ID                        |
| 366      | 70     | owner_name         | CHAR | Owner name                      |
| 436      | 1      | confidential_flag  | CHAR | Confidential indicator          |
| 437      | 12     | py_owner_id        | NUM  | Previous year owner ID          |
| 449      | 70     | py_owner_name      | CHAR | Previous year owner name        |
| 519      | 80     | addr_line1         | CHAR | Owner address line 1            |
| 599      | 80     | addr_line2         | CHAR | Owner address line 2            |
| 679      | 50     | city               | CHAR | Owner city                      |
| 729      | 50     | state              | CHAR | Owner state                     |
| 779      | 20     | country            | CHAR | Owner country                   |
| 799      | 10     | zip                | CHAR | Owner ZIP code                  |
| 809      | 2      | confidential_flag2 | CHAR | Additional confidential flags   |
| 811      | 1      | delivery_point     | CHAR | Delivery point code             |
| 812      | 1      | exemption_flag     | CHAR | Has exemption flag              |
| 813      | 40     | situs_street       | CHAR | Property street address         |
| 853      | 30     | situs_city         | CHAR | Property city                   |
| 883      | 10     | situs_zip          | CHAR | Property ZIP                    |
| 893      | 150    | legal_desc         | CHAR | Legal description               |
| 1043     | 150    | legal_desc2        | CHAR | Legal description continued     |
| 1193     | 14     | legal_acreage      | NUM  | Legal acreage                   |
| 1207     | 10     | abs_subdv_cd       | CHAR | Abstract/subdivision code       |
| 1217     | 30     | neighborhood_cd    | CHAR | Neighborhood code               |
| 1247     | 10     | block              | CHAR | Block                           |
| 1257     | 10     | tract_or_lot       | CHAR | Tract or lot                    |
| 1267     | 15     | land_hstd_val      | NUM  | Land homestead value            |
| 1282     | 15     | land_non_hstd_val  | NUM  | Land non-homestead value        |
| 1297     | 15     | land_ag_mkt_val    | NUM  | Land ag market value            |
| 1312     | 15     | land_ag_use_val    | NUM  | Land ag use value               |
| 1327     | 15     | land_timber_mkt    | NUM  | Land timber market              |
| 1342     | 15     | land_timber_use    | NUM  | Land timber use                 |
| 1357     | 15     | impr_hstd_val      | NUM  | Improvement homestead value     |
| 1372     | 15     | impr_non_hstd_val  | NUM  | Improvement non-homestead value |
| 1387     | 15     | personal_val       | NUM  | Personal property value         |
| 1402     | 15     | mineral_val        | NUM  | Mineral value                   |
| 1417     | 15     | appraised_val      | NUM  | Total appraised value           |
| 1432     | 15     | hs_cap_val         | NUM  | Homestead cap value             |
| 1447     | 15     | assessed_val       | NUM  | Assessed value                  |
| 1462     | 1      | arb_flag           | CHAR | ARB flag                        |
| 1463     | 12     | deed_vol           | CHAR | Deed volume                     |
| 1475     | 12     | deed_page          | CHAR | Deed page                       |
| 1487     | 8      | deed_date          | CHAR | Deed date (MMDDYYYY)            |
| 1495     | 15     | sale_price         | NUM  | Sale price                      |

---

### 3. APPRAISAL_ENTITY

Taxing entity reference table.

| Position | Length | Field Name  | Type | Description           |
| -------- | ------ | ----------- | ---- | --------------------- |
| 1        | 12     | prop_id     | NUM  | Property ID           |
| 13       | 1      | entity_type | CHAR | Entity type (F=Fixed) |
| 14       | 5      | filler      | CHAR | Reserved              |

---

### 4. APPRAISAL_ENTITY_INFO

Property to taxing entity relationships and values.

| Position | Length | Field Name   | Type | Description    |
| -------- | ------ | ------------ | ---- | -------------- |
| 1        | 12     | prop_id      | NUM  | Property ID    |
| 13       | 4      | tax_year     | NUM  | Tax year       |
| 17       | 5      | entity_id    | CHAR | Entity ID      |
| 22       | 10     | entity_cd    | CHAR | Entity code    |
| 32       | 50     | entity_name  | CHAR | Entity name    |
| 82       | 15     | taxable_val  | NUM  | Taxable value  |
| 97       | 15     | exempt_val   | NUM  | Exempt value   |
| 112      | 15     | freeze_val   | NUM  | Freeze value   |
| 127      | 15     | assessed_val | NUM  | Assessed value |

---

### 5. APPRAISAL_LAND_DETAIL

Land segment detail records.

| Position | Length | Field Name     | Type | Description           |
| -------- | ------ | -------------- | ---- | --------------------- |
| 1        | 12     | prop_id        | NUM  | Property ID           |
| 13       | 4      | tax_year       | NUM  | Tax year              |
| 17       | 12     | land_seg_id    | NUM  | Land segment ID       |
| 29       | 8      | land_type_cd   | CHAR | Land type code        |
| 37       | 25     | land_type_desc | CHAR | Land type description |
| 62       | 5      | state_cd       | CHAR | State code            |
| 67       | 1      | ag_flag        | CHAR | Agricultural flag     |
| 68       | 14     | land_sqft      | NUM  | Land square feet      |
| 82       | 14     | land_acres     | NUM  | Land acres            |
| 96       | 15     | mkt_val        | NUM  | Market value          |
| 111      | 15     | prod_val       | NUM  | Productivity value    |
| 126      | 5      | land_class     | CHAR | Land classification   |
| 131      | 10     | soil_cd        | CHAR | Soil code             |
| 141      | 15     | appraised_val  | NUM  | Appraised value       |
| 156      | 5      | ag_apply_cd    | CHAR | Ag application code   |
| 161      | 10     | adj_cd         | CHAR | Adjustment code       |

---

### 6. APPRAISAL_IMPROVEMENT_INFO

Improvement (building) summary records.

| Position | Length | Field Name        | Type | Description                  |
| -------- | ------ | ----------------- | ---- | ---------------------------- |
| 1        | 12     | prop_id           | NUM  | Property ID                  |
| 13       | 4      | tax_year          | NUM  | Tax year                     |
| 17       | 12     | impr_id           | NUM  | Improvement ID               |
| 29       | 10     | impr_type_cd      | CHAR | Improvement type code        |
| 39       | 25     | impr_type_desc    | CHAR | Improvement type description |
| 64       | 5      | state_cd          | CHAR | State code                   |
| 69       | 1      | homesite_flag     | CHAR | Homesite flag                |
| 70       | 10     | year_built        | NUM  | Year built                   |
| 80       | 15     | percent_complete  | NUM  | Percent complete             |
| 95       | 1      | depreciation_flag | CHAR | Depreciation flag            |
| 96       | 15     | appraised_val     | NUM  | Appraised value              |

---

### 7. APPRAISAL_IMPROVEMENT_DETAIL

Detailed improvement component records.

| Position | Length | Field Name     | Type | Description           |
| -------- | ------ | -------------- | ---- | --------------------- |
| 1        | 12     | prop_id        | NUM  | Property ID           |
| 13       | 4      | tax_year       | NUM  | Tax year              |
| 17       | 12     | impr_id        | NUM  | Improvement ID        |
| 29       | 12     | detail_id      | NUM  | Detail ID             |
| 41       | 10     | component_cd   | CHAR | Component code        |
| 51       | 30     | component_desc | CHAR | Component description |
| 81       | 10     | living_area    | NUM  | Living area sqft      |
| 91       | 15     | component_val  | NUM  | Component value       |

---

### 8. APPRAISAL_IMPROVEMENT_DETAIL_ATTR

Improvement attribute records.

| Position | Length | Field Name | Type | Description     |
| -------- | ------ | ---------- | ---- | --------------- |
| 1        | 12     | prop_id    | NUM  | Property ID     |
| 13       | 4      | tax_year   | NUM  | Tax year        |
| 17       | 12     | impr_id    | NUM  | Improvement ID  |
| 29       | 12     | detail_id  | NUM  | Detail ID       |
| 41       | 20     | attr_cd    | CHAR | Attribute code  |
| 61       | 50     | attr_val   | CHAR | Attribute value |

---

### 9. APPRAISAL_ABSTRACT_SUBDV

Abstract and subdivision reference codes.

| Position | Length | Field Name     | Type | Description               |
| -------- | ------ | -------------- | ---- | ------------------------- |
| 1        | 10     | abs_subdv_cd   | CHAR | Abstract/subdivision code |
| 11       | 40     | abs_subdv_desc | CHAR | Description               |

---

### 10. APPRAISAL_AGENT

Property agent/representative information.

| Position | Length | Field Name  | Type | Description          |
| -------- | ------ | ----------- | ---- | -------------------- |
| 1        | 12     | agent_id    | NUM  | Agent ID             |
| 13       | 70     | agent_name  | CHAR | Agent name           |
| 83       | 80     | agent_addr1 | CHAR | Agent address line 1 |
| 163      | 80     | agent_addr2 | CHAR | Agent address line 2 |
| 243      | 50     | agent_city  | CHAR | Agent city           |
| 293      | 2      | agent_state | CHAR | Agent state          |
| 295      | 10     | agent_zip   | CHAR | Agent ZIP            |
| 305      | 15     | agent_phone | CHAR | Agent phone          |

---

### 11. APPRAISAL_STATE_CODE

State classification codes reference.

| Position | Length | Field Name    | Type | Description            |
| -------- | ------ | ------------- | ---- | ---------------------- |
| 1        | 5      | state_cd      | CHAR | State code             |
| 6        | 50     | state_cd_desc | CHAR | State code description |

---

### 12. APPRAISAL_COUNTRY_CODE

Country codes reference.

| Position | Length | Field Name   | Type | Description  |
| -------- | ------ | ------------ | ---- | ------------ |
| 1        | 5      | country_cd   | CHAR | Country code |
| 6        | 50     | country_name | CHAR | Country name |

---

### 13. APPRAISAL_LAWSUIT

Lawsuit/protest information.

| Position | Length | Field Name   | Type | Description         |
| -------- | ------ | ------------ | ---- | ------------------- |
| 1        | 12     | prop_id      | NUM  | Property ID         |
| 13       | 4      | tax_year     | NUM  | Tax year            |
| 17       | 20     | lawsuit_cd   | CHAR | Lawsuit code        |
| 37       | 50     | lawsuit_desc | CHAR | Lawsuit description |
| 87       | 15     | protest_val  | NUM  | Protest value       |

---

### 14. APPRAISAL_MOBILE_HOME_INFO

Mobile home specific information.

| Position | Length | Field Name | Type | Description       |
| -------- | ------ | ---------- | ---- | ----------------- |
| 1        | 12     | prop_id    | NUM  | Property ID       |
| 13       | 4      | tax_year   | NUM  | Tax year          |
| 17       | 20     | mh_make    | CHAR | Mobile home make  |
| 37       | 20     | mh_model   | CHAR | Mobile home model |
| 57       | 20     | mh_serial  | CHAR | Serial number     |
| 77       | 4      | mh_year    | NUM  | Year              |
| 81       | 10     | mh_size    | CHAR | Size              |
| 91       | 20     | hud_label  | CHAR | HUD label         |

---

### 15. APPRAISAL_TAX_DEFERRAL_INFO

Tax deferral records.

| Position | Length | Field Name     | Type | Description     |
| -------- | ------ | -------------- | ---- | --------------- |
| 1        | 12     | prop_id        | NUM  | Property ID     |
| 13       | 4      | tax_year       | NUM  | Tax year        |
| 17       | 10     | deferral_cd    | CHAR | Deferral code   |
| 27       | 15     | deferred_amt   | NUM  | Deferred amount |
| 42       | 8      | effective_date | CHAR | Effective date  |

---

### 16. APPRAISAL_UDI

Undivided interest records.

| Position | Length | Field Name     | Type | Description        |
| -------- | ------ | -------------- | ---- | ------------------ |
| 1        | 12     | prop_id        | NUM  | Property ID        |
| 13       | 12     | parent_prop_id | NUM  | Parent property ID |
| 25       | 10     | udi_percent    | NUM  | UDI percentage     |
| 35       | 15     | udi_val        | NUM  | UDI value          |

---

### 17. APPRAISAL_ENTITY_TOTALS

Aggregate totals by taxing entity.

| Position | Length | Field Name      | Type | Description           |
| -------- | ------ | --------------- | ---- | --------------------- |
| 1        | 10     | entity_cd       | CHAR | Entity code           |
| 11       | 50     | entity_name     | CHAR | Entity name           |
| 61       | 15     | total_appraised | NUM  | Total appraised value |
| 76       | 15     | total_taxable   | NUM  | Total taxable value   |
| 91       | 10     | property_count  | NUM  | Property count        |

---

## Data Type Definitions

| Type | Description                                      |
| ---- | ------------------------------------------------ |
| CHAR | Character/text field, left-aligned, space-padded |
| NUM  | Numeric field, right-aligned, zero-padded        |

## Notes

1. All files are fixed-width format with no delimiters
2. Numeric fields are stored as strings and may need conversion
3. Date fields are typically in MMDDYYYY or YYYYMMDD format
4. Property ID (prop_id) is the primary key linking most tables
5. Text fields are space-padded to their full length

---

_Last Updated: December 2025_
_Source: Kaufman County CAD Export_
