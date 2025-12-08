-- Update ENTITY_INFO table to correct assessed_val values
-- The raw file data was parsed incorrectly due to wrong column positions
-- We need to apply the correction formula: (last_2_digits * 10000) + (remaining_digits / 100)
-- Example: 991200000000036 -> (36 * 10000) + (991200 / 100) = 369912

-- Create a backup of the original values (optional)
-- ALTER TABLE cad.appraisal_entity_info ADD COLUMN IF NOT EXISTS assessed_val_raw BIGINT;
-- UPDATE cad.appraisal_entity_info SET assessed_val_raw = assessed_val WHERE assessed_val_raw IS NULL;

-- Apply the correction formula to assessed_val
UPDATE cad.appraisal_entity_info
SET assessed_val = (
    ((assessed_val % 100) * 10000) + 
    (((assessed_val - (assessed_val % 100)) / 1000000000)::bigint / 100)
)::bigint
WHERE assessed_val IS NOT NULL 
  AND assessed_val > 0;

-- Verify the update with a sample
SELECT 
    prop_id,
    entity_cd,
    assessed_val,
    'Corrected' as status
FROM cad.appraisal_entity_info 
WHERE prop_id IN (207880, 207881, 207882, 197867)
ORDER BY prop_id, entity_cd
LIMIT 20;
