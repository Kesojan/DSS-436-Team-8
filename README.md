# ML-Driven House Customization for Maximum Profit Tool
Decision Support System for MSCI 436 (Team 8)

The main objective of the DSS is for realtors/sellers to analyze buyer's preferences to understand and identify the most attractive house features (ex. upgraded kitchen, garage type, pool area). This model will help them make informed decisions about potential renovations or improvements to increase the chances of attracting interested buyers and generating more offers or achieving a higher selling price.

**Files Description:**
- MSCI 436 ML Model.ipynb: Colab notebook file containing the data cleaning/analysis and model training 
- app.py : File contains the code to run Streamlit 
- logs.txt: File contains the log for Streamlit app
- out.csv: File contains the dataframe to be used for Streamlit

**Code Structure and Description:** 
1. Import packages required to train model
2. Load required data
3. Clean data (removing missing data, etc)
4. Fit a LR model (generate coeff.)
5. Model evaluation (MSE, MAE)
6. Streamlit (UI)
7. References for code

*Note: We used code from external sources which we've cited under references.*
