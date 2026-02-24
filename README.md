# EU Housing Herding (CSAD)
### Dispersion-Based Evidence from European Union Housing Markets (2015–2025)

This repository contains the reproducible empirical pipeline supporting the research paper:

> **Herding Behaviour in European Union Housing Markets: Evidence from the Post-Crisis Regulatory Period (2015–2025)**  
> Zahreddine Bouslama

---

##  Research Objective

This project investigates whether European Union housing markets exhibit behavioural convergence (herding) during the post-crisis regulatory period.

Using harmonised Eurostat House Price Index (HPI) data for 26 EU member states, we test whether cross-country return dispersion declines nonlinearly during periods of strong aggregate housing market movements.

The methodology follows the Cross-Sectional Absolute Deviation (CSAD) framework of:

- Christie & Huang (1995)
- Chang, Cheng & Khorana (2000)

---

## Methodological Framework

Quarterly log returns are computed as:

Rᵢₜ = ln(HPIᵢₜ) − ln(HPIᵢₜ₋₁)

Aggregate EU return:

Rₘₜ = (1/N) Σ Rᵢₜ

Cross-sectional dispersion (CSAD):

CSADₜ = (1/N) Σ |Rᵢₜ − Rₘₜ|

Regression specification:

CSADₜ = α + β₁|Rₘₜ| + β₂Rₘₜ² + εₜ

Evidence of herding requires:

β₂ < 0  (nonlinear dispersion compression)

---

## Repository Structure


eu-hpi-herding-csad/
│
├── data/
│ ├── raw/ # Original Eurostat CSV download
│ └── processed/ # Cleaned and return-computed data
│
├── src/
│ ├── 01_download_data.py
│ ├── 02_compute_csad.py
│ └── 03_regression.py
│
├── outputs/
│ ├── tables/
│ └── figures/
│
├── requirements.txt
└── README.md


---

## Reproducibility

###  Install dependencies

```bash
pip install -r requirements.txt
Run full pipeline
python src/01_download_data.py
python src/02_compute_csad.py
python src/03_regression.py

Outputs include:

Processed CSAD time series

HAC-robust regression tables

Regression diagnostics

 Key Finding

The nonlinear dispersion coefficient (β₂) is not statistically negative, indicating no evidence of supranational housing market herding during 2015–2025.

Cross-country dispersion remains structurally persistent despite aggregate market movements.

Contribution

This project extends dispersion-based herding tests to:

Illiquid residential housing markets

Harmonised cross-country EU data

Post-crisis macroprudential regime

It contributes to behavioural real estate finance and European housing integration research.

Technical Stack

Python 3.10+

pandas

numpy

statsmodels (HAC robust estimation)

Eurostat API

Citation

If you use this code or methodology, please cite:

Bouslama, Z. (2026). Herding Behaviour in European Union Housing Markets: Evidence from the Post-Crisis Regulatory Period (2015–2025). Working Paper.

 Contact

Dr. Zahreddine Bouslama
Behavioural Real Estate Finance (Europe)

