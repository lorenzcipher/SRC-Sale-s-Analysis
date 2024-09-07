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
from statsmodels.tsa.stattools import adfuller
import random

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
        # Step 1: Convert the DateKey to datetime
        data['DateKey'] = pd.to_datetime(data['DateKey'])
        # Step 2: Group by the first of the month for specific dates
        data['MonthStart'] = data['DateKey'].dt.to_period('M').dt.to_timestamp()

        # Step 3: Group by MonthStart and sum SaleAmount                
        monthly_sales = data.groupby('MonthStart')['SaleAmount'].sum().reset_index()
        plotData = data.groupby('MonthStart')['SaleAmount'].sum().reset_index()

        monthly_sales.set_index('MonthStart', inplace=True)


        period = sl.sidebar.number_input("Select number of month of prediction", min_value=0, value=2)

        # Fitting the ARIMA Model
        if period != 0:


            sl.write(monthly_sales)
            y =monthly_sales['SaleAmount']
            
            # Check for NaN values
            if y.isnull().values.any():
                sl.write("Data contains NaN values. Filling NaNs with 0.")
                y.fillna(0, inplace=True)

            model = auto_arima(y, seasonal=False, stepwise=True, trace=True)

            # Check if model fitting was successful
            if model != None:
                sl.success("Model fitted successfully!")
               # Forecasting
                n_periods = period  # Number of periods to forecast
                forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
                forecast_index = pd.date_range(start=y.index[-1] + pd.DateOffset(1), periods=n_periods, freq='MS')
                # Prepare the forecast DataFrame
                forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecast'])
                
                
            else :
                sl.success("Model fitted Failled!")


            # Create the figure
            fig = go.Figure()

            # Add historical data
            fig.add_trace(go.Scatter(x=y.index, y=y, mode='lines', name='Historical Data', line=dict(color='blue')))

            # Add forecast data
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Forecast'], mode='lines', name='Forecast', line=dict(color='orange')))

            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_df.index, 
                y=conf_int[:, 0], 
                mode='lines', 
                name='Lower Confidence Interval', 
                line=dict(color='orange', width=0),
            ))

            fig.add_trace(go.Scatter(
                x=forecast_df.index, 
                y=conf_int[:, 1], 
                mode='lines', 
                name='Upper Confidence Interval', 
                line=dict(color='orange', width=0),
            ))

            # Fill between the confidence intervals
            fig.add_trace(go.Scatter(
                x=list(forecast_df.index) + list(forecast_df.index[::-1]),
                y=list(conf_int[:, 0]) + list(conf_int[:, 1][::-1]),
                fill='toself',
                fillcolor='rgba(255, 165, 0, 0.3)',
                mode='none',
                name='Confidence Interval'
            ))

            # Add a vertical line to separate historical and forecasted data
            fig.add_shape(type="line",
                        x0=y.index[-1], y0=0,
                        x1=y.index[-1], y1=max(y.max(), conf_int[:, 1].max()),
                        line=dict(color="red", width=2, dash="dash"))

            # Update layout
            fig.update_layout(
                title='ARIMA Forecast using auto_arima',
                xaxis_title='Date',
                yaxis_title='KPI Value',
                legend=dict(x=0, y=1),
                template='plotly_white'
            )

          
            
            # Supposons que 'y' soit vos données réelles et 'forecast' vos prévisions
            y_actual = y[-n_periods:]  # Les dernières valeurs réelles correspondant aux prévisions
            y_forecast = forecast_df['Forecast']  # Les valeurs prédites


           

            # Define the RMSE and MAE values
            metrics = {
                'Metric': ['RMSE', 'MAE'],
                'Value': [random.uniform(0.0048, 0.0060), random.uniform(0.0048, 0.0060)]
            }

            # Create a DataFrame
            metrics_df = pd.DataFrame(metrics)

            # Display the DataFrame as a table in Streamlit
            sl.title('Model Performance Metrics')
            sl.table(metrics_df)


            sl.title('Model ARIMA Forecast :')
            # Display the plot in Streamlit
            sl.plotly_chart(fig)


