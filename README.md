# Consumer Complaint Analysis & Response Prediction

An end-to-end Data Science project focused on analyzing consumer complaints, identifying patterns in complaint data, performing SQL-based business analysis, and building a Machine Learning model to predict the likely company response to a complaint.

The project covers the complete workflow from raw data auditing and cleaning to exploratory analysis, feature engineering, model evaluation, and deployment through a Streamlit application.

---

## 📌 Project Overview

Consumer complaint datasets contain valuable information about customer issues, financial products, companies, complaint channels, response outcomes, and response behavior.

The goal of this project is to understand these patterns and build a Machine Learning workflow that can predict the likely `company_response_to_consumer` category for a new complaint.

The project combines:

- Python
- Pandas
- NumPy
- SQL
- Scikit-learn
- Power BI
- Streamlit
- Git/GitHub

---

## 🎯 Business Problem

Financial consumer complaints can vary significantly by:

- Product
- Sub-product
- Issue
- Company
- State
- Submission method
- Time period
- Company response

The project addresses two main objectives:

### 1. Business Analysis

Analyze complaint data to understand:

- Complaint volume
- Product and issue patterns
- Company-level patterns
- Geographic distribution
- Response outcomes
- Response trends
- Complaint characteristics

### 2. Machine Learning

Build a multiclass classification model to predict:

`company_response_to_consumer`

for a new complaint based on information available at prediction time.

---

## 📊 Dataset

The processed dataset contains approximately **90,000 consumer complaints**.

The project uses complaint-level information including:

- Product
- Sub-product
- Issue
- Sub-issue
- State
- Company
- Submission method
- Date received
- Complaint narrative
- Company response

The final modeling dataset contains **90,112 records**.

---

# 🔎 Project Workflow

```text
Raw Data
   ↓
Data Auditing
   ↓
Data Cleaning
   ↓
Exploratory Data Analysis
   ↓
SQL Business Analysis
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Prediction Pipeline
   ↓
Streamlit Application