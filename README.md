
# 📊 Affiliate Investment Dashboard

This Streamlit app provides a detailed, interactive dashboard analyzing investment data from Royal Palm's affiliate marketing channel between **July 2024 and January 2025**. It helps to visualize customer behaviours, affiliate performance, and monthly trends.

---

This well detailed Investment Analytics Dashboard which I developed for UMéRA can be accessed live on streamlit [Here](https://umeraaffiliates.streamlit.app/)

---

## 📬 Author

**Gbenga Kajola**
🎓 Certified Data Analyst | 👨‍💻 Certified Data Scientist | 🧠 AI/ML Engineer | 📱 Mobile App Developer 

[LinkedIn](https://www.linkedin.com/in/kajolagbenga)

[Portfolio](https://kajolagbenga.netlify.app)

[Certified_Data_Scientist](https://www.datacamp.com/certificate/DSA0012312825030)

[Certified_Data_Analyst](https://www.datacamp.com/certificate/DAA0018583322187)

[Certified_SQL_Database_Programmer](https://www.datacamp.com/certificate/SQA0019722049554)


---

## 🚀 Features

- 📋 **Charts Tab:** Overview of customer type distribution and affiliate referrals by month.
- 📈 **Trends Tab:** Time-based comparisons of affiliate vs non-affiliate investments.
- 🤝 **Top Affiliates Tab:** Visual ranking of the top 10 performing affiliates.
- ⬇️ **Download Tab:** Export a comprehensive Word report of the analytics.
- 👨‍💻 **About Developer Tab:** Learn more about the creator.

---

## 📂 Data Source

- **File Name:** `royal_palm_receipt_portfolio.xlsx`
- **Sheet Used:** `AFFILIATES`
- **Fields Used:** `S/N`, `NAME`, `INVESTMENT YEAR`, `INVESTMENT MONTH`, `AFFILIATE`, `AFFILIATE 10%`

---

## 🧼 Data Preprocessing Steps

- Filtered records for investment year **2024** and **January 2025**.
- Removed rows with missing months or years.
- Categorized customers as **Affiliate** or **Non-Affiliate**.
- Ordered investment months chronologically for clear visualization.

---

## 📊 Visualizations

### Summary Tab
- **Bar Chart:** Customer type distribution (Affiliate vs Non-Affiliate).
- **Stacked Bar Chart:** Monthly count of affiliate vs non-affiliate referrals.

### Trends Tab
- **Area Chart:** Growth comparison between affiliate and non-affiliate referrals.
- **Line Plot:** Trend line for each group across months.
- **Heatmap:** Monthly distribution of affiliate contributions.
- **Pie & Doughnut Charts:** Proportional breakdown of customer types.

### Top Affiliates Tab
- **Bubble Chart:** Top 10 affiliates by number of referrals.
- **Treemap:** Referral distribution among top affiliates.

---

## 📤 Downloadable Report

- A full portfolio analytics report is available in Word format under the **Download** tab.

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Squarify](https://github.com/laserson/squarify)

---

## 📌 How to Run This App

1. Ensure the following Python libraries are installed:
```bash
pip install streamlit pandas matplotlib seaborn squarify plotly openpyxl
```

2. Place `royal_palm_receipt_portfolio.xlsx` in the same directory.

3. Run the app with:
```bash
streamlit run app.py
```

---

## 📎 License

This project is for educational and analysis purposes. All rights reserved to Kajola Gbenga.
