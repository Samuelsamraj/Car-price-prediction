# -*- coding: utf-8 -*-
"""Car price prediction(cleaning _ EDA ) .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XKoAt5WT2v8Lmic1cvMh22uUk8cn7WBn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import re

df1 = pd.read_excel('/content/bangalore_cars.xlsx')
df2 = pd.read_excel('/content/chennai_cars.xlsx')
df3 = pd.read_excel('/content/delhi_cars.xlsx')
df4 = pd.read_excel('/content/hyderabad_cars.xlsx')
df5 = pd.read_excel('/content/jaipur_cars.xlsx')
df6 = pd.read_excel('/content/kolkata_cars.xlsx')

df1['place'] = 'bangalore'

df1

df2['place'] = 'chennai'

df2

df3['place'] = 'delhi'

df3

df4['place'] = 'hyderabad'

df4

df5['place'] = 'jaipur'

df5

df6['place'] = 'kolkata'

df6

# Concatenate the dataframes into one
combined_df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)

combined_df.head()

combined_df.tail()

combined_df.shape

combined_df.new_car_detail[0]

new_car_detail = pd.DataFrame(combined_df.new_car_detail.apply(eval).tolist())
new_car_detail['place'] = combined_df.place.to_list()
new_car_detail

new_car_detail.drop(['it','ownerNo','centralVariantId','priceActual','priceSaving','priceFixedText','trendingText'],axis = 1,inplace = True)

new_car_detail.km = new_car_detail.km.apply(lambda x : x.replace(",","")).astype(float)

new_car_detail.head()

new_car_detail.owner = new_car_detail.owner.apply(lambda owner: int(re.findall(r'\d+',owner)[0]))
new_car_detail.head()

print("Unique oem present >>>>>>>>>\n\n",sorted(new_car_detail.oem.unique()))
print("\nTotal No of Unique oem >>>>>>",new_car_detail.oem.nunique())
print("\nTotal No of Model >>>>>>>",new_car_detail.model.nunique())
print("\nUnique modelYear >>>>>>>>\n\n",sorted(new_car_detail.modelYear.unique()))

price_colvalues = new_car_detail.price.str.replace("₹","").str.strip().to_list() #replacing rupee sign to empty string

#to find the denominators
text = []
for PriceString in price_colvalues:

    try:
        if (PriceString.split()[1]).isalpha(): #splitting prices "8.11 Lakh" by spaces
            text.append(PriceString.split()[1])
    except:
        pass

print("price denominations >>>>>>>>>>> ",set(text))

CroreCarsFrame = new_car_detail[new_car_detail.price.str.contains('Crore')]

# print("Crores Valued Cars Model >>>>>>\n",CroreCarsFrame.model.tolist())
# print("\nCrores Valued Cars Model Year >>>>>>\n",CroreCarsFrame.modelYear.tolist())
# print("\nCrores Valued Cars Model Price >>>>>>\n",CroreCarsFrame.price.tolist())

CroreCarsFrame.loc[:,['place','km','model','modelYear','price']].sort_values(by = 'km').reset_index(drop=True)

lakhCarsFrame = new_car_detail[new_car_detail.price.str.contains('Lakh')]

# print("Crores Valued Cars Model >>>>>>\n",CroreCarsFrame.model.tolist())
# print("\nCrores Valued Cars Model Year >>>>>>\n",CroreCarsFrame.modelYear.tolist())
# print("\nCrores Valued Cars Model Price >>>>>>\n",CroreCarsFrame.price.tolist())

lakhCarsFrame.loc[:,['place','km','model','modelYear','price']].sort_values(by = 'km').reset_index(drop=True)

"""# *new_car_overview*

"""

combined_df.new_car_overview

def to_get_overview(data):
    return {value['key'] : value['value'] for value in data}

combined_df.new_car_overview =combined_df.new_car_overview.apply(lambda x: to_get_overview(eval(x).get('top')))
new_car_overview = pd.DataFrame(combined_df.new_car_overview.tolist())

new_car_overview.head()

def to_get_features(data):
    extract = {'Features': [],
               "Comfort": [],
               "Interior":[],
               "Exterior": []
               }

    for features in data['top']:
        extract['Features'].append(features['value'])
    try:
        for comfort in data['data'][0]['list']:
            extract['Comfort'].append(comfort['value'])
    except:
        extract['Comfort'].append('Not-Specified')


    try:
        for interior in data['data'][1]['list']:
            extract['Interior'].append(interior['value'])
    except:
        extract['Interior'].append('Not-Specified')

    try:
        for exterior in data['data'][2]['list']:
            extract['Exterior'].append(exterior['value'])
    except:
        extract['Exterior'].append(None)
    # print(extract)
    return extract

combined_df.new_car_feature = combined_df.new_car_feature.apply(lambda x: to_get_features(eval(x)))
new_car_feature =pd.DataFrame(combined_df.new_car_feature.tolist())
new_car_feature

pd.set_option('display.max_columns', 500)

final_data =pd.concat([new_car_detail, new_car_overview, new_car_feature], axis=1)
final_data.head()

final_data.isna().sum()

final_data.info()

for i in final_data.columns:
    # print(i)
    if i not in ['Features','Comfort', 'Interior', 'Exterior', 'trendingText']:
        print(i, final_data[i].nunique())

final_data.isna().sum()

import pandas as pd

# Assuming 'Registration Year' is the column name
final_data['Registration Year'] = final_data['Registration Year'].str.extract(r'(\d{4})')

# Print the updated column
print(final_data['Registration Year'])

final_data['Registration Year'].value_counts()

final_data.drop(columns=['Registration Year'], inplace=True)

final_data['Insurance Validity'].value_counts()

final_data['Insurance Validity'].fillna(final_data['Insurance Validity'].mode()[0], inplace=True)

final_data.Seats.value_counts()

final_data['Seats'].fillna(final_data['Seats'].mode()[0], inplace=True)

final_data.drop(columns=['RTO'], inplace=True)

final_data.Ownership.value_counts()

final_data['Ownership'].fillna(final_data['Ownership'].mode()[0], inplace=True)

final_data['Year of Manufacture'].value_counts()

final_data['Year of Manufacture'].fillna(final_data['Year of Manufacture'].mode()[0], inplace=True)

final_data['Engine Displacement'].value_counts()

final_data['Engine Displacement'].fillna(final_data['Engine Displacement'].mode()[0], inplace=True)

final_data.isnull().sum()

final_data.drop(['Kms Driven','Ownership'],axis = 1,inplace = True)

final_data.head(1)

final_data['Seats'] = final_data['Seats'].str.extract('(\d+)').astype(float)


final_data['Engine Displacement'] = final_data['Engine Displacement'].str.extract('(\d+)').astype(float)

final_data.ft.value_counts()

final_data.bt.value_counts()

final_data.km.value_counts()

final_data.transmission.value_counts()

final_data.owner.value_counts()

final_data.oem.value_counts()

final_data.model.value_counts()

final_data.modelYear.value_counts()

final_data.variantName.value_counts()

final_data.price.value_counts()

import re

# Assuming 'price' is the column name
def convert_price(value):
    if 'Lakh' in value:
        value = re.sub(r'[^\d.]', '', value)  # Remove non-numeric characters except '.'
        value = float(value) * 100000  # 1 Lakh = 100,000
    elif 'Crore' in value:
        value = re.sub(r'[^\d.]', '', value)  # Remove non-numeric characters except '.'
        value = float(value) * 10000000  # 1 Crore = 10,000,000
    else:
        value = re.sub(r'[^\d.]', '', value)  # Remove non-numeric characters except '.'
        value = float(value)
    return value

final_data['price'] = final_data['price'].apply(convert_price)

final_data.price.value_counts()

final_data.place.value_counts()

final_data['Insurance Validity'].value_counts()

final_data['Fuel Type'].value_counts()

final_data['Seats'].value_counts()

final_data['Engine Displacement'].value_counts()

final_data['Transmission'].value_counts()

final_data['Year of Manufacture'].value_counts()

final_data['Features'].value_counts()

final_data['Comfort'].value_counts()

final_data['Interior'].value_counts()

final_data['Exterior'].value_counts()

final_data.head(1)

final_data.info()               #   km, price, Seats, Engine Displacement, Year of Manufacture,

# Assuming 'km', 'price', 'Seats', 'Engine Displacement', 'Year of Manufacture' are the column names
final_data['km'] = final_data['km'].astype(int)
final_data['price'] = final_data['price'].astype(int)
final_data['Seats'] = final_data['Seats'].astype(int)
final_data['Engine Displacement'] = final_data['Engine Displacement'].astype(int)
final_data['Year of Manufacture'] = final_data['Year of Manufacture'].astype(int)

final_data.info()

"""**EXPLORATORY DATA ANALYSIS**

distribution of all columns
"""

ft_counts = final_data['ft'].value_counts()

# Plotting the bar plot
plt.figure(figsize=(10, 6))
ft_counts.plot(kind='bar')
plt.title('Frequency of ft Values')
plt.xlabel('ft')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

# Assuming 'ft' is the column name
ft_counts = final_data['bt'].value_counts()

# Plotting the bar plot
plt.figure(figsize=(10, 6))
ft_counts.plot(kind='bar')
plt.title('Frequency of ft Values')
plt.xlabel('bt')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(final_data['km'], bins=20, color='skyblue', edgecolor='black')  # Adjust the number of bins as needed
plt.title('Histogram of km')
plt.xlabel('Kilometers Driven')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

columns_to_check = ['Year of Manufacture']

for column in columns_to_check:
    plt.figure(figsize=(10, 6))
    plt.hist2d(final_data[column], final_data['km'], bins=20, cmap='Blues')
    plt.colorbar(label='Frequency')
    plt.title(f'Histogram of km vs {column}')
    plt.xlabel(column)
    plt.ylabel('Kilometers Driven')
    plt.show()

ft_counts = final_data['transmission'].value_counts()

# Plotting the bar plot
plt.figure(figsize=(10, 6))
ft_counts.plot(kind='bar')
plt.title('Frequency of transmission Values')
plt.xlabel('transmission')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

ft_counts = final_data['owner'].value_counts()

# Plotting the bar plot
plt.figure(figsize=(10, 6))
ft_counts.plot(kind='bar')
plt.title('Frequency of owner Values')
plt.xlabel('owner')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

ft_counts = final_data['oem'].value_counts()

# Plotting the bar plot
plt.figure(figsize=(10, 6))
ft_counts.plot(kind='bar')
plt.title('Frequency of oem Values')
plt.xlabel('oem')
plt.ylabel('Frequency')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

# List of numeric columns
numeric_columns = ['km', 'price', 'Seats', 'Engine Displacement', 'Year of Manufacture']

# List of categorical columns
categorical_columns = ['ft', 'bt', 'transmission', 'owner', 'oem', 'model', 'modelYear', 'variantName', 'place',
                       'Insurance Validity', 'Fuel Type', 'Transmission']

# Plot histograms for numeric columns
for column in numeric_columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(final_data[column], kde=True, color='skyblue', edgecolor='black')
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Plot count plots for categorical columns
for column in categorical_columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=final_data, x=column, palette='viridis')
    plt.title(f'Count Plot of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

final_data.info ()



"""**VS PLOT**"""

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

# List of categorical columns
categorical_columns = ['ft', 'bt', 'transmission', 'owner', 'oem', 'modelYear']

# Plot violin plots for categorical columns vs price
for column in categorical_columns:
    plt.figure(figsize=(12, 6))
    sns.violinplot(x=final_data[column], y=final_data['price'], palette='muted', inner='quartile')
    plt.title(f'Violin plot of price vs {column}')
    plt.xlabel(column)
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(x=final_data['place'], y=final_data['price'], palette='muted')
plt.title('Bar plot of price vs place')
plt.xlabel('Place')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

# Sort the DataFrame by 'price' column in ascending order
sorted_final_data = final_data.sort_values(by='price')

plt.figure(figsize=(12, 6))
sns.barplot(x=sorted_final_data['place'], y=sorted_final_data['price'], palette='muted')
plt.title('Bar plot of price vs place (ascending order)')
plt.xlabel('Place')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

plt.figure(figsize=(12, 6))
sns.barplot(x=final_data['Insurance Validity'], y=final_data['price'], palette='muted')
plt.title('Bar plot of price vs Insurance Validity')
plt.xlabel('Insurance Validity')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

plt.figure(figsize=(12, 6))
sns.barplot(x=final_data['Fuel Type'], y=final_data['price'], palette='muted')
plt.title('Bar plot of price vs Fuel Type')
plt.xlabel('Fuel Type')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

plt.figure(figsize=(12, 6))
sns.barplot(x=final_data['Transmission'], y=final_data['price'], palette='muted')
plt.title('Bar plot of price vs Transmission')
plt.xlabel('Transmission')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

# Get the top 10 most frequent models
top_10_models = final_data['model'].value_counts().head(10).index.tolist()

# Filter the DataFrame for only the top 10 models
top_10_data = final_data[final_data['model'].isin(top_10_models)]

# Plotting
plt.figure(figsize=(12, 6))
sns.violinplot(x='model', y='price', data=top_10_data, palette='muted')
plt.title('Violin plot of price vs top 10 models')
plt.xlabel('Model')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your DataFrame is named 'final_data'

# List of numeric columns
numeric_columns = ['km', 'Seats', 'Engine Displacement', 'Year of Manufacture']

# Plot scatter plots for numeric columns
for column in numeric_columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=final_data[column], y=final_data['price'], color='skyblue')
    plt.title(f'Scatter plot of price vs {column}')
    plt.xlabel(column)
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()

# Assuming your cleaned DataFrame is named 'cleaned_data'
final_data.to_csv('cleaned_car_data.csv', index=False)

final_data.isnull().sum()