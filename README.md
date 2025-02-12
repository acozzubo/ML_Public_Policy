# White Elephants Kill. Can we anticipate them with Machine Learning?

### Project for UChicago CAPP30254, Machine Learning for Public Policy (June 2020) with A.Bartra 
### Keywords: Public Expenditure, Machine Learning, Python

<img src="https://github.com/acozzubo/ML_Public_Policy/blob/master/images/welephants_img2.png" alt="drawing" height="350" width="1200"/>

## Overview
This repository contains the replication material for the project **"White Elephants Kill: Can we anticipate them with Machine Learning?"**, developed for the **CAPP-30254 course**. The project investigates how **machine learning techniques** can help identify early predictors of **unsuccessful large-scale public projects** ("white elephants").

### Project Team:
- **Angelo Cozzubo**
- **Andrei Bartra**

## Motivation
### Why Study Public Expenditures?
Governments worldwide invest billions in large-scale infrastructure and social projects. However, many projects **fail to deliver their intended benefits**, resulting in wasted resources and economic inefficiencies. Identifying **early warning signs** of such failures can significantly improve **public policy decisions** and resource allocation.

### Why Machine Learning?
Machine learning allows us to:
- Process large datasets efficiently.
- Identify complex patterns in public spending data.
- Improve prediction accuracy for project success/failure.

## Data Accessibility
**Note:** The datasets are **not included** in this repository due to size constraints. You can access the full dataset via GoogleDrive [link](https://drive.google.com/file/d/1PZPDA61DV7urmnkTIEdcpiToanFbXO4e/view?usp=sharing) 

### Data Sources:
- Government reports on public expenditures
- Administrative records and policy documents

## Methodology
### 1. Data Processing
- **Data Cleaning:** Handling missing values, standardizing formats.
- **Feature Engineering:** Creating meaningful variables from raw data.
- **ETL Pipeline:** Extracting, transforming, and loading data for analysis.

### 2. Machine Learning Models Used
- **Logistic Regression**
- **Random Forest Classifier**
- **Gradient Boosting Models (XGBoost, LightGBM)**

### 3. Evaluation Metrics
- Accuracy
- Precision-Recall F1 Score
- ROC-AUC Score
- Feature Importance Analysis

## Repository Structure
```
├── Data/            # Placeholder for datasets (instructions on how to download included)
├── Scripts/         # Contains data processing and ML analysis scripts
├── Results/         # Output files and visualizations
├── images/          # Visualizations and figures for README
├── README.md        # Project documentation
├── LICENSE          # MIT License
```

## How to Use This Repository
### Prerequisites
- **Python (>=3.8)**
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Analysis
1. Clone the repository:
   ```bash
   git clone https://github.com/acozzubo/ML_Public_Policy.git
   ```
2. Navigate to the scripts folder:
   ```bash
   cd ML_Public_Policy/Scripts
   ```
3. Run the main analysis scripts:
  **i) my_fns.py : the functions used for the descriptive analysis and preprocessing** 
  **ii) 200611_final_project.ipynb: the Jupyter Notebook with the code and outputs of the preprocessing and Machine Learning algorithms.**
  **iii) db_consolidation.py: the code used for the ETL process of the data.**
  **iv) varlists.py: contains the list of variables used for time operators.**
  
## Key Findings
- **Early Warning Signs:** Certain budgetary patterns correlate strongly with project failure.
- **Feature Importance:** Political factors and initial project mismanagement are strong predictors.
- **Model Performance:** Random Forest and XGBoost models performed best in identifying potential white elephants.

## Citation
If you use this repository, please cite:
```
Cozzubo, A. (2023). Predicting Public Project Failures Using Machine Learning.
CAPP-30254 Final Project.
```

## License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
We thank **Professor Nick Feamster** at UChicago CAPP, and all contributors for their support.

---







