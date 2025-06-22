import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from wordcloud import WordCloud
import squarify
import plotly.express as px
from datetime import datetime

# Set page config with modern design
st.set_page_config(
    page_title="Affiliate Investment Dashboard",
    layout="wide",
    page_icon="📈"
)

# Inject CSS for UI enhancements
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [role="tab"] {
        font-size: 18px;
        padding: 10px;
    }
    .css-18e3th9 { padding: 2rem 2rem 2rem 2rem; }
    </style>
""", unsafe_allow_html=True)

# Load data
def load_data():
    file_path = "royal_palm_receipt_portfolio.xlsx"
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="AFFILIATES")
    return df

# Load & preprocess
with st.spinner("Loading and cleaning data..."):
    df = load_data()
    df = df[["S/N", "NAME", "INVESTMENT YEAR", "INVESTMENT MONTH", "AFFILIATE", "AFFILIATE 10%"]]
    df = df.dropna(subset=["INVESTMENT YEAR", "INVESTMENT MONTH"])
    df["INVESTMENT YEAR"] = df["INVESTMENT YEAR"].astype(int)
    df = df[(df["INVESTMENT YEAR"] == 2024) | ((df["INVESTMENT YEAR"] == 2025) & (df["INVESTMENT MONTH"] == "JANUARY"))]
    df = df.iloc[:-2]
    df["Came_Through_Affiliate"] = df["AFFILIATE"].apply(lambda x: x != "NIL")
    df["Affiliate_Label"] = df["Came_Through_Affiliate"].map({True: "Affiliate", False: "Non-Affiliate"})
    month_order = ["JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
    df["INVESTMENT MONTH"] = pd.Categorical(df["INVESTMENT MONTH"], categories=month_order, ordered=True)
    affiliate_by_month = pd.crosstab(df["INVESTMENT MONTH"], df["Came_Through_Affiliate"])
    top_affiliates = df[df["AFFILIATE"] != "NIL"]["AFFILIATE"].value_counts().head(10)

st.title("📊 Affiliate Investment Analysis Dashboard")
st.markdown("""
    This dashboard provides a detailed interactive analysis of customer investments via affiliate channels.
""")

# Tabs for better structure
summary_tab, trends_tab, affiliate_tab, download_tab, about_developer = st.tabs(["📋 Charts", "📈 Trends", "🤝 Top Performing Affiliates", "⬇️ Download", "👨‍💻 About the Developer"])


with summary_tab:
    col1, col2 = st.columns(2)

    # CSS to equalize chart heights
    chart_style = """
        <style>
            .chart-box {
                height: 350px;
                overflow: hidden;
            }
        </style>
    """
    st.markdown(chart_style, unsafe_allow_html=True)

    with col1:
        st.subheader("Customers Distribution")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x="Affiliate_Label", hue="Affiliate_Label", palette="coolwarm", ax=ax, legend=False)
        ax.set_xlabel("Customer Type")
        ax.set_ylabel("Count")
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        # Stacked Bar Chart
        st.subheader("Number of Customers Through Affiliates Per Month")
        fig, ax = plt.subplots(figsize=(5, 4))
        affiliate_by_month.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
        ax.set_xlabel("Investment Month")
        ax.set_ylabel("Count of Customers")
        fig.tight_layout()
        st.pyplot(fig)


with trends_tab:
    st.subheader("Affiliate vs. Non-Affiliate Growth Over Months")
    fig = px.area(
        affiliate_by_month,
        x=affiliate_by_month.index,
        y=[True, False],
        labels={"value": "Customer Count", "variable": "Type"},
        title="Monthly Trend of Affiliate vs. Non-Affiliate",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Line Chart with Trend Analysis
    st.subheader("Growth Trend of Affiliate vs. Non-Affiliate Customers")
    fig, ax = plt.subplots()
    sns.lineplot(x=affiliate_by_month.index, y=affiliate_by_month[True], label="Affiliate", marker="o", ax=ax)
    sns.lineplot(x=affiliate_by_month.index, y=affiliate_by_month[False], label="Non-Affiliate", marker="o", ax=ax)
    ax.set_xlabel("Investment Month")
    ax.set_ylabel("Customer Count")
    st.pyplot(fig)

    st.subheader("Customer Type Distribution per Month (Heatmap)")
    fig, ax = plt.subplots()
    sns.heatmap(affiliate_by_month, cmap="coolwarm", annot=True, fmt="d", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    # Stacked Bar Chart
    st.subheader("Number of Customers Through Affiliates Per Month")
    fig, ax = plt.subplots()
    affiliate_by_month.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set_xlabel("Investment Month")
    ax.set_ylabel("Count of Customers")
    st.pyplot(fig)

    # Pie Chart
    st.subheader("Affiliate vs. Non-Affiliate Customers")
    fig, ax = plt.subplots()
    df["Came_Through_Affiliate"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'})
    ax.set_ylabel("")
    st.pyplot(fig)

    # Doughnut Pie Chart
    st.subheader("Affiliate vs. Non-Affiliate Customers")
    fig, ax = plt.subplots()
    df["Came_Through_Affiliate"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=90, wedgeprops={'edgecolor': 'black'})
    ax.add_artist(plt.Circle((0, 0), 0.6, fc='white'))
    ax.set_ylabel("")
    st.pyplot(fig)


with affiliate_tab:

    st.subheader("Top 10 Affiliates (Bubble Size = Number of investors brought in)")
    fig = px.scatter(
        x=top_affiliates.index,
        y=top_affiliates.values,
        size=top_affiliates.values,
        color=top_affiliates.index,
        labels={'x': 'Affiliate Name', 'y': 'Referrals'},
        title="Top Referring Affiliates"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Performance Treemap of Top Affiliates")
    fig = px.treemap(
        names=top_affiliates.index,
        parents=["" for _ in top_affiliates],
        values=top_affiliates.values,
        title="Treemap of Referrals by Top Affiliates"
    )
    st.plotly_chart(fig, use_container_width=True)

    # st.subheader("Top Performing Affiliates Word Cloud")
    # wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(df[df["AFFILIATE"] != "NIL"]["AFFILIATE"]))
    # fig, ax = plt.subplots()
    # ax.imshow(wordcloud, interpolation="bilinear")
    # ax.axis("off")
    # st.pyplot(fig)

# with download_tab:
#     st.subheader("📤 Export Cleaned Data")
#     df.to_excel("Cleaned_Affiliate_Report.xlsx", index=False)
#     with open("Cleaned_Affiliate_Report.xlsx", "rb") as f:
#         st.download_button("Download Excel Report", f, file_name="Cleaned_Affiliate_Report.xlsx")

# Word Report Download
with download_tab:
    st.markdown("### \U0001F4DD Download Full UMéRA Portfolio Analytics Report")
    with open("UMéRA Royal Palm Data Analytics Report.docx", "rb") as doc_file:
        st.download_button(
            label="\U0001F4E5 Download Full Word Report",
            data=doc_file,
            file_name="UMeRA_RoyalPalm_Analytics_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        st.markdown("---")
        st.info("This report presents a seven month in-depth analytics of the Royal Palm investment portfolio data for the period spanning July 2024 to January 2025.")
        st.info("The objective is to identify trends, investors’ behaviour, distribution of investments across different land types and unit types, age segmentation, and most importantly a robust analytics on the affiliates and their pivotal roles during the seven month period.")

with about_developer:
    st.markdown("# The brain behind this project")

    st.image("Gbenga.jpg", width=300)
    st.markdown("## **Kajola Gbenga**")

    st.markdown(
        """
    \U0001F4C7 Certified Data Analyst | Certified Data Scientist | Certified SQL Programmer | Mobile App Developer | AI/ML Engineer

    \U0001F517 [LinkedIn](https://www.linkedin.com/in/kajolagbenga)  
    \U0001F4DC [View My Certifications & Licences](https://www.datacamp.com/portfolio/kgbenga234)  
    \U0001F4BB [GitHub](https://github.com/prodigy234)  
    \U0001F310 [Portfolio](https://kajolagbenga.netlify.app/)  
    \U0001F4E7 k.gbenga234@gmail.com
    """
    )