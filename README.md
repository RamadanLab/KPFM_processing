# KPFM_processing
Processing for Kelvin Probe Force Microscopy time series and further image analysis

When using this code please cite the following: arXiv:2607.07221



## Notebook Overview

| File Name | Description |
| --- | --- |
| **`CPDGrainBoundaryAnalysis - IndividualScatter.ipynb`** | Extracts and plots the contact potential difference delta ($\Delta$CPD) between grain boundaries and interiors across varying mask widths using automated single-Gaussian fitting. |
| **`SPVGrainBoundaryAnalysis.ipynb`** | For grain mask analysis of SPV and CPD before, with and post-illumination. |
| **`GBGIvsWholeImages.ipynb`** | Generates plots to compare distributions of grain boundaries, grain interiors, and whole-image. |
| **`TimeSeriesProcessing_Main.ipynb`** | For long or short term time series with exponential fitting and full time series plotting. |
| **`SpreadAnalysis.ipynb`** | Fits single image distributions with Gaussian fitting to extract fit peak and FWHM. |

---

## Getting Started

> **Note on GUI Prompts:** Most of these notebooks utilize Tkinter pop-up windows for file and folder selection. If the notebook appears to be hanging during execution, check your background windows as the file dialog may have opened underneath your browser.

> **Note on data inputs:** Ensure all data is input as .txt until further updates for .npy inputs are provided. 
