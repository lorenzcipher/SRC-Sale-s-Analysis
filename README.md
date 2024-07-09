# Consoto Sales' Analysis

![Header](img/header-image2.png)

In this project, I analysed the sales, profits and refund records of Microsoft's Consoto Dataset, comprising of transaction records from branches of the organization across three continents (Asia, Europe, and Nort America), with a total of 306 stores covering 4 channels (Online, store, catalog, and reseller) with three years of data (2014 to 2016), making a total of 2.28 million transactions.

I developed a dynamic dashboard using `Streamlit` and `Plotly` python libraries to help business managers monitor transactions on the fly, [click here](https://consoto-sales.streamlit.app/) to view the dashboard. The analysis was aimed at providing insights to help top excutives make better data driven business decisions for organizational growth.

**Objective:** To create reports or dashboards of `Revenues`, `Profits`, and `Returns/Refunds`.

To achieve the above objective, several business tasks which cut across revenue, profit, and refunds were drawn. These tasks will guide the development of the various reports. The business tasks are listed in sections below.

**Tools & Libraries:** The following tools and libraries were used to complete the analysis, visualization, and dashboard building - `SQL`, `Python`, `DuckDB`, `Pandas`, `Plotly`, and `Streamlit`.

**Processes of Analysis:** The steps applied during the entire project include:

-  _Data Preprocessing_: This step ensured that there were no duplicate records in the transaction (fact sale) table, and that empty or blank rows were properly handled before embarking on the report development.
-  _Exploratory Data Analysis_: There were a total of 9 table in the database which include `channel`, `entity`, `factsale`, `geography`, `product`, `productcategory`, `productsubcategory`, `promotion`, and `store`. Therefore, to analyse data across these tables, I made use of `SQL`, and analysed various aspect of the dataset, by solving the business tasks of each of the objective items. The SQL analysis script can be accessed [here]()

_Business Tasks_

The following business tasks were analyzed:

-  Revenue tasks:

   -  Calculate gross and net revenue, and identify the days that typically have the highest number of transactions.
   -  Which days have the highest revenue generation typically?
   -  Are the monthly trends consistent each year? And which months generates the most revenue?
   -  Which product category has be declining in sales? And which has been steady?
   -  Which channel generates the most income in revenue?

   To answer the above questions, I created the report or dashboard below:

   ![Revenue Report](img/1%20revenue-dashboard.png)

-  Profit tasks:

   -  Calculate total profit, and determine the product categories with the highest profit margin.
   -  Which products generate the most dollars in profit?
   -  Compare Profit in each month to profit margin in each month

   Answers to the above question provided in the report below:

   ![Profit Report](img/2%20profit-dashboard.png)

-  Refund tasks:

   -  What portion of total sales was refunded?
   -  Which Product Category has the most returns quantity?
   -  Which Product Category has the highest refund amount? The highest refund:sales ratio?
   -  What time of the year brings in the most refunds?

   The report below provides insights to the above queries.

![Refund Report](img/3%20refund-dashboard.png)

**_Insights & Recommendations_**

-  Computers, Cameras and camcoders are the highest monthly revenue generating product categories, however, they are also the categories with the highest return rates.
   -  Management should work on reducing the rate of returns in these product categories to the bearest minimum by identifying and managing customers reasons for the returns.
-  Music, Movies and Audio books product category generates the highest profit margin, but are the least in monthly revenue generation. And also has the most return:sales ratio.
   -  Management should consider running a promotional campaign to increase monthly sales in this category, and develop strategies to minimize the rate returns.
-  Year 2016 recorded the lowest monthly return rates.
   -  Management should work on maintaining minimal return rate monthly in subsequent business years by eliminating the challenges that lead to the return of goods by customers
"# SRC-Sale-s-Analysis" 
