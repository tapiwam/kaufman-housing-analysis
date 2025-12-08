-- Fix Primary Key for appraisal_entity_info
-- The original PK (prop_id, tax_year, entity_id) is invalid because entity_id is always 00000.
-- We will switch to (prop_id, tax_year, entity_cd).

DROP TABLE IF EXISTS cad.appraisal_entity_info CASCADE;

CREATE TABLE cad.appraisal_entity_info (
    prop_id BIGINT NOT NULL,
    tax_year INTEGER NOT NULL,
    entity_id VARCHAR(5),
    entity_cd VARCHAR(10) NOT NULL,
    entity_name VARCHAR(50),
    taxable_val BIGINT,
    exempt_val BIGINT,
    freeze_val BIGINT,
    assessed_val BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (prop_id, tax_year, entity_cd)
);

-- Recreate index on prop_id for performance
CREATE INDEX idx_entity_info_prop_id ON cad.appraisal_entity_info(prop_id);
