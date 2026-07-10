# KPFM_processing
Processing for Kelvin Probe Force Microscopy time series and further image analysis

When using this code please cite the following: arXiv:2607.07221



## Notebook Overview

| File Name | Description |
| --- | --- |
| **`CPDGrainBoundaryAnalysis - IndividualScatter.ipynb`** | Extracts and plots the contact potential difference delta ($\Delta$CPD) between grain boundaries and interiors across varying mask widths using automated single-Gaussian fitting. |
| **`LineByLineTimeSeriesProcessing.ipynb`** | Extracts time-resolved surface photovoltage kinetics by fitting Gaussian curves row-by-row across raw binary (`.npy`) KPFM images. |
| **`SPVGrainBoundaryAnalysis.ipynb`** | Automates batch potential shift analyses across passivated and unpassivated samples to generate localized diagnostic reports and multi-dataset summary plots. |
| **`GBGIvsWholeImages.ipynb`** | Generates comparative overlay diagrams comparing the distinct electrical potential distributions of grain boundaries, grain interiors, and whole-image control data. |
| **`TimeSeriesProcessing_BCK_Main.ipynb`** | Tracks long-term chronological potential shifts and distribution spreads using multi-Gaussian profiling and exponential saturation modeling. |
| **`SpreadAnalysis.ipynb`** | Fits full-image CPD distribution histograms to Gaussian curves to visually compare and evaluate potential spreads across different sample processing conditions. |

---

## Getting Started

> **Note on GUI Prompts:** Most of these notebooks utilize Tkinter pop-up windows for file and folder selection. If the notebook appears to be hanging during execution, check your background windows as the file dialog may have opened underneath your browser.

> **Note on data inputs:** Ensure all data is input as .txt until further updates for .npy inputs are provided. 
