
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title("ML-driven House Customization for Maximum Profit")
st.caption("MSCI 436 - Team 8")

#filtering
st.header("Filtered Data")
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    st.caption("To filter through the columns, select the columns you would like.")
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

df_ui = pd.read_csv('out.csv')
st.dataframe(filter_dataframe(df_ui))

#Graphs
st.header("Visualization")

#all features
st.subheader("All features")
st.caption("Showing the relationship between all the features and the house price.")
cols = df_ui.columns.tolist()[:-1]
st.line_chart(df_ui, x = "SalePrice", y = cols, )

#line graph
def line_graph():
  st.subheader("Line Graphs: Quality, Year, Area")
  st.caption("Showing the relationship between features of the house and the sale price.")
  tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Overall Quality", "Year Built",
                      "Year Remodel", "Total Basement SF", "Above Ground Sqft",
                      "Garage Area", "Wood Deck SF", "Open Porch SF"])
  with tab1:
   st.line_chart(df_ui, x = "OverallQual", y = "SalePrice")
   st.text("The overall quality of the house is measured from 1-10. As shown, as the overall\n quality increases, so does the price.")
  with tab2:
    st.line_chart(df_ui, x = "YearBuilt", y = "SalePrice")
    st.text("The graph shows the relationship between the year built and the house sale price.\n Indicating that the newer house prices are higher comapred to the houses built from\n 1900s-1950s.")
  with tab3:
    st.line_chart(df_ui, x = "YearRemodAdd", y = "SalePrice")
    st.text("The remodal year shows a position correlation towards the house sale price. As the\n remodal year becomes recent, the house sale price increases as well.")
  with tab4:
    st.line_chart(df_ui, x = "TotalBsmtSF", y = "SalePrice")
    st.text("As shown in the graph, the average total basement surface area is between\n 600-1700 sqft, with the average house price range being approximately $100k to $300k.")
  with tab5:
    st.line_chart(df_ui, x = "GrLivArea", y = "SalePrice")
    st.text("This graph shows a strong positive correlation between the above ground sqft and\n the house sale price.")
  with tab6:
    st.line_chart(df_ui, x = "GarageArea", y = "SalePrice")
    st.text("This graph shows the average garage area is between 600-850 sqft, with the highest\n price at $440,101 with 831 sqft.")
  with tab7:
    st.line_chart(df_ui, x = "WoodDeckSF", y = "SalePrice")
    st.text("The graph shows that the average wood deck surface area is approximately between\n 50-450 sqft.")
  with tab8:
    st.line_chart(df_ui, x = "OpenPorchSF", y = "SalePrice")
    st.text("")

line_graph()

#plots with values that can be controlled
def plot():
  st.subheader("Line Graphs: Total Rooms, Baths, Garage Cars, Fireplaces")
  tab1, tab2, tab3, tab4, tab5 = st.tabs(["Total Rooms Abv Ground", "Full Bath", "Half Bath",
                                   "Garage Cars", "Fireplaces"])
  with tab1:
    st.subheader("Line Graph - Total Rooms Abv Ground vs Sale price")
    st.caption("Showcasing the relationship between the total number of rooms above the ground and the house sale price.")
    df = pd.read_csv('out.csv')
    df['TotRmsAbvGrd'] = df['TotRmsAbvGrd'].astype(str)
    clist = df["TotRmsAbvGrd"].unique().tolist()
    total_rooms = st.multiselect("Select total number of rooms", clist)
    st.text("You selected: {}".format(", ".join(total_rooms)))
    dfs = {TotRmsAbvGrd: df[df["TotRmsAbvGrd"] == TotRmsAbvGrd] for TotRmsAbvGrd in total_rooms}
    fig = go.Figure()
    for TotRmsAbvGrd, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["TotRmsAbvGrd"], y=df["SalePrice"], name=TotRmsAbvGrd))
    st.plotly_chart(fig)

  with tab2:
    st.subheader("Line Graph - Full Bath vs Sale price")
    st.caption("Showcasing the relationship between the number of full baths and the house sale price.")
    df = pd.read_csv('out.csv')
    df['FullBath'] = df['FullBath'].astype(str)
    clist = df["FullBath"].unique().tolist()
    full_baths = st.multiselect("Select number of full baths", clist)
    st.text("You selected: {}".format(", ".join(full_baths)))
    dfs = {FullBath: df[df["FullBath"] == FullBath] for FullBath in full_baths}
    fig = go.Figure()
    for FullBath, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["FullBath"], y=df["SalePrice"], name=FullBath))
    st.plotly_chart(fig)

  with tab3:
    st.subheader("Line Graph - Half Bath vs Sale price")
    st.caption("Showcasing the relationship between the number of half baths and the house sale price.")
    df = pd.read_csv('out.csv')
    df['HalfBath'] = df['HalfBath'].astype(str)
    clist = df["HalfBath"].unique().tolist()
    half_baths = st.multiselect("Select number of half baths", clist)
    st.text("You selected: {}".format(", ".join(half_baths)))
    dfs = {HalfBath: df[df["HalfBath"] == HalfBath] for HalfBath in half_baths}
    fig = go.Figure()
    for HalfBath, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["HalfBath"], y=df["SalePrice"], name=HalfBath))
    st.plotly_chart(fig)

  with tab4:
    st.subheader("Line Graph - Garage Cars vs Sale price")
    st.caption("Showcasing the relationship between the number of cars that can fit in the garage and the house sale price.")
    df = pd.read_csv('out.csv')
    df['Fireplaces'] = df['Fireplaces'].astype(str)
    clist = df["Fireplaces"].unique().tolist()
    garage_cars = st.multiselect("Select number of cars", clist)
    st.text("You selected: {}".format(", ".join(garage_cars)))
    dfs = {GarageCars: df[df["GarageCars"] == GarageCars] for GarageCars in garage_cars}
    fig = go.Figure()
    for GarageCars, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["GarageCars"], y=df["SalePrice"], name=GarageCars))
    st.plotly_chart(fig)

  with tab5:
    st.subheader("Line Graph - Fireplaces vs Sale price")
    st.caption("Showcasing the relationship between the number of fireplaces and the house sale price.")
    df = pd.read_csv('out.csv')
    df['Fireplaces'] = df['Fireplaces'].astype(str)
    clist = df["Fireplaces"].unique().tolist()
    fireplaces = st.multiselect("Select number of fireplaces", clist)
    st.text("You selected: {}".format(", ".join(fireplaces)))
    dfs = {Fireplaces: df[df["Fireplaces"] == Fireplaces] for Fireplaces in fireplaces}
    fig = go.Figure()
    for Fireplaces, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["Fireplaces"], y=df["SalePrice"], name=Fireplaces))
    st.plotly_chart(fig)


plot()
