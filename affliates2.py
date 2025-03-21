import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import plotly.express as px
import numpy as np
from wordcloud import WordCloud

# Load the Excel file
file_path = "ROYAL PALM RECEIPT & PORTFOLIO (3).xlsx"
xls = pd.ExcelFile(file_path)

# Load the "PORTFOLIO" sheet
df = pd.read_excel(xls, sheet_name="PORTFOLIO")

# Select relevant columns
df = df[["S/N", "NAME", "INVESTMENT YEAR", "INVESTMENT MONTH", "AFFILIATE", "AFFILIATE 10%"]]

# Data Cleaning and Filtering
df = df.dropna(subset=["INVESTMENT YEAR", "INVESTMENT MONTH"])
df["INVESTMENT YEAR"] = df["INVESTMENT YEAR"].astype(int)
df = df[(df["INVESTMENT YEAR"] == 2024) | ((df["INVESTMENT YEAR"] == 2025) & (df["INVESTMENT MONTH"] == "JANUARY"))]

# Remove last two refunded/incomplete customers
df = df.iloc[:-2]

# Mark customers that came through affiliates
df["Came_Through_Affiliate"] = df["AFFILIATE"].apply(lambda x: x != "NIL")

# Define correct month order
month_order = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
df["INVESTMENT MONTH"] = pd.Categorical(df["INVESTMENT MONTH"], categories=month_order, ordered=True)

# Cross-tabulation of affiliates by month
affiliate_by_month = pd.crosstab(df["INVESTMENT MONTH"], df["Came_Through_Affiliate"])

# Streamlit App
st.title("Affiliate Analysis Dashboard")

# Pie Chart
st.subheader("Affiliate vs. Non-Affiliate Customers")
fig, ax = plt.subplots()
df["Came_Through_Affiliate"].value_counts().plot.pie(autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'}, ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# Heatmap
st.subheader("Heatmap of Affiliate vs. Non-Affiliate Customers Per Month")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(affiliate_by_month, cmap="coolwarm", annot=True, fmt="d", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Word Cloud
st.subheader("Top Affiliates Word Cloud")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(df[df["AFFILIATE"] != "NIL"]["AFFILIATE"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Treemap
st.subheader("Treemap of Top Affiliates")
top_affiliates = df[df["AFFILIATE"] != "NIL"]["AFFILIATE"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
squarify.plot(sizes=top_affiliates.values, label=top_affiliates.index, alpha=0.8, color=plt.cm.Set3.colors)
ax.set_axis_off()
st.pyplot(fig)

# 3D Bar Chart
st.subheader("3D Bar Chart of Affiliate vs. Non-Affiliate Customers")
fig = px.bar(df, x="INVESTMENT MONTH", y=df["Came_Through_Affiliate"].astype(int), color="Came_Through_Affiliate", barmode="group", height=500, title="3D Bar Chart of Affiliate vs. Non-Affiliate Customers", labels={"Came_Through_Affiliate": "Affiliate Status"})
st.plotly_chart(fig)

# Save cleaned data
df.to_excel("Cleaned_Affiliate_Report.xlsx", index=False)
st.success("Cleaned data saved successfully!")