import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import i18n

from languages import translate_list


def categories_filter(categories, threshold):
    categories_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= threshold:
            categories_map[categories.index[i]] = categories.index[i]
        else:
            categories_map[categories.index[i]] = 'Other'
    return categories_map


def experience_clean(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)


def education_clean(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelor’s degree"


@st.cache  # in order to prevent from run each operation whenever the page loads
def load_data():
    df = pd.read_csv('./survey_results_public.csv')
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_categories_map = categories_filter(df.Country.value_counts(), 100)
    df["Country"] = df["Country"].map(country_categories_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(experience_clean)
    df["EdLevel"] = df["EdLevel"].apply(education_clean)

    return df


df = load_data()

def show_explore_page():
    st.markdown(i18n.t('title'), unsafe_allow_html=True)
    st.markdown(i18n.t('intro'))
    st.markdown('\n')
    
    data = df.Country.value_counts()

    st.markdown(i18n.t('title_graph_1'))
    st.markdown(i18n.t('comment_graph_1'))
    fig, ax = plt.subplots(1,1, figsize=(12,7))
    ax.barh(translate_list(data.index), data)
    st.pyplot(fig)
    st.markdown('\n')
    st.markdown('\n')

    st.markdown(i18n.t('title_graph_2'))
    st.markdown(i18n.t('comment_graph_2'))
    data = df.groupby(["Country"])["Salary"].mean()
    data_translated = pd.Series(data.values, index=translate_list(data.index))
    st.bar_chart(pd.DataFrame(data_translated, columns=[i18n.t('Salary')]))


    st.markdown(i18n.t('title_graph_3'))
    st.markdown(i18n.t('comment_graph_3'))
    data = df.groupby(["YearsCodePro"])["Salary"].mean()
    st.line_chart(pd.DataFrame(data.values, index=data.index, columns=[i18n.t('Salary')]))




