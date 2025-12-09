# GitHub Copilot Instructions - Kaufman CAD Analysis Project

## Project Overview

This project analyzes property appraisal data from Kaufman County Central Appraisal District (CAD). The data is loaded from fixed-width text files into PostgreSQL for analysis using Python and Jupyter notebooks.

## Code Style and Standards

### Python Code

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for all functions, classes, and modules (Google style)
- Prefer pathlib.Path over string paths
- Use context managers (`with` statements) for file and database operations
- Log important operations using the configured logger

Example:

```python
from pathlib import Path
from typing import Dict, List, Optional

def process_records(file_path: Path, batch_size: int = 1000) -> Dict[str, int]:
    """Process records from a fixed-width file.

    Args:
        file_path: Path to the input file
        batch_size: Number of records to process at once

    Returns:
        Dictionary with processing statistics
    """
    pass
```

### SQL Queries

- Use explicit column names instead of `SELECT *` in production queries
- Always include table aliases for joins
- Format queries for readability with proper indentation
- Add comments explaining complex logic
- Use CTEs (WITH clauses) for complex multi-step queries

Example:

```sql
WITH property_values AS (
    SELECT
        i.prop_id,
        i.owner_name,
        MAX(e.assessed_val) as appraised_value
    FROM cad.appraisal_info i
    LEFT JOIN cad.appraisal_entity_info e
        ON i.prop_id = e.prop_id
    WHERE i.prop_val_yr = 2025
    GROUP BY i.prop_id, i.owner_name
)
SELECT * FROM property_values;
```

## Jupyter Notebook Standards

### Notebook Structure

Every analysis notebook should follow this structure:

1. **Title and Overview** (Markdown)

   - Clear, descriptive title
   - Location and tax year
   - Data source citation

2. **Purpose Section** (Markdown)

   - Why this analysis exists
   - Key questions being answered
   - Expected outputs

3. **Methodology Section** (Markdown)

   - How data is filtered/selected
   - Classification logic explained
   - Calculation formulas documented
   - Any assumptions clearly stated

4. **Preliminary Findings** (Markdown)

   - Key statistics discovered during exploration
   - Interesting patterns or anomalies
   - Context for what follows

5. **Setup Code** (Python)

   - Imports
   - Database connection
   - Path configuration
   - Always include success confirmation messages

6. **Analysis Sections** (Alternating Markdown/Python)

   - Each section with clear markdown header explaining what's happening
   - Code cells focused on single tasks
   - Output interpretation when relevant

7. **Results Export** (Python)
   - Save datasets to CSV
   - Print summary statistics
   - Confirm file locations

### Markdown Cell Guidelines

- Use proper heading hierarchy (`#`, `##`, `###`)
- Include **bold** for emphasis on key terms
- Use bullet lists for multiple points
- Add horizontal rules (`---`) to separate major sections
- Include context before code execution

Example:

```markdown
## Property Value Analysis

This section examines property values across the subdivision to identify:

- **Average and median values** - Understanding typical property worth
- **Value distributions** - Identifying clusters and outliers
- **Trends by location** - Geographic patterns in valuation

The values are sourced from the `appraisal_entity_info` table, which contains appraised values by taxing entity. We use the maximum value across entities as the official appraised value.
```

### Code Cell Guidelines

- Include comments explaining non-obvious logic
- Print informative messages showing progress
- Display sample data after major operations
- Use emoji markers for visual organization (✅ ❌ 📊 🏘️ 💰)
- Format large numbers with commas (`:,`)
- Round percentages to 1 decimal place

Example:

```python
print("📊 Analyzing property values...")

# Calculate statistics excluding zero values
valid_values = df[df['appraised_value'] > 0]['appraised_value']

print(f"\n💰 Value Statistics:")
print(f"  Count: {len(valid_values):,}")
print(f"  Average: ${valid_values.mean():,.0f}")
print(f"  Median: ${valid_values.median():,.0f}")
print(f"  Range: ${valid_values.min():,.0f} - ${valid_values.max():,.0f}")

print("\n✅ Analysis complete")
```

## Data-Specific Conventions

### Field Naming

- Use snake_case for database columns and Python variables
- Use descriptive names: `appraised_value` not `val`
- Prefix aggregations: `total_value`, `avg_price`, `max_assessment`

### Value Handling

- Always handle NULL values explicitly
- Use `COALESCE()` in SQL for default values
- Use `pd.notna()` or `.fillna()` in pandas
- Document the assessed_val correction formula when displaying raw values

### Occupancy Classification

When classifying owner occupancy:

```python
def determine_occupancy(row):
    """Classify property as owner-occupied or investor-owned.

    Logic: If mailing city matches property city, assume owner-occupied.
    Otherwise, assume investor/non-owner occupied.
    """
    mail_city = str(row['mail_city']).upper().strip() if pd.notna(row['mail_city']) else ""
    property_city = "FORNEY"  # or dynamic based on situs_city

    if not mail_city:
        return "Unknown"
    return "Owner-Occupied" if mail_city == property_city else "Investor/Non-Owner"
```

## Database Schema Knowledge

Key tables:

- `appraisal_info` - Main property records (owner, address, legal description)
- `appraisal_entity_info` - Property values by taxing entity
- `appraisal_land_detail` - Land parcel details
- `appraisal_improvement_info` - Building/structure information
- `appraisal_improvement_detail` - Detailed building components

Important notes:

- `assessed_val` in `entity_info` had a parsing correction applied (see app/services/file_reader.py)
- `year_built` in `improvement_info` is often NULL in this dataset
- Use `legal_desc` for subdivision matching (e.g., `LIKE '%GATEWAY PARK%'`)
- Properties may have multiple entity_info records (one per taxing jurisdiction)

## File Organization

- Analysis notebooks go in `analysis/` directory
- Utility scripts go in `scripts/` directory
- SQL examples go in `sql/examples/` directory
- Output CSV files go in project root (or `output/` if created)
- Keep data files in `Kaufman-CAD-*` directory (not tracked in git)

## Error Handling

- Always use try-except for database operations
- Log errors with context
- Provide user-friendly error messages
- Don't let the kernel die silently - catch and display errors

Example:

```python
try:
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    print(f"✅ Query successful: {len(results):,} results")
except psycopg2.Error as e:
    print(f"❌ Database error: {e}")
    logger.error(f"Query failed: {e}", exc_info=True)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    logger.error(f"Unexpected error in query execution: {e}", exc_info=True)
```

## Documentation

- Comment complex SQL queries inline
- Add docstrings to all Python functions
- Use markdown cells to explain analysis steps
- Document assumptions and limitations
- Credit data sources

## Testing and Validation

- Always verify data loads with record counts
- Spot-check values against known properties (e.g., prop_id 197867)
- Print sample data after transformations
- Cross-reference totals with source documentation when available

---

When generating code for this project, prioritize clarity, documentation, and user feedback through informative print statements. Every notebook should be understandable to someone unfamiliar with the data structure.
