# Crime Data Reference - Gateway Parks Analysis

## Data Source

**Forney Police Department Transparency Portal**

- **URL:** https://forneypdtx-transparency.connect.socrata.com/
- **Platform:** Socrata Open Data Portal
- **Coverage:** Forney, Texas crime incidents
- **Update Frequency:** Regular updates from Forney PD

## Analysis Period

**Date Range Used:** November 1, 2025 - December 7, 2025

This represents the most recent crime data available at the time of analysis (December 2025).

## Heat Map Analysis

The crime heat map visualization from the Forney PD portal shows:

### Geographic Crime Concentration

**High-Crime Zone (Red/Orange areas):**

- Located in the **southeastern quadrant** of Gateway Parks subdivision
- Concentrated around the following streets:
  - **Arbor Drive/Court**
  - **Pueblo Drive**
  - **Everglades Drive**

**Lower-Crime Areas (Green/Yellow):**

- Northwestern section of Gateway Parks
- Streets including Cedar Crest, Ferguson, Pike areas
- More dispersed, lower-intensity incident patterns

### Crime Categories Included

Based on the portal URL parameters, the analysis includes:

- Category 1 incidents (codes 1-8, 10-18, 20-21, 23-25, 27, 29, 31-33, 35, 42, 46, 48-49, 51, 53-56, 58, 62-63, 65, 67-74, 76)
- Typical categories include:
  - Property crimes (burglary, theft, vandalism)
  - Violent crimes (assault, robbery)
  - Disturbances
  - Drug-related offenses
  - Other reported incidents

## Visualization Type

**Heat Map Display:**

- Intensity-based visualization showing crime concentration
- Red = Highest incident density
- Orange/Yellow = Moderate incident density
- Green = Lower incident density
- Overlays: Police beat boundaries, Police ORI jurisdictions

## Limitations

1. **Visual Analysis Only:**

   - No access to raw incident data export
   - Cannot provide exact incident counts per street
   - Crime categories not individually broken down in visual

2. **Time Window:**

   - Single month snapshot (Nov-Dec 2025)
   - Cannot show year-over-year trends
   - Does not capture historical crime rate changes

3. **Incident Reporting:**
   - Reflects reported crimes only (not unreported incidents)
   - May include in-progress investigations (status filter: Open)
   - Subject to police discretion in categorization

## Methodology for Gateway Analysis

The ownership correlation analysis uses this crime heat map to:

1. **Identify High-Crime Streets:**

   - Streets within red/orange zones: Arbor, Pueblo, Everglades
   - Based on visual density of incident markers

2. **Compare Ownership Patterns:**

   - Extract property data for identified high-crime streets
   - Calculate investor vs. owner-occupied percentages
   - Compare against other Gateway Parks streets

3. **Test Hypothesis:**
   - Evaluate if high-crime streets have higher investor property concentrations
   - Statistical significance testing (chi-square)
   - Control for property values and location factors

## Screenshot Reference

A screenshot of the crime heat map is included in the repository for reference:

- **File:** `docs/gateway_crime_heatmap.png` (to be added)
- **View:** Zoomed to Gateway Parks area
- **Date:** December 7, 2025 (most recent data available)

## How to Access the Portal

For real-time crime data:

1. Visit: https://forneypdtx-transparency.connect.socrata.com/
2. Navigate to the Dashboard view
3. Set date range and filters as needed
4. Use map controls to zoom to Gateway Parks area
5. Toggle between Heat Map, List, and other visualizations

## Data Accuracy Notes

- Crime data is provided by Forney Police Department
- Incidents are geolocated based on reported addresses
- Some incidents may be privacy-restricted and not displayed
- Location precision depends on address quality in police reports

## Contact for Detailed Data

For incident-level data or specific crime reports:

**Forney Police Department**

- Phone: (972) 564-7607
- Address: 101 E. Main St, Forney, TX 75126
- Public Records Requests: Available through city website

---

**Last Updated:** December 8, 2025  
**Analysis Context:** Gateway Parks Crime-Ownership Correlation Study
