-- Kaufman CAD Database Schema
-- Generated for 2025 Appraisal Data Export

-- Create schema
CREATE SCHEMA IF NOT EXISTS cad;

-- Set search path
SET search_path TO cad, public;

-- =====================================================
-- Reference Tables
-- =====================================================

-- Abstract/Subdivision codes
CREATE TABLE IF NOT EXISTS cad.appraisal_abstract_subdv (
    abs_subdv_cd VARCHAR(10) PRIMARY KEY,
    abs_subdv_desc VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- State classification codes
CREATE TABLE IF NOT EXISTS cad.appraisal_state_code (
    state_cd VARCHAR(5) PRIMARY KEY,
    state_cd_desc VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Country codes
CREATE TABLE IF NOT EXISTS cad.appraisal_country_code (
    country_cd VARCHAR(5) PRIMARY KEY,
    country_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent information
CREATE TABLE IF NOT EXISTS cad.appraisal_agent (
    agent_id BIGINT PRIMARY KEY,
    agent_name VARCHAR(70),
    agent_addr1 VARCHAR(80),
    agent_addr2 VARCHAR(80),
    agent_city VARCHAR(50),
    agent_state VARCHAR(2),
    agent_zip VARCHAR(10),
    agent_phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Header / Metadata
-- =====================================================

CREATE TABLE IF NOT EXISTS cad.appraisal_header (
    id SERIAL PRIMARY KEY,
    export_date VARCHAR(10),
    export_time VARCHAR(6),
    tax_year INTEGER,
    roll_description VARCHAR(30),
    supplement_number VARCHAR(10),
    record_count INTEGER,
    export_type VARCHAR(10),
    property_types VARCHAR(50),
    cad_name VARCHAR(50),
    exported_by VARCHAR(20),
    version_info VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Entity Tables
-- =====================================================

-- Taxing entity base info
CREATE TABLE IF NOT EXISTS cad.appraisal_entity (
    prop_id BIGINT PRIMARY KEY,
    entity_type VARCHAR(1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entity totals
CREATE TABLE IF NOT EXISTS cad.appraisal_entity_totals (
    entity_cd VARCHAR(10) PRIMARY KEY,
    entity_name VARCHAR(50),
    total_appraised BIGINT,
    total_taxable BIGINT,
    property_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Main Property Tables
-- =====================================================

-- Main property information (with mailing address for owner-occupancy analysis)
CREATE TABLE IF NOT EXISTS cad.appraisal_info (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT,
    prop_type_cd VARCHAR(1),
    prop_val_yr INTEGER,
    owner_id BIGINT,
    owner_name VARCHAR(70),
    confidential_flag VARCHAR(1),
    mail_addr_line1 VARCHAR(80),
    mail_addr_line2 VARCHAR(80),
    mail_city VARCHAR(50),
    mail_state VARCHAR(50),
    mail_country VARCHAR(20),
    mail_zip VARCHAR(10),
    situs_street VARCHAR(60),
    situs_city VARCHAR(30),
    situs_zip VARCHAR(10),
    legal_desc VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_appraisal_info_prop_id ON cad.appraisal_info(prop_id);
CREATE INDEX IF NOT EXISTS idx_appraisal_info_year ON cad.appraisal_info(prop_val_yr);
CREATE INDEX IF NOT EXISTS idx_appraisal_info_legal_desc ON cad.appraisal_info USING gin(to_tsvector('english', legal_desc));

-- Property-entity relationships
CREATE TABLE IF NOT EXISTS cad.appraisal_entity_info (
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    entity_id VARCHAR(5) NOT NULL,
    entity_cd VARCHAR(10),
    entity_name VARCHAR(50),
    taxable_val BIGINT,
    exempt_val BIGINT,
    freeze_val BIGINT,
    assessed_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prop_id, tax_year, entity_id)
);

-- =====================================================
-- Land Tables
-- =====================================================

CREATE TABLE IF NOT EXISTS cad.appraisal_land_detail (
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    land_seg_id BIGINT NOT NULL,
    land_type_cd VARCHAR(8),
    land_type_desc VARCHAR(25),
    state_cd VARCHAR(5),
    ag_flag VARCHAR(1),
    land_sqft BIGINT,
    land_acres BIGINT,
    mkt_val BIGINT,
    prod_val BIGINT,
    land_class VARCHAR(5),
    soil_cd VARCHAR(10),
    appraised_val BIGINT,
    ag_apply_cd VARCHAR(5),
    adj_cd VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prop_id, tax_year, land_seg_id)
);

-- =====================================================
-- Improvement Tables
-- =====================================================

-- Improvement summary
CREATE TABLE IF NOT EXISTS cad.appraisal_improvement_info (
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    impr_id BIGINT NOT NULL,
    impr_type_cd VARCHAR(10),
    impr_type_desc VARCHAR(25),
    state_cd VARCHAR(5),
    homesite_flag VARCHAR(1),
    year_built INTEGER,
    percent_complete DECIMAL(18, 6),
    depreciation_flag VARCHAR(1),
    appraised_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prop_id, tax_year, impr_id)
);

-- Improvement detail
CREATE TABLE IF NOT EXISTS cad.appraisal_improvement_detail (
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    impr_id BIGINT NOT NULL,
    detail_id BIGINT NOT NULL,
    component_cd VARCHAR(10),
    component_desc VARCHAR(30),
    living_area INTEGER,
    component_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prop_id, tax_year, impr_id, detail_id)
);

-- Improvement detail attributes
CREATE TABLE IF NOT EXISTS cad.appraisal_improvement_detail_attr (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    impr_id BIGINT NOT NULL,
    detail_id BIGINT NOT NULL,
    attr_cd VARCHAR(20),
    attr_val VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_impr_detail_attr_prop 
    ON cad.appraisal_improvement_detail_attr(prop_id, tax_year, impr_id, detail_id);

-- =====================================================
-- Supplementary Tables
-- =====================================================

-- Lawsuit information
CREATE TABLE IF NOT EXISTS cad.appraisal_lawsuit (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    lawsuit_cd VARCHAR(20),
    lawsuit_desc VARCHAR(50),
    protest_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lawsuit_prop ON cad.appraisal_lawsuit(prop_id, tax_year);

-- Mobile home information
CREATE TABLE IF NOT EXISTS cad.appraisal_mobile_home_info (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    mh_make VARCHAR(20),
    mh_model VARCHAR(20),
    mh_serial VARCHAR(20),
    mh_year INTEGER,
    mh_size VARCHAR(10),
    hud_label VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_mobile_home_prop ON cad.appraisal_mobile_home_info(prop_id, tax_year);

-- Tax deferral information
CREATE TABLE IF NOT EXISTS cad.appraisal_tax_deferral_info (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    deferral_cd VARCHAR(10),
    deferred_amt BIGINT,
    effective_date VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tax_deferral_prop ON cad.appraisal_tax_deferral_info(prop_id, tax_year);

-- Undivided interest
CREATE TABLE IF NOT EXISTS cad.appraisal_udi (
    id SERIAL PRIMARY KEY,
    prop_id BIGINT NOT NULL,
    parent_prop_id BIGINT,
    udi_percent DECIMAL(18, 6),
    udi_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_udi_prop ON cad.appraisal_udi(prop_id);

-- =====================================================
-- Indexes for Performance
-- =====================================================

-- Property info indexes
CREATE INDEX IF NOT EXISTS idx_info_owner ON cad.appraisal_info(owner_id);
CREATE INDEX IF NOT EXISTS idx_info_geo ON cad.appraisal_info(geo_id);
CREATE INDEX IF NOT EXISTS idx_info_abs_subdv ON cad.appraisal_info(abs_subdv_cd);
CREATE INDEX IF NOT EXISTS idx_info_neighborhood ON cad.appraisal_info(neighborhood_cd);
CREATE INDEX IF NOT EXISTS idx_info_situs_city ON cad.appraisal_info(situs_city);
CREATE INDEX IF NOT EXISTS idx_info_situs_zip ON cad.appraisal_info(situs_zip);

-- Entity info indexes
CREATE INDEX IF NOT EXISTS idx_entity_info_entity ON cad.appraisal_entity_info(entity_cd);

-- Land detail indexes
CREATE INDEX IF NOT EXISTS idx_land_state_cd ON cad.appraisal_land_detail(state_cd);
CREATE INDEX IF NOT EXISTS idx_land_type ON cad.appraisal_land_detail(land_type_cd);

-- Improvement indexes
CREATE INDEX IF NOT EXISTS idx_impr_info_type ON cad.appraisal_improvement_info(impr_type_cd);
CREATE INDEX IF NOT EXISTS idx_impr_info_year ON cad.appraisal_improvement_info(year_built);

-- =====================================================
-- Data Load Tracking
-- =====================================================

CREATE TABLE IF NOT EXISTS cad.data_load_log (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(100) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    records_loaded INTEGER,
    load_start TIMESTAMP,
    load_end TIMESTAMP,
    status VARCHAR(20),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA cad TO cad_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cad TO cad_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA cad TO cad_user;
