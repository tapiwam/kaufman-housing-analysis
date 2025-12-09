# Kaufman CAD Data Loader

A Python application to parse and load Kaufman County Central Appraisal District (CAD) property appraisal data from fixed-width text files into a PostgreSQL database.

## Overview

This project provides tools to:

- Parse fixed-width text files from CAD data exports
- Load data into a PostgreSQL database
- Query and analyze property appraisal data

## Project Structure

```
housing1/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── layout.py            # File layout configuration models
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── file_reader.py       # Fixed-width file parser
│   │   ├── database.py          # Database operations
│   │   └── loader.py            # Data loading orchestration
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── logging_config.py    # Logging setup
├── config/                       # Configuration files
│   └── file_layouts.json        # File layout definitions
├── docs/                         # Documentation
│   └── data_layout.md           # Data layout documentation
├── sql/                          # SQL scripts
│   └── 001_create_schema.sql    # Database schema creation
├── Kaufman-CAD-2025-.../         # Data files directory
├── docker-compose.yml            # Docker services configuration
├── requirements.txt              # Python dependencies
├── housing1.ipynb               # Testing/prototyping notebook
└── README.md                    # This file
```

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- pip (Python package manager)

## Quick Start

### 1. Start the Database

```bash
# Start PostgreSQL and pgAdmin containers
docker-compose up -d

# Verify containers are running
docker-compose ps
```

Database will be available at:

- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050` (admin@admin.com / admin)

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database Schema

The schema is automatically created when the container starts, or you can run it manually:

```python
from app.services.database import DatabaseService

db = DatabaseService()
db.execute_sql_file("sql/001_create_schema.sql")
```

### 4. Load Data

Using the notebook:

```bash
jupyter notebook housing1.ipynb
```

Or programmatically:

```python
from app.services.loader import DataLoader

loader = DataLoader()

# Load all files
results = loader.load_all_files()

# Or load specific files
results = loader.load_file("ABSTRACT_SUBDV")
```

## Configuration

### Database Settings

Edit `app/config.py` or use environment variables:

| Variable    | Default      | Description       |
| ----------- | ------------ | ----------------- |
| DB_HOST     | localhost    | Database host     |
| DB_PORT     | 5432         | Database port     |
| DB_NAME     | kaufman_cad  | Database name     |
| DB_USER     | cad_user     | Database user     |
| DB_PASSWORD | cad_password | Database password |

### File Layouts

File layouts are defined in `config/file_layouts.json`. Each file type specifies:

- Column positions and lengths
- Data types
- Table mapping

## Data Files

The following CAD export files are supported:

| File                    | Description                | Records |
| ----------------------- | -------------------------- | ------- |
| HEADER                  | Export metadata            | 1       |
| INFO                    | Main property data         | ~104K   |
| ENTITY                  | Taxing entity codes        | 65      |
| ENTITY_INFO             | Property-entity links      | ~511K   |
| LAND_DETAIL             | Land segments              | ~103K   |
| IMPROVEMENT_INFO        | Building summary           | ~102K   |
| IMPROVEMENT_DETAIL      | Building details           | ~348K   |
| IMPROVEMENT_DETAIL_ATTR | Building attributes        | ~409K   |
| ABSTRACT_SUBDV          | Abstract/subdivision codes | ~2.5K   |
| AGENT                   | Agent information          | ~1K     |
| And more...             |                            |         |

## Usage Examples

### Read and Parse Files

```python
from app.models.layout import load_layout_config
from app.services.file_reader import read_all_records, get_file_path
from app.config import DATA_DIR, CONFIG_DIR

# Load configuration
config = load_layout_config(CONFIG_DIR / "file_layouts.json")

# Get file configuration
file_config = config.get_file_config("INFO")

# Read records
file_path = get_file_path(DATA_DIR, config.filePrefix, "INFO")
records = read_all_records(file_path, file_config, max_records=100)

# Convert to DataFrame
import pandas as pd
df = pd.DataFrame(records)
```

### Load to Database

```python
from app.services.loader import DataLoader

loader = DataLoader()

# Load single file
result = loader.load_file("ABSTRACT_SUBDV")
print(f"Loaded {result['records_loaded']} records")

# Load all files
results = loader.load_all_files()
summary = loader.get_load_summary(results)
print(f"Total records: {summary['total_records']}")
```

### Query Database

```python
import pandas as pd
from app.config import DATABASE_CONFIG

conn_string = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Query properties
df = pd.read_sql("""
    SELECT prop_id, owner_name, situs_street, appraised_val
    FROM cad.appraisal_info
    WHERE appraised_val > 500000
    LIMIT 100
""", conn_string)
```

## Database Schema

The database uses the `cad` schema with tables matching each file type:

- `cad.appraisal_info` - Main property records
- `cad.appraisal_entity_info` - Property-entity relationships
- `cad.appraisal_land_detail` - Land segment details
- `cad.appraisal_improvement_info` - Improvement summaries
- `cad.appraisal_improvement_detail` - Improvement details
- And more...

See `docs/data_layout.md` for complete field definitions.

## Development

### Running Tests

Use the notebook `housing1.ipynb` for interactive testing and prototyping.

### Adding New File Types

1. Add file configuration to `config/file_layouts.json`
2. Add corresponding table to `sql/001_create_schema.sql`
3. Test with the notebook

### Logging

Logging is configured in `app/utils/logging_config.py`. Set the level via:

```python
from app.utils.logging_config import setup_logger
logger = setup_logger("cad_loader", level="DEBUG")
```

## Troubleshooting

### Database Connection Failed

```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart containers
docker-compose restart
```

### File Not Found

Ensure data files are in the correct directory with the expected prefix:
`Kaufman-CAD-2025-.../2025-10-27_002174_APPRAISAL_*.TXT`

### Parse Errors

Check the file layout configuration in `config/file_layouts.json` matches the actual file structure.

### INFO File Layout Notes

The APPRAISAL_INFO file has a complex 9,263-character fixed-width layout. The documented layout from the PDF may not match actual field positions. Key verified positions:

| Field        | Start | Length | Description            |
| ------------ | ----- | ------ | ---------------------- |
| prop_id      | 0     | 12     | Property ID            |
| prop_type_cd | 12    | 1      | Property type (R=Real) |
| prop_val_yr  | 18    | 4      | Tax year (2025)        |
| owner_id     | 596   | 12     | Owner ID               |
| owner_name   | 608   | 70     | Owner name             |
| situs_street | 745   | 40     | Property address       |
| situs_city   | 873   | 30     | Property city          |
| situs_zip    | 978   | 10     | Property ZIP           |
| legal_desc   | 1145  | 150    | Legal description      |

Note: Positions 13-17 and 22-595 contain filler/additional data not currently parsed.

## License

For internal use only. Data is property of Kaufman County CAD.

---

_Last Updated: December 2025_
