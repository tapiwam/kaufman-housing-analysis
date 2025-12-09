-- Basic Query Examples for Kaufman CAD Database
-- These queries help you explore and understand the property appraisal data

-- ========================================
-- 1. BASIC PROPERTY INFORMATION
-- ========================================

-- Sample property records with owner and address information
SELECT 
    prop_id,
    owner_name,
    situs_street,
    situs_city,
    situs_zip,
    mail_city,
    prop_val_yr
FROM cad.appraisal_info
LIMIT 10;

-- ========================================
-- 2. ENTITY INFORMATION
-- ========================================

-- View taxing entities (jurisdictions that can tax properties)
SELECT *
FROM cad.appraisal_entity
LIMIT 10;

-- ========================================
-- 3. PROPERTY VALUES BY ENTITY
-- ========================================

-- See how a property is valued by different taxing entities
SELECT *
FROM cad.appraisal_entity_info
LIMIT 10;

-- ========================================
-- 4. AGGREGATE ENTITY TOTALS
-- ========================================

-- Summary of total appraised and taxable values by entity
SELECT *
FROM cad.appraisal_entity_totals
LIMIT 10;

-- ========================================
-- 5. IMPROVEMENT (BUILDING) INFORMATION
-- ========================================

-- View building/structure information for properties
SELECT *
FROM cad.appraisal_improvement_info
LIMIT 10;

-- ========================================
-- 6. DETAILED IMPROVEMENT COMPONENTS
-- ========================================

-- Detailed breakdown of building components (rooms, features, etc.)
SELECT *
FROM cad.appraisal_improvement_detail
LIMIT 10;

-- ========================================
-- 7. IMPROVEMENT ATTRIBUTES
-- ========================================

-- Specific attributes of improvements (quality, condition, etc.)
SELECT *
FROM cad.appraisal_improvement_detail_attr
LIMIT 10;

-- ========================================
-- 8. SUBDIVISION/ABSTRACT INFORMATION
-- ========================================

-- View subdivision and abstract information
SELECT *
FROM cad.appraisal_abstract_subdv
LIMIT 100;

-- ========================================
-- 9. JOIN EXAMPLE: Property with Improvements
-- ========================================

-- Combine property info with improvement data
SELECT 
    a.prop_id,
    a.owner_name,
    a.situs_street,
    a.situs_city,
    b.impr_type_desc,
    b.year_built,
    b.appraised_val
FROM cad.appraisal_info a
LEFT JOIN cad.appraisal_improvement_info b 
    ON a.prop_id = b.prop_id
WHERE a.prop_id = 10;

-- ========================================
-- 10. PROPERTY VALUE SUMMARY
-- ========================================

-- Get comprehensive value information for a specific property
SELECT 
    i.prop_id,
    i.owner_name,
    i.situs_street || ', ' || i.situs_city as property_address,
    i.legal_desc,
    MAX(e.assessed_val) as appraised_value,
    SUM(imp.appraised_val) as total_improvement_value,
    SUM(l.appraised_val) as total_land_value
FROM cad.appraisal_info i
LEFT JOIN cad.appraisal_entity_info e 
    ON i.prop_id = e.prop_id AND i.prop_val_yr = e.tax_year
LEFT JOIN cad.appraisal_improvement_info imp
    ON i.prop_id = imp.prop_id AND i.prop_val_yr = imp.tax_year
LEFT JOIN cad.appraisal_land_detail l
    ON i.prop_id = l.prop_id AND i.prop_val_yr = l.tax_year
WHERE i.prop_id = 197867
GROUP BY i.prop_id, i.owner_name, i.situs_street, i.situs_city, i.legal_desc;

-- ========================================
-- 11. PROPERTIES BY CITY
-- ========================================

-- Count properties in each city
SELECT 
    situs_city,
    COUNT(*) as property_count,
    AVG(NULLIF(
        (SELECT MAX(assessed_val) 
         FROM cad.appraisal_entity_info e 
         WHERE e.prop_id = i.prop_id), 0
    )) as avg_appraised_value
FROM cad.appraisal_info i
WHERE situs_city IS NOT NULL AND situs_city != ''
GROUP BY situs_city
ORDER BY property_count DESC
LIMIT 15;

-- ========================================
-- 12. FIND PROPERTIES IN A SUBDIVISION
-- ========================================

-- Search for properties by legal description (e.g., subdivision name)
SELECT 
    prop_id,
    owner_name,
    situs_street,
    situs_city,
    legal_desc
FROM cad.appraisal_info
WHERE UPPER(legal_desc) LIKE '%GATEWAY PARK%'
ORDER BY situs_street
LIMIT 20;

-- ========================================
-- 13. PROPERTY OWNERSHIP ANALYSIS
-- ========================================

-- Find owners with multiple properties
SELECT 
    owner_name,
    COUNT(*) as property_count,
    STRING_AGG(DISTINCT situs_city, ', ') as cities
FROM cad.appraisal_info
WHERE owner_name IS NOT NULL
GROUP BY owner_name
HAVING COUNT(*) > 1
ORDER BY property_count DESC
LIMIT 20;

-- ========================================
-- 14. VALUE RANGES
-- ========================================

-- Analyze distribution of property values
SELECT 
    CASE 
        WHEN assessed_val < 100000 THEN 'Under $100K'
        WHEN assessed_val < 200000 THEN '$100K - $200K'
        WHEN assessed_val < 300000 THEN '$200K - $300K'
        WHEN assessed_val < 500000 THEN '$300K - $500K'
        ELSE '$500K+'
    END as value_range,
    COUNT(*) as property_count
FROM cad.appraisal_entity_info
WHERE assessed_val > 0
GROUP BY value_range
ORDER BY MIN(assessed_val);

-- ========================================
-- 15. RECENT CONSTRUCTION
-- ========================================

-- Find recently built properties
SELECT 
    i.prop_id,
    i.owner_name,
    i.situs_street,
    i.situs_city,
    imp.year_built,
    imp.impr_type_desc
FROM cad.appraisal_info i
JOIN cad.appraisal_improvement_info imp
    ON i.prop_id = imp.prop_id
WHERE imp.year_built >= 2020
ORDER BY imp.year_built DESC, i.situs_street
LIMIT 50;
