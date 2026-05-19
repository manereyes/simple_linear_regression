import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from model import LinearRegressionModel
###

# --- PAGE CONFIGURATION --- #
st.set_page_config(page_title="Salary Analytics Pro", layout="wide")

# --- DATA LOADING --- #
data_raw = pd.read_csv('../data/salaries.csv')
df = pd.DataFrame(data_raw)

# Model caching to avoid retraining on every interaction
@st.cache_resource
def get_model():
    return LinearRegressionModel(df['YearsExperience'], df['Salary'])


model = get_model()


# -- NAVIGATION --- #
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Salaries Calculator", "Analytics", "About Me"])

if page == 'Salaries Calculator':
    st.title("📊 Salary Predictions")
    st.write("Enter the years of experience to predict the salary: ")
    
    # Input for years of experience
    years_experience = st.sidebar.slider("Years of Experience", 1.1, 10.5, 5.0, 0.1)
    
    # Computation
    pe = model.predict(years_experience)
    ci_low, ci_high = model.get_confidence_interval(years_experience)
    pi_low, pi_high = model.get_prediction_interval(years_experience)
    
    # Metrics Visualization
    st.subheader("Predicted Salary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated Salary", f"${pe:,.0f}")
    c2.metric("Lower Confidence Interval", f"${ci_low:,.0f}")
    c3.metric("Upper Confidence Interval", f"${ci_high:,.0f}")
    
    st.divider()
    
    # Interactive Plot for Predictions
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.regplot(x='YearsExperience', y='Salary', data=df, ax=ax, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    ax.scatter(years_experience, pe, color='black', s=150, label='Your Prediction', zorder=5)
    ax.set_title("Position of the Prediction on the Regression Line")
    st.pyplot(fig)
elif page == 'Analytics':
    st.title("📈 Data Analytics")
    st.write("Explore the dataset and the regression model metrics.")
    
    # Dataset Exploration
    st.subheader("Dataset Overview")
    
    tab1, tab2, tab3 = st.tabs(["Dataset & ANOVA", "Residuals Analysis", "Correlation Matrix"])
    
    with tab1:
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.subheader("Original Dataset")
            st.dataframe(df, height=400)
        
        with col_b:
            st.subheader("ANOVA Table")
            # ANOVA calculations
            ssr = np.sum((model.scikit_model.predict(model.X_arr.reshape(-1, 1)) - model.Y_arr.mean())**2)
            sse = model.sse
            sst = ssr + sse
            msr = ssr / 1
            f_val = msr / model.MSE
            
            anova_df = pd.DataFrame({
                "Source": ["Regression", "Error (Residual)", "Total"],
                "DF": [1, model.n - 2, model.n - 1],
                "Sum of Squares": [f"{ssr:,.2f}", f"{sse:,.2f}", f"{sst:,.2f}"],
                "Mean Square": [f"{msr:,.2f}", f"{model.MSE:,.2f}", ""],
                "F": [f"{f_val:.4f}", "", ""]
            })
            st.table(anova_df)
            st.info(f"**Standard Error (S):** {model.S:.2f}")
    
    with tab2:
        st.subheader("Residual Analysis")
        c1, c2 = st.columns(2)
        
        with c1:
            # Residuals Grap
            fig2, ax2 = plt.subplots()
            ax2.scatter(df['YearsExperience'], model.residuals)
            ax2.axhline(0, color='red', linestyle='--')
            ax2.set_title("Residuals Graph (Independence Check)")
            ax2.set_xlabel("Years of Experience")
            ax2.set_ylabel("Residuals ($)")
            st.pyplot(fig2)
            
        with c2:
            # Gráfico de Probabilidad Normal
            res_sorted = np.sort(model.residuals)
            perc = np.arange(1, len(res_sorted) + 1) / len(res_sorted) * 100
            fig3, ax3 = plt.subplots()
            ax3.scatter(perc, res_sorted)
            ax3.set_title("Normal Probability Plot")
            ax3.set_xlabel("Percentile")
            ax3.set_ylabel("Residuals ($)")
            st.pyplot(fig3)
            
    with tab3:
        st.subheader("Correlation Matrix")
        fig4, ax4 = plt.subplots()
        sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", ax=ax4)
        st.pyplot(fig4)
    
elif page == 'About Me':
    st.title("👨‍💻 About Me")
    st.write("""
    Hi! I'm José Reyes, a data enthusiast with a passion for making complex concepts simple and accessible. 
    I created this app to help people understand linear regression and how it can be used to make predictions based on data.
    
    If you have any questions or feedback, feel free to reach out!
    
    - Email: manu.contact707@gmail.com
    - LinkedIn: [José's LinkedIn](https://www.linkedin.com/in/arkreyes/)
    """)
    