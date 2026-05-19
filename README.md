# 📊 Salary Analytics Pro - Interactive Regression Dashboard

This project consists of an interactive application developed in **Streamlit** that implements a **Simple Linear Regression** model to predict salaries based on years of experience. The mathematical and statistical core is developed using the **Object-Oriented Programming (OOP)** paradigm and integrates **Scikit-Learn** for model training and optimization.

Unlike traditional calculators, this system not only provides a point estimate, but also calculates **confidence intervals** (for market averages) and **prediction intervals** (for individual cases), backed by rigorous validation of statistical assumptions.

---

## 🚀 Key Features

* **Decoupled Architecture (OOP):** Complete separation between the mathematical logic (`model.py`) and the graphical interface (`app.py`).
* **Estimates with Uncertainty:** Dynamic calculation of intervals using the *t-Student* distribution.
* **Integrated Research Section:** A tab dedicated to model auditing that includes:
    * Viewing the historical dataset.
    * Generating the **ANOVA table** in real time.
    * Assessing homoscedasticity using residual plots.
    * Testing for normality using a **normal probability plot** based on sample percentiles.

---

## 🛠️ Technologies Used

* **Python 3.12+**
* **Streamlit** (UI/UX Design)
* **Scikit-Learn** (Linear model fitting)
* **SciPy & Math** (Statistical distributions and confidence interval calculation)
* **Pandas & NumPy** (Data manipulation and structuring)
* **Matplotlib & Seaborn** (Rendering statistical graphs)

---

## 📂 Project Architecture

```text
SIMPLE_REGRESSION/
│
├── app/
│   ├── app.py             # Streamlit user interface and navigation layout
│   └── model.py           # LinearRegressionModel OOP class (Statistical engine)
│
├── data/
│   └── data.txt           # txt to download the clean data
│
│
├── investigation/
│   └── linear_regression.ipynb  # Initial exploratory data analysis and model training
│
├── .gitignore             # Specifies intentionally untracked files to ignore
└── README.md              # Project documentation and setup guide