# popVAT: Population Mapping using Variational Autoencoder with Transfer Learning

## 1. Introduction

This repository provides the implementation of **popVAT**, an extension of the **popVAE** framework for high-resolution population mapping.  
While popVAT uses the **same datasets as popVAE**, the **deep learning architecture and training strategy are modified** to improve prediction performance.

The overall workflow of the study and the geographical context of the research are illustrated in **Figure 1-a of popVAE**, which presents the methodological flowchart and the location of the study area (**Tunisia**).

The figure is provided in this repository.

**Study Area:** Tunisia  
**Reference Figure:** `Figure_1a_popVAE.png`

---

# 2. Dataset

This section explains how the dataset used in the study was assembled, pre-processed, and transformed.  
The full workflow is illustrated in **Figure 1 of popVAT** (provided in this repository).

The dataset consists of **population data** and several **ancillary datasets**.

---

# 2.1 Population Data

Four population datasets were used:

- WorldPop
- GPWv4
- LandScan
- INS (Institut National de la Statistique – Tunisia)

Original sources:

- WorldPop: https://www.worldpop.org/
- GPWv4: https://sedac.ciesin.columbia.edu/data/collection/gpw-v4
- LandScan: https://landscan.ornl.gov/
- INS: http://www.ins.tn/

Because some of these datasets require downloading **global rasters and extracting Tunisia**, we provide the ready-to-use files in the repository.

Folder:
