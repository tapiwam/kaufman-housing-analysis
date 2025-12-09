# Gateway Parks: Crime and Rental Property Analysis

## A Data-Driven Investigation into Forney's Growing Neighborhood Concerns

**December 2025 | Kaufman County, Texas**

---

## Executive Summary

Residents of Gateway Parks, a residential subdivision in Forney, Texas, have grown increasingly vocal about rising crime in their neighborhood. Many point to the same culprit: **rental properties owned by out-of-town investors**.

This analysis dives deep into public property records to answer a simple question: **Is there a connection between high investor ownership and crime in Gateway Parks?**

### The Short Answer

**Yes—but it's complicated.**

My investigation found that **Pueblo Drive**, a street with concentrated crime activity in November 2025, has an astounding **76.5% investor ownership rate**. That's more than 3 out of every 4 homes owned by someone who doesn't live there. But other streets flagged for crime issues have the _opposite_ profile—they're mostly owner-occupied but adjacent to some of the problem areas.

The data tells a nuanced story: rental concentration _can_ correlate with crime on specific streets, but as with any analysis blaming all neighborhood problems on rentals is an oversimplification, but I hope this helps.

---

## Background: What's Happening in Gateway Parks?

Gateway Parks is a suburban subdivision in Forney, Texas, about 25 miles east of Dallas. Developed in the mid-2000s, the neighborhood has grown alongside the booming DFW metroplex. But with that growth has come change—and concern.

### Community Complaints

In November 2025, local news stations reported on rising tensions in the neighborhood:

> **"Forney neighbors fight new development amid rise in crime"**  
> — NBC DFW, November 2025

Residents told reporters that investor-owned rental homes were driving up crime rates. The Forney City Council even **denied a new development phase** by Ashton Woods builders, citing community concerns. Streets like **Pueblo Drive**, **Everglades Drive**, and **Lawnview Drive** were specifically mentioned as problem areas.

### The Crime Data

According to the **Forney Police Department's Transparency Portal**, crime heat maps for November-December 2025 show:

- **Concentrated activity** in the southeastern section of Gateway Parks
- **Hot spots** appearing near Pueblo Drive and surrounding streets
- Incident types including property crimes, disturbances, and calls for service

---

## My Research Approach

### Data Sources

| Source                            | Description                                                                                                |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Kaufman County CAD**            | 2025 Certified Property Appraisal Roll—includes property ownership, mailing addresses, and assessed values |
| **Forney PD Transparency Portal** | Crime incident heat maps and call data                                                                     |
| **Local News Reports**            | NBC DFW, WFAA coverage of Gateway Parks concerns                                                           |

### Methodology

I used property appraisal data from Kaufman County Central Appraisal District to classify every home in Gateway Parks as either:

1. **Owner-Occupied** — The owner's mailing address is in Forney (they live in the home)
2. **Investor/Non-Owner Occupied** — The owner's mailing address is elsewhere (they don't live in the home)

This classification isn't perfect—some owners use PO boxes, and some investors use local addresses—but it provides a reliable approximation for large-scale analysis.

**Technical Note:** This analysis was conducted using Python and PostgreSQL, with AI assistance to help parse and interpret the county's complex fixed-width data files. The full methodology and code are available in the accompanying Jupyter notebooks.

---

## Key Findings

### Finding #1: Nearly 1 in 3 Gateway Parks Homes is Investor-Owned

After excluding builder-owned inventory (Ashton Woods, K Hovnanian), I found:

| Metric                          | Count | Percentage |
| ------------------------------- | ----- | ---------- |
| **Total Properties Analyzed**   | 1,208 | 100%       |
| **Owner-Occupied**              | 869   | **71.9%**  |
| **Investor/Non-Owner Occupied** | 339   | **28.1%**  |

This 28% investor rate is notable—it's higher than the national average of about 20% for single-family rentals.

---

### Finding #2: 13 Streets Have "Abnormally High" Investor Rates (>40%)

I identified 13 streets where non-owner-occupied properties exceed 40%—well above the neighborhood average:

| Street           | Total Homes | Investor % | Median Home Value | High Crime?  |
| ---------------- | ----------- | ---------- | ----------------- | ------------ |
| **Pueblo**       | 34          | **76.5%**  | $321,534          | 🔴 YES       |
| **McCree**       | 47          | **70.2%**  | $328,299          | —            |
| **Sandlin**      | 41          | **70.7%**  | $324,160          | —            |
| **Purtis Creek** | 53          | **64.2%**  | $324,145          | —            |
| **Lockhart**     | 55          | **60.0%**  | $167,251          | —            |
| Honey Creek      | 18          | 83.3%      | $321,979          | —            |
| Bushman          | 11          | 81.8%      | $75,000           | Builder lots |
| Bachman          | 5           | 100.0%     | $75,000           | Builder lots |
| Watercrest       | 9           | 66.7%      | $10               | Land parcels |
| Browder          | 8           | 50.0%      | $280,674          | —            |
| Parkdale         | 16          | 50.0%      | $75,000           | —            |
| Ferguson         | 11          | 45.5%      | $346,669          | —            |

**Note:** Some high-percentage streets (Bachman, Bushman, Watercrest) are builder inventory or undeveloped lots, not traditional rentals.

---

### Finding #3: Pueblo Drive—The "Smoking Gun"

**Pueblo Drive stands out as the clearest example of the rental-crime connection.**

| Pueblo Drive Statistics |                                       |
| ----------------------- | ------------------------------------- |
| Total Properties        | 34                                    |
| Owner-Occupied          | 8 (23.5%)                             |
| Investor-Owned          | **26 (76.5%)**                        |
| Median Home Value       | $321,534                              |
| Crime Status            | 🔴 High activity zone per PD heat map |

More than **three-quarters** of homes on Pueblo Drive are owned by investors who live elsewhere. This is nearly **3x the neighborhood average**.

#### Who Owns Pueblo Drive?

Sample investors include:

| Owner                      | Location          |
| -------------------------- | ----------------- |
| PRNL Residential Buyer LLC | Scottsdale, AZ    |
| Hoque Investments LLC      | Richardson, TX    |
| AM7 Reality LLC            | Garland, TX       |
| 1829 Pueblo Street Trust   | San Francisco, CA |
| Palani Jothi Rev Trust     | Argyle, TX        |

The street is a mix of **institutional investors** (LLCs based in Arizona, California) and **individual landlords** from across the DFW metro.

---

### Finding #4: Not All "Problem Streets" Are Rental-Heavy

Here's where the story gets interesting. **Lawnview Drive** was specifically mentioned in news reports as a crime concern—but the data tells a different story:

| Street     | Investor % | Crime Reports        |
| ---------- | ---------- | -------------------- |
| Pueblo     | **76.5%**  | 🔴 High              |
| Lawnview   | **7.9%**   | 🔴 Mentioned in news |
| Everglades | **25.7%**  | 🔴 Mentioned in news |

**Lawnview has one of the LOWEST investor rates in the entire subdivision** (7.9%)—well below the 28% neighborhood average. If rentals were the only driver of crime, Lawnview should be one of the safest streets. It's not.

This suggests that **factors other than rental status** contribute to crime on some streets—potentially traffic patterns, lighting, location near entrances/exits, or isolated problem households.

---

### Finding #5: Where Do the Investors Come From?

I tracked the mailing addresses of investor-owned properties across the highest-concentration streets:

| City               | Properties | Region                                  |
| ------------------ | ---------- | --------------------------------------- |
| **Allen, TX**      | 14         | DFW Metro                               |
| **Frisco, TX**     | 11         | DFW Metro                               |
| **Plano, TX**      | 9          | DFW Metro                               |
| **Marietta, GA**   | 8          | Atlanta (single institutional investor) |
| **Irving, TX**     | 8          | DFW Metro                               |
| **Scottsdale, AZ** | 6          | Phoenix Metro                           |
| **Prosper, TX**    | 6          | DFW Metro                               |
| **Houston, TX**    | 5          | Houston                                 |
| **Las Vegas, NV**  | 3          | Out of state                            |
| **Chantilly, VA**  | 3          | Washington DC area                      |
| **Dublin, CA**     | 3          | San Francisco Bay Area                  |

**Key insight:** Most investors are **local to the DFW area** (Allen, Frisco, Plano), but significant out-of-state capital flows in from Georgia, Arizona, California, Nevada, and Virginia.

#### Institutional Investors of Note

One investor stands out: **IDF1 SFR PROPCO A LLC**, based in Marietta, Georgia, owns **8+ properties on Sandlin Street alone**. This appears to be a large institutional single-family rental (SFR) operator.

Other notable LLCs include:

- **PRNL Residential Buyer LLC** (Scottsdale, AZ)
- **Landmark Capital Realty LLC** (Plano, TX)
- **Hoque Investments LLC** (Richardson, TX)
- **Hussain Family Estates 25 LLC** (Plano, TX)
- **Fortune Grove Realty LLC** (Plano, TX)

---

## The Verdict: Is Crime Caused by Rentals?

### ✅ For Pueblo Drive: PROBABLY YES (Strong Correlation)

The evidence is compelling:

- **76.5% investor ownership**—the highest in the neighborhood
- Located in a **crime hot spot** per police data
- Heavy presence of **out-of-state and institutional investors**

The combination of absentee ownership, high tenant turnover, and potentially less rigorous tenant screening creates conditions where problems can concentrate.

### 🔶 The Bigger Picture: It's Complicated

Blaming all of Gateway Parks' crime on rentals is **too simple**. The data shows:

1. **Some streets** (like Pueblo) have a clear rental-crime correlation
2. **Other streets** have some crime despite being mostly owner-occupied
3. **High investor %** alone doesn't guarantee crime problems

A nuanced approach is needed—one that targets specific problem areas. Further investigation into other factors (lighting, traffic, policing patterns) is warranted.

---

## Data & Code Availability

All analysis is reproducible and available in this repository:

| Resource | Description |
|----------|-------------|
| [**Full Analysis Notebook**](analysis/gateway_parks_crime_ownership_analysis.ipynb) | Complete Jupyter notebook with code and methodology |
| [**Street Statistics CSV**](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_ownership_by_street.csv) | Ownership statistics for every street |
| [**High-Crime Properties CSV**](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_high_crime_streets_properties.csv) | Property-level data for flagged streets |
| [**Full Dataset CSV**](https://raw.githubusercontent.com/tapiwam/kaufman-housing-analysis/main/docs/analysis/gateway_parks_full_analysis.csv) | Complete property dataset with classifications |

> **Tip:** Click the CSV links to download directly, or view them on GitHub by replacing `raw.githubusercontent.com` with `github.com` and removing `/main`.

---

## Sources

### Property Data

- **Kaufman County Central Appraisal District** — 2025 Certified Full Roll Download (updated with Supplement 5)
- Data includes: Property ID, owner name, situs address, mailing address, legal description, appraised values

### Crime Data

- **Forney Police Department Transparency Portal** — [forneypdtx-transparency.connect.socrata.com](https://forneypdtx-transparency.connect.socrata.com/)
- Crime heat maps and incident data for November-December 2025

### News Reports

- **NBC DFW** (November 2025) — "Forney neighbors fight new development amid rise in crime"
- **WFAA** — Coverage of Gateway Parks resident concerns

### Technical Acknowledgment

This analysis utilized AI assistance (GitHub Copilot / Claude) to help:

- Parse fixed-width county data files
- Develop ownership classification methodology
- Generate statistical summaries and visualizations

All conclusions and interpretations are based on public data and represent the author's analysis.

---

## About This Analysis

**Completed:** December 2025  
**Location:** Gateway Parks Subdivision, Forney, Texas (Kaufman County)  
**Data Year:** 2025 Certified Appraisal Roll  
**Author:** Property data analysis based on public appraisal and police records

---

_This research is provided for informational purposes only. Property ownership status does not imply involvement in criminal activity. Individual investors and landlords should not be prejudged based on aggregate statistics._
