import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor_loaded = data["model"]
le_Country = data["le_Country"]
le_EdLevel = data['le_EdLevel']
le_RemoteWork = data['le_RemoteWork']
le_Age = data['le_Age']
le_MainBranch = data['le_MainBranch']
le_DevType = data['le_DevType']


def show_predict_page():
    st.title("Software Developer Salary Prediction App 👨‍💻")

    st.write("""### We need some information to predict the salary (Please fill in all details)""")

    countries = (
        'United Kingdom',
        'Netherlands',
        'United States of America',
        'Italy',
        'Canada',
        'Germany',
        'Poland',
        'France',
        'Brazil',
        'Sweden',
        'Spain',
        'Turkey',
        'India',
        'Switzerland',
        'Australia',
        'Russian Federation'
    )

    educations = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    )

    remoteWorks = (
        'Hybrid (some remote, some in-person)',
        'Fully remote',
        'Full in-person'
    )

    ages = (
        '25-34 years old',
        '18-24 years old',
        '35-44 years old',
        '55-64 years old',
        '45-54 years old',
        '65 years or older',
        'Under 18 years old'
    )

    mainBranchs = (
        'Not professional developer',
        'Professional developer'
    )

    devTypes = (
        'Data scientist',
        'Back-end',
        'Full-Stack',
        'Front-end',
        'Developer, desktop or enterprise applications',
        'Developer, embedded applications or devices',
        'Others',
        'Engineering manager',
        'Mobile'
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", educations)
    remoteWork = st.selectbox("Remote work", remoteWorks)
    age = st.slider("Your age", 15, 80, 21, step=1,)
    mainBranch = st.selectbox("Status as a developer", mainBranchs)
    devType = st.radio("Developer Profile", devTypes)
    yearsCoded = st.number_input("Years you have been coding in total", 0, 50, 2)
    yearsCodePro = st.number_input("Years you have coded professionally", 0, 50, 1)
    expericence = st.slider("Years of Working Experience", 0, 50, 2)

    if age < 18:
        age = ages[6]
    elif 18 <= age < 25:
        age = ages[1]
    elif 25 <= age < 35:
        age = ages[0]
    elif 35 <= age < 45:
        age = ages[2]
    elif 45 <= age < 55:
        age = ages[4]
    elif 55 <= age < 65:
        age = ages[3]
    elif 65 <= age:
        age = ages[5]

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, remoteWork, age, mainBranch,
                       devType, yearsCoded, yearsCodePro, expericence]])
        X[:, 0] = le_Country.transform(X[:, 0])
        X[:, 1] = le_EdLevel.transform(X[:, 1])
        X[:, 2] = le_RemoteWork.transform(X[:, 2])
        X[:, 3] = le_Age.transform(X[:, 3])
        X[:, 4] = le_MainBranch.transform(X[:, 4])
        X[:, 5] = le_DevType.transform(X[:, 5])

        X = X.astype(float)

        salary = regressor_loaded.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]}")
