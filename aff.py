import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import squarify
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

def load_data():
    file_path = "ROYAL PALM RECEIPT & PORTFOLIO (3).xlsx"
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="PORTFOLIO")
    return df

st.title("Affiliate Investment Analysis Dashboard")

# Load Data
df = load_data()
df = df[["S/N", "NAME", "INVESTMENT YEAR", "INVESTMENT MONTH", "AFFILIATE", "AFFILIATE 10%"]]
df = df.dropna(subset=["INVESTMENT YEAR", "INVESTMENT MONTH"])
df["INVESTMENT YEAR"] = df["INVESTMENT YEAR"].astype(int)
df = df[(df["INVESTMENT YEAR"] == 2024) | ((df["INVESTMENT YEAR"] == 2025) & (df["INVESTMENT MONTH"] == "JANUARY"))]
df = df.iloc[:-2]
df["Came_Through_Affiliate"] = df["AFFILIATE"].apply(lambda x: x != "NIL")
month_order = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
df["INVESTMENT MONTH"] = pd.Categorical(df["INVESTMENT MONTH"], categories=month_order, ordered=True)
affiliate_by_month = pd.crosstab(df["INVESTMENT MONTH"], df["Came_Through_Affiliate"])
top_affiliates = df[df["AFFILIATE"] != "NIL"]["AFFILIATE"].value_counts().head(10)

# Bar Chart
st.subheader("Customers Through Affiliates vs. Non-Affiliates")
fig, ax = plt.subplots()
sns.countplot(x=df["Came_Through_Affiliate"].map({True: "Affiliate", False: "Non-Affiliate"}), palette="coolwarm", ax=ax)
st.pyplot(fig)

# Pie Chart
st.subheader("Affiliate vs. Non-Affiliate Customers")
fig, ax = plt.subplots()
df["Came_Through_Affiliate"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'})
ax.set_ylabel("")
st.pyplot(fig)

# Area Chart
st.subheader("Trend of Affiliate vs. Non-Affiliate Customers Over Time")
fig, ax = plt.subplots()
affiliate_by_month.plot.area(ax=ax, colormap="plasma", alpha=0.75)
ax.set_xlabel("Investment Month")
ax.set_ylabel("Count")
st.pyplot(fig)

# Word Cloud
st.subheader("Top Affiliates Word Cloud")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(df[df["AFFILIATE"] != "NIL"]["AFFILIATE"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Pie Chart
st.subheader("Affiliate vs. Non-Affiliate Customers")
fig, ax = plt.subplots()
df["Came_Through_Affiliate"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'})
ax.add_artist(plt.Circle((0, 0), 0.6, fc='white'))
ax.set_ylabel("")
st.pyplot(fig)

# Stacked Bar Chart
st.subheader("Number of Customers Through Affiliates Per Month")
fig, ax = plt.subplots()
affiliate_by_month.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
ax.set_xlabel("Investment Month")
ax.set_ylabel("Count of Customers")
st.pyplot(fig)

# Bubble Chart
st.subheader("Bubble Chart of Top Affiliates")
fig, ax = plt.subplots()
sns.scatterplot(x=top_affiliates.index, y=top_affiliates.values, size=top_affiliates.values, sizes=(100, 1000), alpha=0.6, palette="coolwarm", hue=top_affiliates.index, legend=False, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Heatmap
st.subheader("Heatmap of Affiliate vs. Non-Affiliate Customers Per Month")
fig, ax = plt.subplots()
sns.heatmap(affiliate_by_month, cmap="coolwarm", annot=True, fmt="d", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Additional Heatmap
st.subheader("Heatmap of Affiliate vs. Non-Affiliate Customers Per Month")
affiliate_heatmap = pd.crosstab(df["INVESTMENT MONTH"], df["Came_Through_Affiliate"].replace({True: "Affiliate", False: "Non-Affiliate"}))
fig, ax = plt.subplots()
sns.heatmap(affiliate_heatmap, cmap="coolwarm", annot=True, fmt="d", ax=ax)
st.pyplot(fig)

# Treemap
st.subheader("Treemap of Top Affiliates")
fig, ax = plt.subplots()
squarify.plot(sizes=top_affiliates.values, label=top_affiliates.index, alpha=0.8, color=plt.cm.Set3.colors)
ax.axis("off")
st.pyplot(fig)

# Line Chart with Trend Analysis
st.subheader("Growth Trend of Affiliate vs. Non-Affiliate Customers")
fig, ax = plt.subplots()
sns.lineplot(x=affiliate_by_month.index, y=affiliate_by_month[True], label="Affiliate", marker="o", ax=ax)
sns.lineplot(x=affiliate_by_month.index, y=affiliate_by_month[False], label="Non-Affiliate", marker="o", ax=ax)
ax.set_xlabel("Investment Month")
ax.set_ylabel("Customer Count")
st.pyplot(fig)

# 3D Bar Chart
st.subheader("3D Bar Chart of Affiliate vs. Non-Affiliate Customers")
fig = px.bar(df, x="INVESTMENT MONTH", y=df["Came_Through_Affiliate"].astype(int), color="Came_Through_Affiliate", barmode="group", height=500)
st.plotly_chart(fig)

# Save Processed Data
output_file = "Cleaned_Affiliate_Report.xlsx"
df.to_excel(output_file, index=False)

# Allow users to download Word Report
st.subheader("Download Report")
report_file = "Affiliate_Analysis_Report.docx"
with open(report_file, "rb") as file:
    btn = st.download_button(label="Download Word Report", data=file, file_name=report_file, mime="application/msword")

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from wordcloud import WordCloud
# import squarify
# import plotly.express as px
# import plotly.graph_objects as go
# from io import BytesIO

# def load_data():
#     file_path = "ROYAL PALM RECEIPT & PORTFOLIO (3).xlsx"
#     xls = pd.ExcelFile(file_path)
#     df = pd.read_excel(xls, sheet_name="PORTFOLIO")
#     return df

# st.title("Affiliate Investment Analysis Dashboard")

# # Load Data
# df = load_data()
# df = df[["S/N", "NAME", "INVESTMENT YEAR", "INVESTMENT MONTH", "AFFILIATE", "AFFILIATE 10%"]]
# df = df.dropna(subset=["INVESTMENT YEAR", "INVESTMENT MONTH"])
# df["INVESTMENT YEAR"] = df["INVESTMENT YEAR"].astype(int)
# df = df[(df["INVESTMENT YEAR"] == 2024) | ((df["INVESTMENT YEAR"] == 2025) & (df["INVESTMENT MONTH"] == "JANUARY"))]
# df = df.iloc[:-2]
# df["Came_Through_Affiliate"] = df["AFFILIATE"].apply(lambda x: x != "NIL")
# month_order = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
# df["INVESTMENT MONTH"] = pd.Categorical(df["INVESTMENT MONTH"], categories=month_order, ordered=True)
# affiliate_by_month = pd.crosstab(df["INVESTMENT MONTH"], df["Came_Through_Affiliate"])
# top_affiliates = df[df["AFFILIATE"] != "NIL"]["AFFILIATE"].value_counts().head(10)

# # Area Chart
# st.subheader("Trend of Affiliate vs. Non-Affiliate Customers Over Time")
# fig, ax = plt.subplots()
# affiliate_by_month.plot.area(ax=ax, colormap="plasma", alpha=0.75)
# ax.set_xlabel("Investment Month")
# ax.set_ylabel("Count")
# st.pyplot(fig)

# # Word Cloud
# st.subheader("Top Affiliates Word Cloud")
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(df[df["AFFILIATE"] != "NIL"]["AFFILIATE"]))
# fig, ax = plt.subplots()
# ax.imshow(wordcloud, interpolation="bilinear")
# ax.axis("off")
# st.pyplot(fig)

# # Pie Chart
# st.subheader("Affiliate vs. Non-Affiliate Customers")
# fig, ax = plt.subplots()
# df["Came_Through_Affiliate"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'})
# ax.set_ylabel("")
# st.pyplot(fig)

# # Bar Chart
# st.subheader("Customers Through Affiliates vs. Non-Affiliates")
# fig, ax = plt.subplots()
# sns.countplot(x=df["Came_Through_Affiliate"].map({True: "Affiliate", False: "Non-Affiliate"}), palette="coolwarm", ax=ax)
# st.pyplot(fig)

# # Treemap
# st.subheader("Treemap of Top Affiliates")
# fig, ax = plt.subplots()
# squarify.plot(sizes=top_affiliates.values, label=top_affiliates.index, alpha=0.8)
# ax.axis("off")
# st.pyplot(fig)

# # 3D Bar Chart
# st.subheader("3D Bar Chart of Affiliate vs. Non-Affiliate Customers")
# fig = px.bar(df, x="INVESTMENT MONTH", y=df["Came_Through_Affiliate"].astype(int), color="Came_Through_Affiliate", barmode="group", height=500)
# st.plotly_chart(fig)

# # Save Processed Data
# output_file = "Cleaned_Affiliate_Report.xlsx"
# df.to_excel(output_file, index=False)

# # Allow users to download Word Report
# st.subheader("Download Report")
# report_file = "Affiliate_Analysis_Report.docx"
# with open(report_file, "rb") as file:
#     btn = st.download_button(label="Download Word Report", data=file, file_name=report_file, mime="application/msword")
