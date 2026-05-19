import streamlit as st
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import math

###

class SalaryModel:
    def __init__(self, data):
        self.df = data
        pass