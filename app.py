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

st.write()

st.markdown("## Data related to our research question")

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


#####################################################################
st.markdown("### Average Gender Employment Gap (15+) by Region")

# Convert Year to numeric
df_merged["Year"] = pd.to_numeric(df_merged["Year"])

# Get the average gender gap for each country
df_summary2 = df_merged.groupby(["Country.Name", "Region"]).agg(
    avg_gap=("gender_gap", "mean")
).reset_index()

# Sort the data by the average gender gap (ascending order)
df_summary2 = df_summary2.sort_values(by="avg_gap", ascending=True)

# Define a custom color scale using hex codes for green and orange shades
custom_colorscale = [
    [0, "#006400"],  # Dark Green
    [0.25, "#90EE90"],  # Light Green
    [0.5, "#FFB84D"],  # Light Orange
    [0.75, "#FF8C00"],  # Dark Orange
    [1, "#FF4500"]  # Red-Orange
]

# Create a bar plot
fig = px.bar(
    df_summary2,
    x="Country.Name",
    y="avg_gap",
    color="Region",  # Color by Region
    color_continuous_scale=custom_colorscale,  # Custom color scale
    hover_data=["Country.Name", "Region"],
    title="Average Gender Employment Gap (15+) by Region",
    labels={"avg_gap": "Average Gender Gap (Male - Female Employment)", "Country.Name": "Country"},
    category_orders={"Country.Name": df_summary2["Country.Name"].tolist()}  # Ensure sorted order of countries
)

# Add a reference line for equal male/female ratio (avg_gap = 0)
fig.add_shape(
    type="line",
    x0=-0.5,  # Start position of the line (before the first bar)
    y0=0,  # The y position for the line (0 gap)
    x1=len(df_summary2) - 0.5,  # End position of the line (after the last bar)
    y1=0,  # Keep the line at y = 0
    line=dict(color="red", width=2, dash="dash")  # Red dashed line
)
st.plotly_chart(fig, use_container_width=True)

#####################################################################
st.markdown("### Average Gender Employment Gap (15+) by Region (Shown in an alternative way)")

# Convert Year to numeric
df_merged["Year"] = pd.to_numeric(df_merged["Year"])

# Get the average gender gap for each country
df_summary2 = df_merged.groupby(["Country.Name", "Region"]).agg(
    avg_gap=("gender_gap", "mean")
).reset_index()

# Sort the data by the average gender gap (ascending order)
df_summary2 = df_summary2.sort_values(by="avg_gap", ascending=True)

# Define a custom color scale using hex codes for green and orange shades
custom_colorscale = [
    [0, "#006400"],  # Dark Green
    [0.25, "#90EE90"],  # Light Green
    [0.5, "#FFB84D"],  # Light Orange
    [0.75, "#FF8C00"],  # Dark Orange
    [1, "#FF4500"]  # Red-Orange
]

# Force order to maintain sorting in plot
category_order = df_summary["Country.Name"].tolist()

# Create a bar plot
fig = px.bar(
    df_summary2,
    x="Country.Name",
    y="avg_gap",
    color="Region",  # Color by Region
    color_continuous_scale=custom_colorscale,  # Custom color scale
    hover_data=["Country.Name", "Region"],
    title="Average Gender Employment Gap (15+) by Region",
    labels={"avg_gap": "Average Gender Gap (Male - Female Employment)", "Country.Name": "Country"},
    category_orders={"Region": df_summary2["Region"].tolist()}  # Ensure sorted order of countries
)

# Add a reference line for equal male/female ratio (avg_gap = 0)
fig.add_shape(
    type="line",
    x0=-0.5,  # Start position of the line (before the first bar)
    y0=0,  # The y position for the line (0 gap)
    x1=len(df_summary2) - 0.5,  # End position of the line (after the last bar)
    y1=0,  # Keep the line at y = 0
    line=dict(color="red", width=2, dash="dash")  # Red dashed line
)
st.plotly_chart(fig, use_container_width=True)


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

st.markdown("### Average Gender Employment Gap (15-24 and 15+) by Income Group")
with open("youngGenderGapIncome.html", "r") as f:
    html_string = f.read()

# Embed it in your Streamlit app
components.html(html_string, height=600, width=900)

st.markdown("Conclusion")
