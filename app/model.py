import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import t
import math

###

class LinearRegressionModel:
    def __init__(self, X_arr, Y_arr):
        """
        Initializes the Regression Model with the historical trainning arrays.
        Computes metrics and coef. needed for every interval.

        Args:
            X_arr (List): Historical trainning array of the independent variable (X).
            Y_arr (List): Historical trainning array of the dependent variable (Y).
        """
        
        # Flattening numpy arrays
        self.X_arr = np.array(X_arr).flatten()
        self.Y_arr = np.array(Y_arr).flatten()
        self.n = self.X_arr.size
        
        # Reshaping X_arr for sklearn
        X_reshape = self.X_arr.reshape(-1, 1)
        
        # Tunning the model using sklearn's LinearRegression
        self.scikit_model = LinearRegression()
        self.scikit_model.fit(X_reshape, self.Y_arr)
        
        # Saving b0 and b1 for later use
        self.b1 = self.scikit_model.coef_[0] # Coefficient / Slope
        self.b0 = self.scikit_model.intercept_ # Intercept
        
        # Calculating residuals using sklearn's predict method
        # Passing X_reshape so sklearn calculates all historical predictions
        y_historical_prediction = self.scikit_model.predict(X_reshape)
        self.residuals = self.Y_arr - y_historical_prediction
        
        # Calculating MSE and S using the residuals
        ssr = np.sum(self.residuals**2)
        self.sse = np.sum(self.residuals**2)
        self.MSE = ssr / (self.n - 2)
        self.S = math.sqrt(self.MSE)
        
        # Saving X total variance for later use in confidence interval calculations
        self.sum_xi2_nxm2 = np.sum(self.X_arr**2) - self.n * (self.X_arr.mean()**2)
        
        # T critic value at 95% confidence level for n-2 degrees of freedom
        self.ta2 = t.isf(0.025, self.n - 2)
        
    def predict(self, x):
        """
        Predicts the value of Y for a given value of X using the linear regression model.
        
        Args:
            x (float): The value of X for which to predict Y.
        Returns:
            float: The predicted value of Y.
        """
        x_input = np.array([[x]])
        return self.scikit_model.predict(x_input)[0]
    
    def get_confidence_interval(self, x):
        """
        Calculates the confidence interval for the predicted value of Y at a given value of X.

        Args:
            x (float): The value of X for which to calculate the confidence interval.
        Returns:
            Tuple: A tuple containing the lower and upper bounds of the confidence interval.
        """
        pe = self.predict(x)
        margin = self.ta2 * self.S * math.sqrt(1 / self.n + (x - self.X_arr.mean())**2 / self.sum_xi2_nxm2)
        return pe - margin, pe + margin
    
    def get_prediction_interval(self, x):
        """
        Calculates the prediction interval for the predicted value of Y at a given value of X.
        
        Args:            
            x (float): The value of X for which to calculate the prediction interval.
        Returns:            
            Tuple: A tuple containing the lower and upper bounds of the prediction interval.
        """
        pe = self.predict(x)
        margin = self.ta2 * self.S * math.sqrt(1 + 1 / self.n + (x - self.X_arr.mean())**2 / self.sum_xi2_nxm2)
        return pe - margin, pe + margin