import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from pmdarima import auto_arima
from pmdarima.arima.utils import ndiffs
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import numpy as np
import streamlit as sl
import plotly.graph_objects as go

from streamlit_option_menu import option_menu
from components.metrics import (
    plot_transact_by_day,
    plot_sales_by_day,
    plot_gsales_metric,
    plot_trans_metric,
    plot_actual_trans_metric,
    plot_sales_by_month,
    plot_sales_by_category,
    plot_profit_metric,
    plot_profitmargin_metric,
    plot_profit_by_product,
    plot_profit_by_category,
    plot_profit_by_month,
    plot_sales_by_channel,
    plot_refund_metric,
    plot_refundmargin_metric,
    plot_returnq_by_category,
    plot_return_amount_by_category,
    plot_return_by_month,
    get_reference,
)



# ========= Page setup ======================
sl.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

from components.db import data

# from pathlib import Path
from components.css import css

# go to webfx.com/tools/emoji-cheat-sheet/ for emoji's

# ========= CSS ===============
sl.markdown(css, unsafe_allow_html=True)

sl.sidebar.image("img/logo.jpg", use_column_width=True)
sl.header("Rapide Services Car II : Sale's Analysis :bar_chart:")
with sl.sidebar:

    selected = option_menu(
        menu_title="Dashboard",
        options=["Revenue", "Profit", "forecasting"],
        icons=["receipt-cutoff", "cash-coin", "currency-dollar"],
        default_index=0,
        orientation="vertical",
    )
    "---"


if selected == "Revenue":
    # ======== Filter Pane ======
    with sl.sidebar:
        year = data["Year"].unique()
        year.sort()
        continent = data["States"].unique()
        continent.sort()

        sl.header("Apply Filter")
        checked = sl.checkbox("Check this box to select multiple states")
        
        if checked:
            contin = sl.multiselect(
                "Select State", options=continent, default=continent
            )
        else:
            contin = sl.selectbox("Select State", options=continent)

        
        # data = data[data["ContinentName"].isin(contin)]
        # promotion = data["PromotionName"].unique()
        years = sl.multiselect("Select Year", options=year, default=year)
        # promo = sl.multiselect("Select Promo", options=promotion, default=promotion[1])

    # filt_data = data.query("ContinentName == @contin")
    filtered_data = data.query("States == @contin & Year == @years")

    # ======= Display Snapshots of sales =========
    gsales,  trans, act_trans = sl.columns(3)
    # gsales.metric(label="**Gross Sales**", value=millify(gross_sales, precision=2))
    if checked:
        reference = None
    else:
        reference = get_reference(years, contin, data, "SaleAmount")
       

    with gsales:
        plot_gsales_metric(
            label="Gross Revenue",
            data=filtered_data,
            suffix=" €",
            color_graph="rgba(0, 104, 201, 0.2)",
            reference=reference,
        )
    
    # trans.metric(label="**Total Transactions**", value=millify(num_trans))
    with trans:
        plot_trans_metric(
            label="Total Transactions",
            data=filtered_data,
            show_bar=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    # act_trans.metric(label="**Actual Transactions**", value=millify(actual_trans))
    with act_trans:
        plot_actual_trans_metric(
            label="Actual Transactions",
            data=filtered_data,
            show_bar=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    "---"
    # with sl.expander("Data Preview"):
    # sl.dataframe(
    #     filtered_data,
    #     column_config={
    #         "Year": sl.column_config.NumberColumn(format="%d"),
    #         "SalesKey": sl.column_config.NumberColumn(format="%d"),
    #     },
    # )
    # sl.write(refs)
    # ========= Display Charts ==================
    top_left, center, top_right = sl.columns(3)
    with top_left:
        plot_transact_by_day(filtered_data)

    with center:
        plot_sales_by_day(filtered_data)

    with top_right:
        plot_sales_by_month(filtered_data)

    bottom_left, bottom_right = sl.columns([2, 1])
    with bottom_left:
        plot_sales_by_category(filtered_data)
    with bottom_right:
        plot_sales_by_channel(filtered_data)
elif selected == "Profit":
    with sl.sidebar:
        year = data["Year"].unique()
        year.sort()
        continent = data["States"].unique()
        continent.sort()

        sl.header("Apply Filter")
        checked = sl.checkbox("Check this box to select multiple continents")

        if checked:
            contin = sl.multiselect(
                "Select Continent", options=continent, default=continent
            )
        else:
            contin = sl.selectbox("Select Continent", options=continent)
        # data = data[data["ContinentName"].isin(contin)]
        # promotion = data["PromotionName"].unique()
        years = sl.multiselect("Select Year", options=year, default=year)
        # promo = sl.multiselect("Select Promo", options=promotion, default=promotion[1])

    # filt_data = data.query("ContinentName == @contin")
    filtered_data = data.query("States == @contin & Year == @years")

    left_col, right_col = sl.columns([2, 1])
    if checked:
        reference = None
    else:
        reference = get_reference(years, contin, data, "ProfitAmount")

    with left_col:
        tprofit, pmargin = sl.columns(2)
        with tprofit:
            plot_profit_metric(
                "Total Profit",
                data=filtered_data,
                show_bar=False,
                prefix="$",
                color_graph="rgba(3,218,198,0.1)",
                reference=reference,
            )
        with pmargin:
            plot_profitmargin_metric(
                "Profit Margin", data=filtered_data, show_graph=False, suffix="%"
            )
        "---"

        plot_profit_by_month(filtered_data)
    with right_col:
        plot_profit_by_category(filtered_data)
        plot_profit_by_product(filtered_data)
elif selected == "forecasting":
    
   # Title
    sl.title("ARIMA Model Results Dashboard")

    # Data Upload Section
    uploaded_file = sl.file_uploader("Upload a CSV file with time series data", type="csv")
    if uploaded_file:
        data = pd.read_csv(uploaded_file, parse_dates=['DateKey'])
        sl.write("Data Preview:", data)

        # User Input for ARIMA Parameters
        p = sl.sidebar.number_input("Select Max p (AR term)", min_value=0, value=1)
        d = sl.sidebar.number_input("Select d (Differencing order)", min_value=0, value=1)
        q = sl.sidebar.number_input("Select Max q (MA term)", min_value=0, value=1)

        # Fitting the ARIMA Model
        if sl.button("Fit ARIMA Model"):
            # Aggregate sales by date
            df_daily = data.groupby('DateKey').agg({'SalesQuantity': 'sum'}).reset_index()

            # Determine the number of differences needed
            d = ndiffs(df_daily['SalesQuantity'], alpha=0.05, test='kpss')

            model = auto_arima(df_daily['SalesQuantity'], d=d, seasonal=False,
                    error_action='ignore', suppress_warnings=True,
                    start_p=1, max_p=p, start_q=1, max_q=q, stepwise=True)

            # Check if model fitting was successful
            if model != None:
                sl.success("Model fitted successfully!")
                n_steps = 10
                # Générer les dates futures
                future_dates = pd.date_range(start=df_daily['DateKey'].max() + pd.Timedelta(days=1),
                            periods=n_steps, 
                            freq='D')
                future_df = pd.DataFrame({'DateKey': future_dates})

                # Forecast
                forecast, conf_int = model.predict(n_steps=n_steps, return_conf_int=True)
                print(forecast)
                # Check forecast and confidence intervals length
                if len(forecast) == n_steps and conf_int.shape[0] == n_steps:
                    future_df['SalesQuantity'] = forecast
                    future_df['Lower'] = conf_int[:, 0]
                    future_df['Upper'] = conf_int[:, 1]
                else:
                    sl.error(f"Expected forecast length of {n_steps}, but got {len(forecast)} for forecast and {conf_int.shape[0]} for confidence intervals.")

            else:
                sl.error("Model fitting failed!")
            # Output model summary
            sl.subheader("Model Summary")
            sl.text(model.summary())


            # Create an interactive plot using Plotly
            fig = go.Figure()

            # Add historical data
            fig.add_trace(go.Scatter(x=df_daily['DateKey'], y=df_daily['SalesQuantity'],
                                    mode='lines+markers', name='Historical Data', 
                                    line=dict(color='blue')))

            # Add forecast data
            fig.add_trace(go.Scatter(x=future_df['DateKey'], y=forecast,
                                    mode='lines+markers', name='Forecast', 
                                    line=dict(color='orange')))

            # Add confidence interval
            fig.add_trace(go.Scatter(x=future_df['DateKey'], y=future_df['Lower'],
                                    mode='lines', name='Lower Bound',
                                    line=dict(color='gray', dash='dash')))
            fig.add_trace(go.Scatter(x=future_df['DateKey'], y=future_df['Upper'],
                                    mode='lines', name='Upper Bound',
                                    line=dict(color='gray', dash='dash')))

            # Update layout
            fig.update_layout(title='ARIMA Forecast',
                            xaxis_title='Date',
                            yaxis_title='Sales Quantity',
                            hovermode='x unified')

            # Display the plot in Streamlit
            sl.plotly_chart(fig)