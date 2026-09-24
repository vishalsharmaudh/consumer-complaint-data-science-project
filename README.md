# Consumer Complaint Data Science Project

> End-to-end Data Science project covering data cleaning, EDA, SQL analysis, feature engineering, machine learning, evaluation, and deployment.

### 🚀 Live Demo

**[👉 Open the Live Demo](https://consumer-complaint-data-science-project-ijgasgqz89ywhyesxx6huw.streamlit.app/)**

### 💻 GitHub Repository

**[👉 View the Source Code](https://github.com/vishalsharmaudh/consumer-complaint-data-science-project)**

## 🎯 Project Motivation

The main motivation behind this project was to understand how consumer complaint data can be transformed from raw records into actionable insights and a machine learning prediction system.

Instead of focusing only on building a machine learning model, the project was designed as an end-to-end Data Science workflow:

**Data Auditing → Data Cleaning → EDA → SQL Analysis → Feature Engineering → Machine Learning → Evaluation → Deployment**

The objective was to understand the data, identify a meaningful prediction problem, build a reliable model, evaluate it using appropriate metrics, and finally deploy the model as a working application.

---

## 💼 Problem Statement

Consumer complaint data contains information about:

- Products and sub-products
- Complaint issues and sub-issues
- Companies
- Consumer locations
- Submission methods
- Complaint dates
- Company response outcomes
- Complaint narratives

The challenge was to determine whether this information could be used to predict the **company's response outcome** to a consumer complaint.

The project therefore focused on the following question:

> **Can historical consumer complaint data be used to predict the likely company response to a new consumer complaint?**

---

## 🎯 Target Selection

### Initial Target Consideration

During the early stage of the project, I initially considered `timely_response` as the prediction target.

The idea was to build a binary classification model that would predict whether a company would respond to a complaint on time.

However, Exploratory Data Analysis showed that approximately **98.8% of the complaints had a timely response**.

This created a highly imbalanced classification problem.

A simple model predicting the majority class could achieve approximately **98.8% accuracy**, without necessarily providing useful predictive value for the minority class.

This led to an important question:

> **If a model achieves very high accuracy simply by predicting the majority class, is that accuracy actually meaningful?**

Instead of proceeding with a potentially misleading target, I revisited the problem definition.

---

## 🔄 Final Target: `company_response_to_consumer`

After analyzing the available outcomes, I selected:

`company_response_to_consumer`

as the final machine learning target.

This target represents the outcome of the company's response to the consumer complaint.

The model predicts four response categories present in the final modeling dataset:

- `Closed with explanation`
- `Closed with monetary relief`
- `Closed with non-monetary relief`
- `Untimely response`

This target was selected because it provides a more meaningful multiclass prediction problem than the initially considered `timely_response` target.

It also introduced a realistic machine learning challenge: **class imbalance across response categories**.

Therefore, model evaluation was not based on accuracy alone.

Metrics such as:

- Macro F1
- Balanced Accuracy
- Precision
- Recall
- Confusion Matrix

were used to understand how well the model performed across different classes.

---

## 🛠️ What I Did

### 1. Data Auditing

I first inspected the raw dataset to understand:

- Dataset structure
- Data types
- Missing values
- Duplicate records
- Date columns
- Categorical variables
- Target distributions
- Potential data quality issues

---

### 2. Data Cleaning

The dataset was cleaned and validated before analysis and modeling.

The process included:

- Handling missing values
- Validating data types
- Converting date columns
- Checking inconsistencies
- Handling categorical values
- Removing unnecessary identifiers
- Validating the cleaned dataset

The goal was not simply to make the dataset look clean, but to make it **reliable and suitable for downstream analysis and machine learning**.

---

### 3. Exploratory Data Analysis

EDA was performed to understand the underlying complaint patterns.

I explored:

- Complaint distribution across products
- Sub-products and issues
- Company-level patterns
- Geographic patterns
- Complaint trends over time
- Submission methods
- Response outcomes
- Response time patterns
- Complaint narratives and tags
- Potential machine learning targets

One of the most important outcomes of EDA was identifying the limitation of `timely_response` as a prediction target.

This demonstrated that EDA was not only used for visualization, but also for **problem definition and target selection**.

---

### 4. SQL Analysis

SQL was used to perform additional business-oriented analysis on the cleaned complaint data.

The analysis covered areas such as:

- Data validation
- Complaint volume
- Product and issue analysis
- Company-level analysis
- Response outcomes
- Response time analysis
- Advanced analytical queries

This helped complement the Python-based analysis with database-oriented data analysis.

---

### 5. Feature Engineering

Features were engineered based on information that would be available at prediction time.

The final feature set included:

#### Date Features

- `received_year`
- `received_month`
- `received_dayofweek`
- `received_day`
- `received_quarter`
- `received_hour`

#### Narrative Features

The raw complaint narrative was not directly used as text input.

Instead, it was converted into simple engineered features:

- `narrative_present`
- `narrative_length`
- `narrative_word_count`

Therefore, the current model does **not perform semantic or NLP-based understanding of complaint text**.

#### Company Feature

Company information was transformed using:

**Frequency Encoding**

The frequency of each company was calculated from the training data and used as a numerical feature.

#### Categorical Features

Categorical variables were transformed using:

**One-Hot Encoding**

Unknown categories were handled using:

`handle_unknown="ignore"`

---

## 🔒 Leakage Prevention

An important part of the feature engineering process was preventing data leakage.

Features that could reveal the outcome directly or were not appropriate for prediction were excluded.

Examples include:

- `timely_response`
- `company_public_response`
- `date_sent_to_company`
- `complaint_id`

The train/test split was performed before learned transformations such as:

- Rare-category bucketing
- Company frequency encoding

This ensured that information from the test set was not used while learning preprocessing transformations.

---

## 🤖 Machine Learning

Multiple classification approaches were evaluated, including:

- Dummy Classifier
- Logistic Regression
- Random Forest
- HistGradientBoosting

Because the target classes were imbalanced, model selection was not based on accuracy alone.

The primary focus was on:

**Macro F1 and Balanced Accuracy**

The final selected model was:

**HistGradientBoostingClassifier**

The model achieved:

- **Accuracy:** 67.69%
- **Balanced Accuracy:** 83.09%
- **Macro F1:** 50.74%

The difference between training and test Macro F1 was relatively small, which provided an additional check against severe overfitting.

---

## 📊 Model Evaluation

The final model was evaluated using:

- Accuracy
- Balanced Accuracy
- Macro F1
- Precision
- Recall
- F1-score by class
- Confusion Matrix

The confusion matrix and class-level metrics were particularly important because the target was imbalanced.

For example, minority classes such as `Untimely response` were evaluated through precision and recall rather than relying only on overall accuracy.

This provided a more realistic view of model performance.

---

## 🚀 Deployment

After completing the modeling workflow, the trained model and preprocessing artifacts were saved and integrated into a Streamlit application.

The application allows a user to enter complaint information such as:

- Product
- Sub-product
- Issue
- Sub-issue
- Submission method
- State
- Company
- Date received
- Complaint narrative

The application then generates:

- Predicted company response
- Class probabilities
- Probability breakdown for each response category

The prediction logic is separated from the Streamlit interface so that the preprocessing and model inference can be reused independently.

---

## 💡 Key Learning

The most important learning from this project was that **model building should come after problem understanding**.

Initially, the focus was on predicting `timely_response`.

However, EDA showed that the target was highly imbalanced, which changed the direction of the machine learning problem.

This reinforced an important Data Science principle:

> **EDA is not just about creating charts. It can change the problem you decide to solve.**

The project therefore focused not only on achieving model performance, but on building a complete and explainable workflow from **raw data to a deployed machine learning application**.
