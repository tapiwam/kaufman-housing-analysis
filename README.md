# Kaufman CAD Property Appraisal Analysis

A comprehensive Python application for analyzing property appraisal data from Kaufman County Central Appraisal District (CAD). This project parses fixed-width text files, loads data into PostgreSQL, and provides tools for in-depth property analysis including ownership patterns, value distributions, and investor identification.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Data Source](#data-source)
- [Project Structure](#project-structure)
- [Detailed Setup](#detailed-setup)
- [Loading Data](#loading-data)
- [Analysis Examples](#analysis-examples)
- [Database Schema](#database-schema)
- [Data Dictionary](#data-dictionary)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Overview

This project provides tools to:

- **Parse** fixed-width text files from CAD data exports (complex format with 1,200+ character lines)
- **Load** property, land, improvement, and entity data into PostgreSQL
- **Analyze** ownership patterns, property values, and subdivision demographics
- **Export** results to CSV for further analysis or reporting

## Features

- ✅ **Automated Setup** - Single script to set up environment, database, and load data
- ✅ **Fixed-Width Parsing** - Handles complex CAD export format with proper encoding
- ✅ **Value Correction** - Applies formula to fix incorrectly parsed assessed values
- ✅ **Comprehensive Schema** - PostgreSQL schema with indexes and relationships
- ✅ **Analysis Notebooks** - Pre-built Jupyter notebooks for common analyses
- ✅ **SQL Examples** - Library of example queries for exploration
- ✅ **Docker Support** - Containerized PostgreSQL and pgAdmin for easy setup

## Quick Start

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Docker & Docker Compose** - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/tapiwam/kaufman-housing-analysis.git
cd kaufman-housing-analysis
```

2. **Download CAD data**

Download the latest data from [Kaufman CAD Public Info](https://kaufman-cad.org/public-info/):

- Direct link: [2025 Certified Full Roll Download](https://kaufman-cad.org/wp-content/uploads/2025/11/Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5.zip)
- Extract to project root (creates `Kaufman-CAD-2025-...` directory)

3. **Run automated setup**

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:

- Create Python virtual environment
- Install dependencies
- Start Docker containers (PostgreSQL + pgAdmin)
- Load all data into database (~5-10 minutes)

4. **Start analyzing**

```bash
source .venv/bin/activate
jupyter notebook
```

Open `analysis/gateway_parks_analysis.ipynb` to see a complete analysis example.

## Data Source

**Source:** Kaufman County Central Appraisal District  
**Website:** https://kaufman-cad.org/public-info/  
**Download:** https://kaufman-cad.org/wp-content/uploads/2025/11/Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5.zip

**Data Description:**

- **Format:** Fixed-width text files (TXT)
- **Tax Year:** 2025
- **Records:** ~200,000+ properties
- **Coverage:** All properties in Kaufman County, Texas
- **Update Frequency:** Annually with supplements

**Included Files:**

- `APPRAISAL_INFO.TXT` - Property ownership and addresses
- `APPRAISAL_ENTITY_INFO.TXT` - Property values by taxing entity
- `APPRAISAL_LAND_DETAIL.TXT` - Land parcel details
- `APPRAISAL_IMPROVEMENT_INFO.TXT` - Building/structure information
- `APPRAISAL_IMPROVEMENT_DETAIL.TXT` - Detailed building components
- And 10+ additional supporting files

See [Data Dictionary](docs/DATA_DICTIONARY.md) for complete field definitions.

## Project Structure

```
kaufman-housing-analysis/
├── .github/
│   └── copilot-instructions.md    # AI coding assistant guidelines
├── analysis/                       # Analysis notebooks
│   ├── gateway_parks_analysis.ipynb
│   ├── gateway_parks_analysis.csv    # Analysis output
│   └── gateway_parks_investors.csv   # Investor subset
├── app/                            # Main application code
│   ├── models/                     # Data models
│   │   └── layout.py              # File layout configuration
│   ├── services/                   # Business logic
│   │   ├── file_reader.py         # Fixed-width file parser
│   │   ├── database.py            # Database operations
│   │   └── loader.py              # Data loading orchestration
│   ├── utils/                      # Utilities
│   │   └── logging_config.py      # Logging setup
│   └── config.py                   # Configuration settings
├── config/                         # Configuration files
│   └── file_layouts.json          # File format definitions
├── docs/                           # Documentation
│   ├── DATA_DICTIONARY.md         # Complete data dictionary
│   └── data_layout.md             # Original layout documentation
├── scripts/                        # Utility scripts
│   ├── setup.sh                   # Automated setup script
│   └── load_data.py               # Data loading script
├── sql/                            # SQL scripts
│   ├── 001_create_schema.sql      # Database schema
│   └── examples/                   # Example queries
│       └── basic_queries.sql
├── Kaufman-CAD-2025-.../           # Data files (not in git)
├── OLD/                            # Archived/experimental files
├── docker-compose.yml              # Docker services config
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Detailed Setup

### Manual Setup (Alternative to script)

If you prefer manual setup or the automated script fails:

#### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Start Docker Services

```bash
docker-compose up -d
```

Wait for PostgreSQL to be ready:

```bash
docker logs kaufman_cad_db -f
# Look for: "database system is ready to accept connections"
```

#### 4. Verify Database Connection

```bash
docker exec kaufman_cad_db psql -U cad_user -d kaufman_cad -c "SELECT version();"
```

## Loading Data

### Using the Automated Script

```bash
source .venv/bin/activate
python scripts/load_data.py
```

This loads all tables in the correct order with progress indicators.

### Using Jupyter Notebook

Open `housing1.ipynb` and run cells sequentially to load data interactively.

### Expected Load Times

| Table                        | Records  | Time | Rate    |
| ---------------------------- | -------- | ---- | ------- |
| Reference Tables             | ~500     | <1s  | -       |
| appraisal_info               | ~207,000 | ~30s | 7,000/s |
| appraisal_entity_info        | ~511,000 | ~60s | 8,500/s |
| appraisal_land_detail        | ~230,000 | ~40s | 5,700/s |
| appraisal_improvement_info   | ~175,000 | ~30s | 5,800/s |
| appraisal_improvement_detail | ~610,000 | ~90s | 6,800/s |

**Total:** ~10-15 minutes for complete load

### Verifying Data

```sql
-- Check record counts
SELECT
    'appraisal_info' as table_name, COUNT(*) FROM cad.appraisal_info
UNION ALL
SELECT
    'appraisal_entity_info', COUNT(*) FROM cad.appraisal_entity_info
UNION ALL
SELECT
    'appraisal_land_detail', COUNT(*) FROM cad.appraisal_land_detail;
```

## Analysis Examples

### Gateway Parks Subdivision Analysis

Complete analysis notebook: `analysis/gateway_parks_analysis.ipynb`

**Features:**

- Identifies all 1,286 properties in Gateway Parks
- Classifies owner-occupied vs investor properties (68% vs 32%)
- Extracts detailed value breakdowns (land, improvements, homesite/non-homesite)
- Identifies largest investors and corporate ownership patterns
- Exports results to `analysis/gateway_parks_analysis.csv` and `analysis/gateway_parks_investors.csv`

**Key Finding:** 406 investor-owned properties (~32%), with top investor owning 67 properties

**Output Files:**

- `analysis/gateway_parks_analysis.csv` - Complete dataset with all properties
- `analysis/gateway_parks_investors.csv` - Investor properties only

### Custom Analysis Template

```python
import psycopg2
import pandas as pd

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="kaufman_cad",
    user="cad_user",
    password="cad_password"
)

# Query properties
query = """
SELECT
    i.prop_id,
    i.owner_name,
    i.situs_city,
    MAX(e.assessed_val) as appraised_value
FROM cad.appraisal_info i
LEFT JOIN cad.appraisal_entity_info e
    ON i.prop_id = e.prop_id
WHERE i.situs_city = 'FORNEY'
GROUP BY i.prop_id, i.owner_name, i.situs_city
"""

df = pd.read_sql(query, conn)
print(f"Found {len(df):,} properties in Forney")
print(f"Average value: ${df['appraised_value'].mean():,.0f}")
```

### SQL Analysis Examples

See `sql/examples/basic_queries.sql` for 15+ ready-to-use queries:

- Property counts by city
- Value distributions
- Subdivision searches
- Multi-property owners
- Recent construction
- Entity-specific valuations

## Database Schema

### Core Tables

**appraisal_info** - Main property records

```sql
prop_id (BIGINT)           -- Unique property identifier
owner_name (VARCHAR)       -- Property owner
mail_addr_line1 (VARCHAR)  -- Mailing address
situs_street (VARCHAR)     -- Property street address
situs_city (VARCHAR)       -- Property city
legal_desc (VARCHAR)       -- Legal description
prop_val_yr (INTEGER)      -- Tax year
```

**appraisal_entity_info** - Property values by taxing entity

```sql
prop_id (BIGINT)       -- Links to appraisal_info
entity_cd (VARCHAR)    -- Taxing entity code (CF=City, KC=County, etc.)
assessed_val (BIGINT)  -- Appraised value (corrected)
taxable_val (BIGINT)   -- Taxable value
exempt_val (BIGINT)    -- Exempt value
```

**appraisal_land_detail** - Land parcels

```sql
prop_id (BIGINT)
land_seg_id (BIGINT)
state_cd (VARCHAR)       -- State code (HS=Homesite)
land_acres (BIGINT)
appraised_val (BIGINT)
```

**appraisal_improvement_info** - Buildings/structures

```sql
prop_id (BIGINT)
impr_id (BIGINT)
homesite_flag (VARCHAR)  -- Y/N homesite indicator
year_built (INTEGER)     -- Often NULL in this dataset
appraised_val (BIGINT)
```

### Relationships

```
appraisal_info (1) ──< (N) appraisal_entity_info
appraisal_info (1) ──< (N) appraisal_land_detail
appraisal_info (1) ──< (N) appraisal_improvement_info
appraisal_improvement_info (1) ──< (N) appraisal_improvement_detail
```

## Data Dictionary

See [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for complete field definitions.

**Important Notes:**

1. **Assessed Value Correction**

   - The `assessed_val` field had a parsing error in the original file format
   - Correction formula applied: `(last_2_digits × 10,000) + (first_6_digits ÷ 100)`
   - Example: `991200000000036` → `$369,912`
   - See `app/services/file_reader.py` for implementation

2. **Year Built**

   - Field exists but is NULL for most properties in this dataset
   - Use improvement date fields if available

3. **Multiple Entity Values**
   - Properties have separate value records for each taxing jurisdiction
   - Use `MAX(assessed_val)` to get official appraised value

## Development

### Running Tests

```bash
source .venv/bin/activate
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Format code with:

```bash
black app/ scripts/
flake8 app/ scripts/
```

### Adding New Analyses

1. Create new notebook in `analysis/` directory
2. Follow structure in `analysis/gateway_parks_analysis.ipynb`
3. Include:
   - Purpose and methodology sections
   - Preliminary findings
   - Well-documented code cells
   - Results export

See `.github/copilot-instructions.md` for detailed standards.

## Troubleshooting

### Docker Services Won't Start

```bash
# Check if ports are in use
lsof -i :5432  # PostgreSQL
lsof -i :5050  # pgAdmin

# Reset Docker services
docker-compose down
docker-compose up -d
```

### Database Connection Errors

```bash
# Verify PostgreSQL is running
docker ps | grep kaufman_cad_db

# Check logs
docker logs kaufman_cad_db

# Test connection
docker exec kaufman_cad_db psql -U cad_user -d kaufman_cad -c "\dt cad.*"
```

### Data Loading Errors

**File not found:**

- Verify data directory name matches `Kaufman-CAD-2025-...`
- Check `app/config.py` for correct `DATA_DIR` path

**Encoding errors:**

- Files use `latin1` encoding (configured in `file_layouts.json`)
- Don't convert files to UTF-8

**Value errors:**

- Assessed values should be reasonable ($10K - $1M range)
- If seeing billions, value correction may not have applied
- Check `app/services/file_reader.py` parse_value() function

### pgAdmin Access

**URL:** http://localhost:5050  
**Email:** admin@admin.com  
**Password:** admin

**Add Server:**

- Host: postgres (container name)
- Port: 5432
- Database: kaufman_cad
- Username: cad_user
- Password: cad_password

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow code style guidelines
4. Add tests for new features
5. Submit pull request

## Acknowledgments

- **Kaufman County CAD** for providing public access to appraisal data
- **PostgreSQL** for robust data storage
- **Jupyter** for interactive analysis capabilities

## Contact

**Project Maintainer:** Tapiwa Maruni  
**Repository:** https://github.com/tapiwam/kaufman-housing-analysis

---

**Last Updated:** December 2025  
**Data Version:** 2025 Certified Roll (Supplement 5)
