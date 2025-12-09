# Kaufman County Housing Analysis

## Unlocking Insights from Public Property Data

Welcome to the **Kaufman County Housing Analysis Project**—an open-source initiative to make sense of the thousands of property records maintained by local appraisal districts in Texas.

---

## 🎯 What This Project Does

Kaufman County, part of the rapidly growing Dallas-Fort Worth metroplex, has seen explosive population growth over the past decade. With that growth comes questions:

- **Who owns our neighborhoods?** Are homes owned by residents or investors?
- **How are property values changing?** Where are values rising or falling?
- **What patterns exist in housing data?** Can we spot trends before they become problems?

This project takes raw property appraisal data—thousands of records in complex, fixed-width text files—and transforms it into actionable insights.

---

## 📊 Current Research

### Featured: Gateway Parks Crime & Rental Analysis

<div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 1rem; margin: 1rem 0;">

**[Read the Full Report →](GATEWAY_PARKS_CRIME_RENTAL_ANALYSIS.md)**

An investigation into whether investor-owned rental properties are driving crime in a Forney subdivision—as residents claim.

**Key Findings:**
- 🏠 **76.5%** of Pueblo Drive homes are investor-owned (vs. 28% average)
- 📍 **13 streets** identified with abnormally high rental rates (>40%)
- 🏢 Institutional investors from **GA, AZ, CA, NV** identified
- ⚖️ **Nuanced verdict**: Some correlation on specific streets, but not a blanket explanation

</div>

---

## 📁 Data & Resources

### Analysis Files

| Resource | Description |
|----------|-------------|
| [**Gateway Parks Analysis Notebook**](analysis/gateway_parks_crime_ownership_analysis.ipynb) | Full Jupyter notebook with code |
| [**Data Dictionary**](DATA_DICTIONARY.md) | Field definitions for CAD data |
| [**Data Layout Reference**](data_layout.md) | Technical specs for data files |

### Raw Data (CSV Downloads)

> **Note:** Click "Raw" on GitHub to download CSV files, or use the direct links below.

| Dataset | Records | Description |
|---------|---------|-------------|
| [Street Ownership Statistics](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_ownership_by_street.csv) | ~70 streets | Investor % by street |
| [High-Crime Street Properties](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_high_crime_streets_properties.csv) | ~170 properties | Properties on flagged streets |
| [Full Gateway Parks Dataset](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_parks_full_analysis.csv) | 1,200+ properties | Complete classified dataset |

---

## 🔍 Data Sources

### Kaufman County Central Appraisal District (CAD)

The primary data source is the **2025 Certified Full Roll** from Kaufman CAD, which includes:

- Property ownership records
- Situs (physical) addresses
- Mailing addresses
- Legal descriptions
- Appraised and assessed values
- Land and improvement details

**Download:** [Kaufman CAD Public Data](https://www.kaufman-cad.org/)

### Forney Police Department

Crime data and heat maps are sourced from:

- **Forney PD Transparency Portal**: [forneypdtx-transparency.connect.socrata.com](https://forneypdtx-transparency.connect.socrata.com/)

---

## 🛠️ Technical Overview

This project uses:

- **Python 3.9+** — Data processing and analysis
- **PostgreSQL 16** — Database storage
- **Jupyter Notebooks** — Interactive analysis
- **Pandas** — Data manipulation
- **Docker** — Database containerization

### Repository Structure

```
kaufman-housing-analysis/
├── docs/                    # GitHub Pages site (you are here)
│   ├── analysis/            # Notebooks and CSV exports
│   └── *.md                 # Documentation
├── app/                     # Python application code
├── config/                  # Data layout configurations
├── scripts/                 # Data loading scripts
└── sql/                     # Database schema
```

**[View Full Repository →](https://github.com/tapiwam/kaufman-housing-analysis)**

---

## 🚀 Getting Started

Want to run your own analysis? See the [main README](https://github.com/tapiwam/kaufman-housing-analysis#readme) for setup instructions.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/tapiwam/kaufman-housing-analysis.git

# Start the database
docker compose up -d

# Load the data
python scripts/load_data.py

# Open analysis notebooks
jupyter notebook
```

---

## 📬 About

This project is maintained as an open-source research initiative. The goal is to make public property data more accessible and useful for residents, researchers, and policymakers.

**Data Sources:** Kaufman County CAD, Forney PD  
**Analysis Period:** December 2025  
**License:** MIT

---

*Property ownership data is public record. This analysis is for informational purposes and does not imply wrongdoing by any individual property owner.*
