# -*- coding: utf-8 -*-
"""house-price-predict.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hdxcjRqVbVSN815ToFqafMD-AuMiNn63
"""

# Importing necessary libraries for data manipulation, visualization, and statistical analysis
import pandas as pd  # Importing pandas for data manipulation
import matplotlib.pyplot as plt  # Importing matplotlib for data visualization
import seaborn as sns  # Importing seaborn for statistical data visualization

# Loading dataset from Excel file
dataset = pd.read_excel("HousePricePrediction.xlsx")

# Displaying the first 5 records of the dataset
print(dataset.head(5))

# Print the dimensions of the dataset (number of rows and columns)
print(dataset.shape)

# Generating descriptive statistics for the dataset
dataset_description = dataset.describe()
print(dataset_description)

# Identifying categorical variables in the dataset
obj = (dataset.dtypes == 'object')  # Boolean series to check if the datatype is 'object'
object_cols = list(obj[obj].index)  # Extracting column names where the datatype is 'object'
print("Categorical variables:", len(object_cols))  # Printing the count of categorical variables

# Identifying integer variables in the dataset
int_ = (dataset.dtypes == 'int')  # Boolean series to check if the datatype is 'int'
num_cols = list(int_[int_].index)  # Extracting column names where the datatype is 'int'
print("Integer variables:", len(num_cols))  # Printing the count of integer variables

# Identifying float variables in the dataset
fl = (dataset.dtypes == 'float')  # Boolean series to check if the datatype is 'float'
fl_cols = list(fl[fl].index)  # Extracting column names where the datatype is 'float'
print("Float variables:", len(fl_cols))  # Printing the count of float variables

unique_values = []

for col in object_cols:
  unique_values.append(dataset[col].unique().size)
plt.figure(figsize=(10,6))
plt.title('No. Unique values of Categorical Features')
plt.xticks(rotation=90)
sns.barplot(x=object_cols,y=unique_values)

# Custom color palette for bars
custom_palette = sns.color_palette('pastel')

# Custom figure size
plt.figure(figsize=(24, 36))

# Custom title
plt.suptitle('Distribution of Categorical Features', fontsize=24)

# Counter for subplot index
index = 1

# Loop through each categorical feature
for col in object_cols:
    # Get value counts for the current feature
    y = dataset[col].value_counts()

    # Create subplot
    plt.subplot(11, 4, index)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Custom bar plot with pastel colors
    sns.barplot(x=list(y.index), y=y, palette=custom_palette)

    # Increment subplot index
    index += 1

# Adjust layout
plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

# Show plot
plt.show()

# Dropping the 'Id' column from the dataset
dataset.drop(['Id'],  # Specify the column to drop
             axis=1,   # Specify to drop along columns (axis=1)
             inplace=True)  # Modifying the dataset in place

# Filling missing values in the 'SalePrice' column with the mean of the column
dataset['SalePrice'] = dataset['SalePrice'].fillna(dataset['SalePrice'].mean())

# Creating a new dataset by removing rows with any missing values
new_dataset = dataset.dropna()

# Checking for missing values in the new dataset
missing_values_count = new_dataset.isnull().sum()
print(missing_values_count)

# Importing OneHotEncoder from scikit-learn
from sklearn.preprocessing import OneHotEncoder

# Identifying categorical variables in the new dataset
s = (new_dataset.dtypes == 'object')  # Creating a boolean series to check if the datatype is 'object'
object_cols = list(s[s].index)  # Extracting column names where the datatype is 'object'
print("Categorical variables:")  # Printing a label for categorical variables
print(object_cols)  # Printing the names of categorical variables
print('No. of categorical features: ', len(object_cols))  # Printing the count of categorical features

# Initializing OneHotEncoder with sparse=False
OH_encoder = OneHotEncoder(sparse=False)

# Encoding categorical variables and creating a DataFrame
OH_cols = pd.DataFrame(OH_encoder.fit_transform(new_dataset[object_cols]))

# Setting index of OH_cols to match the index of new_dataset
OH_cols.index = new_dataset.index

# Naming columns of OH_cols manually
OH_cols.columns = OH_cols.columns.astype(str)

# Creating the final DataFrame by dropping original categorical columns and concatenating one-hot encoded columns
df_final = new_dataset.drop(object_cols, axis=1)  # Dropping original categorical columns
df_final = pd.concat([df_final, OH_cols], axis=1)  # Concatenating one-hot encoded columns

# Importing necessary libraries
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Separating features (X) and target variable (Y)
X = df_final.drop(['SalePrice'], axis=1)  # Features
Y = df_final['SalePrice']  # Target variable

# Splitting the dataset into training and validation sets
# Train size: 80%, Validation size: 20%
# Random state set for reproducibility
X_train, X_valid, Y_train, Y_valid = train_test_split(
    X, Y, train_size=0.8, test_size=0.2, random_state=0)

# Importing Support Vector Machine (SVM) related libraries
from sklearn import svm
from sklearn.svm import SVC

# Importing mean absolute percentage error metric
from sklearn.metrics import mean_absolute_percentage_error

# Initializing Support Vector Regression (SVR) model
model_SVR = svm.SVR()

# Fitting SVR model on the training data
model_SVR.fit(X_train, Y_train)

# Making predictions on the validation set
Y_pred = model_SVR.predict(X_valid)

# Calculating and printing mean absolute percentage error
print(mean_absolute_percentage_error(Y_valid, Y_pred))

# Importing Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor

# Initializing Random Forest Regressor model with 10 estimators
model_RFR = RandomForestRegressor(n_estimators=10)

# Fitting Random Forest Regressor model on the training data
model_RFR.fit(X_train, Y_train)

# Making predictions on the validation set
Y_pred = model_RFR.predict(X_valid)

# Calculating mean absolute percentage error
mean_absolute_percentage_error(Y_valid, Y_pred)

# Importing Linear Regression model
from sklearn.linear_model import LinearRegression

# Initializing Linear Regression model
model_LR = LinearRegression()

# Fitting Linear Regression model on the training data
model_LR.fit(X_train, Y_train)

# Making predictions on the validation set
Y_pred = model_LR.predict(X_valid)

# Printing mean absolute percentage error
print(mean_absolute_percentage_error(Y_valid, Y_pred))