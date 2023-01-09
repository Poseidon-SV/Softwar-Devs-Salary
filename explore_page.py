import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'others'
            
        if categorical_map[categories.index[i]] == 'United Kingdom of Great Britain and Northern Ireland':
            categorical_map[categories.index[i]] = 'United Kingdom'
        if categorical_map[categories.index[i]] == "Other (please specify):":
            categorical_map[categories.index[i]] = "others"
    
    return categorical_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 51
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_mainBranch(x):
    if x == 'I am not primarily a developer, but I write code sometimes as part of my work':
        return 'Not a professional developer'
    if x == 'I am a developer by profession':
        return 'Professional developer'
    return str(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

profession = ["Data scientist",
"Front-end",
"Back-end",
"Full-Stack",
"Mobile",
"Game"]
def clean_devType(x):
    for p in profession:
        if p.lower() in x.lower():
            return p
    return str(x)


df = pd.read_csv('https://media.githubusercontent.com/media/Poseidon-SV/Datasets/main/survey_results_public.csv')

col_list=["Country", "EdLevel", "YearsCodePro", "Employment", "RemoteWork", 
          "YearsCode", "Age", "WorkExp", "MainBranch", "DevType", "ConvertedCompYearly"]

df = df[col_list]
df = df.rename({"ConvertedCompYearly": "Yearly Salary"}, axis=1)

df = df[df['Yearly Salary'].notnull()]

df["WorkExp"].fillna(0, inplace=True)
df = df.dropna()

df = df[df["Employment"]=="Employed, full-time"]
df = df.drop("Employment", axis = 1)

country_map = shorten_categories(df.Country.value_counts(), 350)
df['Country'] = df['Country'].map(country_map)

df = df[df["Age"]!='Prefer not to say']

df = df[df["Yearly Salary"] <= 250000]
df = df[df["Yearly Salary"] >= 10000]
df = df[df['Country'] != 'others']

df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
df['YearsCode'] = df['YearsCode'].apply(clean_experience)
df['MainBranch'] = df['MainBranch'].apply(clean_mainBranch)
df['DevType'] = df['DevType'].apply(clean_devType)
df['EdLevel'] = df['EdLevel'].apply(clean_education)

dev_map = shorten_categories(df.DevType.value_counts(), 150)
df['DevType'] = df['DevType'].map(dev_map)
# df = df[df['DevType'] != 'others']

@st.cache
def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(" ### Stack Overflow Developer Survey 2022 ")

    st.write("""#### Percentage of Data from different *Countries*""")
    countryData = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    explode = (0.0, 0.1, 0.1, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.3, 0.2)
    ax1.pie(countryData, labels=countryData.index, autopct="%1.1f%%", startangle=10, explode = explode,)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.set_title("Countries", pad=5)
    st.pyplot(fig1)

    st.write("# ")

    st.write("""#### Percentage of Data from different *Developer Types*""")
    devData = df["DevType"].value_counts()
    fig2, ax2 = plt.subplots()
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2)
    ax2.pie(devData, labels=devData.index, autopct="%1.1f%%", startangle=10, explode = explode,)
    ax2.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax2.set_title("Developer Types", pad=5)
    st.pyplot(fig2)

    st.write("# ")

    st.write("""#### Mean Salary Based On Country""")

    countrydata = df.groupby(["Country"])["Yearly Salary"].mean().sort_values(ascending=True)
    st.bar_chart(countrydata)

    st.write("# ")

    st.write("""#### Mean Salary Based On Developers""")

    devData = df.groupby(['DevType'])["Yearly Salary"].mean().sort_values(ascending=True)
    st.bar_chart(devData)

    st.write("# ")

    st.write("""#### Mean Salary Based On Experience""")

    proCodedata = df.groupby(["YearsCodePro"])["Yearly Salary"].mean().sort_values(ascending=True)
    codedata = df.groupby(["YearsCode"])["Yearly Salary"].mean().sort_values(ascending=True)
    data = {'Yaers coded professionally':proCodedata, 'Total years given to coding':codedata}
    st.line_chart(data)
    
    st.write("# ")

    st.write("""#### Mean Salary Based On Developer Status""")

    MBData = df.groupby(["MainBranch"])["Yearly Salary"].mean().sort_values(ascending=True)
    st.bar_chart(MBData)
    
    st.write("# ")

    st.write("""#### Mean Salary Based On Age""")

    ageData = df.groupby(["Age"])["Yearly Salary"].mean().sort_values(ascending=False)
    st.bar_chart(ageData)

