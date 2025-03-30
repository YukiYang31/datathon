# to run, do
# streamlit run app.py


import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
# import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("coded_reshaped_mdg.csv")

countryMetadata = pd.read_csv("Country - Metadata.csv")
countryMetadata = countryMetadata.set_index("Code")[["Income Group", "Region"]]
newDF = df.set_index("Country.Code")[["Country.Name", "Year", "employ_pop_ratio_15plus_female", "employ_pop_ratio_15plus_male", "employ_pop_ratio_15plus_total", "ppp_conversion_private", "employ_pop_ratio_15-24_female", "employ_pop_ratio_15-24_male"]]
df_merged = newDF.join(countryMetadata, how="left")

st.title("Gender Gap ")

st.markdown("## Research Question")

st.write("How do employment gender gap manifest in countries of different income level?")

# st.markdown("## Data related to our research question")

# drop regions
df_merged = df_merged.dropna(axis=0, subset=['Income Group', 'Region', 'employ_pop_ratio_15plus_female', 'employ_pop_ratio_15plus_male'])

#####################################################################
st.markdown("### Average Gender Employment Gap (15+) by Income Group")
df_merged["gender_gap"] = df_merged["employ_pop_ratio_15plus_male"] - df_merged["employ_pop_ratio_15plus_female"]

# Convert Year to numeric
df_merged["Year"] = pd.to_numeric(df_merged["Year"])

# Get the average gender gap for each country
df_summary = df_merged.groupby(["Country.Name", "Income Group"]).agg(
    avg_gap=("gender_gap", "mean")
).reset_index()

# Sort only by gender gap, ignoring income groups
df_summary = df_summary.sort_values(by="avg_gap", ascending=True)

# Define fixed colors for each income group
income_colors = {
    "Low income": "#1f77b4",  # Dark Blue
    "Lower middle income": "#aec7e8",  # Light Blue
    "Upper middle income": "#ffbb78",  # Light Orange
    "High income": "#ff7f0e",  # Dark Orange
}

# Force order to maintain sorting in plot
category_order = df_summary["Country.Name"].tolist()

# Create a bar plot with fixed colors, while keeping overall sorting
fig = px.bar(
    df_summary,
    x="Country.Name",
    y="avg_gap",
    color="Income Group",  # Color by Income Group
    color_discrete_map=income_colors,  # Use fixed colors
    hover_data=["Country.Name", "Income Group"],
    title="Average Gender Employment Gap (15+) by Income Group",
    labels={"avg_gap": "Average Gender Gap (Male - Female Employment)", "Country.Name": "Country"},
    category_orders={"Country.Name": category_order}  # Force order
)

# Add a reference line for equal male/female employment ratio
fig.add_shape(
    type="line",
    x0=-0.5,  # Start of the line
    y0=0,  # y=0 is the reference point (equal employment)
    x1=len(df_summary) - 0.5,  # End of the line
    y1=0,  # Keep it horizontal
    line=dict(color="red", width=2, dash="dash")  # Red dashed reference line
)
st.plotly_chart(fig, use_container_width=True)
st.write("From this chart, we see that almost every country has a higher male employment and very little correlate with the country's income level.")

#####################################################################
st.markdown("### Average Gender Employment Gap (15+) by Region")

with open("15region.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)
st.write("From this chart, we can see that middle east and north africa has the biggest gender gap.")

#####################################################################st.markdown("### Average Gender Employment Gap (15+) by Region (Shown in an alternative way)")
with open("15regionA.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)
st.write("Organizing the chart grouping by regions, we can further see that middle east and north Africa has the biggest average gender gap. South Asia has the biggest variation in gender gaps. ")

#####################################################################
st.markdown("### Average Gender Employment Gap (15-24) by Income Group")
onlyCountries = df_merged.dropna(axis=0, subset=['Income Group', 'Region'])
countryMetadata = pd.read_csv("Country - Metadata.csv")
countryMetadata = countryMetadata.set_index("Code")[["Income Group", "Region"]]

# Select relevant columns from df and set index
newDF = df.set_index("Country.Code")[
    [
        "Country.Name", "Year",
        "employ_pop_ratio_15-24_female", "employ_pop_ratio_15-24_male", "employ_pop_ratio_15-24_total",
        "ppp_conversion_private"
    ]
]

# Merge datasets
df_merged = newDF.join(countryMetadata, how="left")

# Compute gender employment gap for 15-24 age group
df_merged["gender_gap_15_24"] = df_merged["employ_pop_ratio_15-24_male"] - df_merged["employ_pop_ratio_15-24_female"]

# Convert Year to numeric
df_merged["Year"] = pd.to_numeric(df_merged["Year"])

# Get the average gender gap for each country (15-24 age group)
df_summary = df_merged.groupby(["Country.Name", "Income Group"]).agg(
    avg_gap_15_24=("gender_gap_15_24", "mean")
).reset_index()

# Sort only by gender gap for 15-24 age group, independent of income groups
df_summary = df_summary.sort_values(by="avg_gap_15_24", ascending=True)

# Define fixed colors for each income group
income_colors = {
    "Low income": "#1f77b4",  # Dark Blue
    "Lower middle income": "#aec7e8",  # Light Blue
    "Upper middle income": "#ffbb78",  # Light Orange
    "High income": "#ff7f0e",  # Dark Orange
}

# Force order to maintain sorting in plot
category_order = df_summary["Country.Name"].tolist()

# Create a bar plot with fixed colors while keeping overall sorting
fig = px.bar(
    df_summary,
    x="Country.Name",
    y="avg_gap_15_24",  # Use the 15-24 employment gap
    color="Income Group",  # Color by Income Group
    color_discrete_map=income_colors,  # Use fixed colors
    hover_data=["Country.Name", "Income Group"],
    title="Average Gender Employment Gap (15-24) by Income Group",
    labels={"avg_gap_15_24": "Average Gender Gap (Male - Female Employment)", "Country.Name": "Country"},
    category_orders={"Country.Name": category_order}  # Force order
)

# Add a reference line for equal male/female employment ratio
fig.add_shape(
    type="line",
    x0=-0.5,  # Start of the line
    y0=0,  # y=0 is the reference point (equal employment)
    x1=len(df_summary) - 0.5,  # End of the line
    y1=0,  # Keep it horizontal
    line=dict(color="red", width=2, dash="dash")  # Red dashed reference line
)

st.plotly_chart(fig, use_container_width=True)

##################################################################
st.markdown("### Average Gender Employment Gap (15-24 and 15+) by Income Group")
with open("youngGenderGapIncome.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)


st.markdown("### Gender Gap in Self-Employment by Income Group")
with open("self.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)


st.markdown("### Gender Gap in Vulnerable Employment by Income Group")
with open("vulnerable.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)


##################################################################
st.markdown("### Gender Gap in Contributing Workers by Income Group")
with open("contirbute.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)


##################################################################

st.markdown("### Change in Gender Employment Gap (15+) Over Time (2006-2015) by Country")
with open("changesOvertime.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)

st.markdown("Conclusion")
st.write("")
