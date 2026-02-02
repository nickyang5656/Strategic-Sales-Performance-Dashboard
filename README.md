# Strategic Sales & P&L Analysis Dashboard

## 🚀 Project Overview
[cite_start]This project provides an automated BI solution for an **EdTech consultancy** to address challenges in profitability tracking and sales quota accuracy[cite: 1, 6, 8]. [cite_start]By distinguishing between organic marketing revenue and agent-driven revenue, the dashboard offers a more realistic view of sales performance and financial health[cite: 7, 19, 20].

> [cite_start]**Disclaimer**: All datasets, company names, and personnel information are entirely synthetic, generated via Python for demonstration purposes[cite: 3, 4].

---

## 🛠️ Technical Implementation

### 1. Data Simulation (Python)
* [cite_start]**Tools**: Python (Pandas, NumPy)[cite: 10].
* [cite_start]**Logic**: Generated a synthetic 2-year dataset covering sales, expenses, and KPI targets[cite: 10].
* [cite_start]**Business Logic**: Simulated seasonal trends and channel attribution (Direct vs. Agent) to mimic real-world EdTech business cycles[cite: 11].

### 2. Data Modeling (Power BI)
* [cite_start]**Architecture**: Designed a **Galaxy Schema**[cite: 12].
* [cite_start]**Implementation**: Connected multiple fact tables (`Fact_Sales` and `Fact_Targets`) through shared dimension tables (`Date` and `Employee`) to support multi-grain analysis[cite: 13].

### 3. Analysis & Metrics (DAX)
* [cite_start]**Key Metrics**: Developed DAX measures for Net Profit Margin, Sales Target Achievement Rate, and Revenue Variance[cite: 14].
* [cite_start]**Advanced Logic**: Implemented dynamic time intelligence (YTD/QTD) for flexible reporting[cite: 15].

---

## 📈 Key Insights & Business Impact

* [cite_start]**Profitability Optimization**: Identified that the "Seminar" product line, despite high revenue, suffered from the lowest profit margins[cite: 17]. [cite_start]Recommended shifting focus to "Application Services" to enhance bottom-line profitability[cite: 18].
* [cite_start]**Sales Performance Correction**: Found that sales quotas were inflated by marketing-driven revenue[cite: 19]. [cite_start]Proposed a new model excluding direct sales, which adjusted team achievement rates from an artificial **30%** to a realistic **90-110%**, significantly boosting staff morale and retention[cite: 20, 21].

---

## 📂 Repository Structure
* [cite_start]`01_Executive_Summary_Report.pdf`: Detailed project breakdown[cite: 1].
* [cite_start]`02_Dashboard_Screenshots.pdf`: Visualizations of the final Power BI dashboard[cite: 22].
* [cite_start]`03_Data_Generator_Pipeline.py`: Python scripts used for data simulation[cite: 10].
* [cite_start]`04_Sales_Performance_Dashboard_Final.pbix`: The source Power BI file[cite: 106].
