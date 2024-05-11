
import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns
import missingno as msno
import datetime as dt
import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from IPython.display import HTML

import sqlite3
con = sqlite3.connect('phonepe.db')
cursor=con.cursor()
con.commit


cursor.execute("SELECT * FROM aggregate_insurance")
con.commit()
table1 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

agg_insura = pd.DataFrame(table1,columns=columns)


cursor.execute("SELECT * FROM aggregate_transaction")
con.commit()
table2 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

agg_tran = pd.DataFrame(table2,columns=columns)

cursor.execute("SELECT * FROM aggregate_user")
con.commit()
table3 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

agg_userr = pd.DataFrame(table3,columns=columns)

cursor.execute("SELECT * FROM map_insurance")
con.commit()
table4 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

map_insura = pd.DataFrame(table4,columns=columns)

cursor.execute("SELECT * FROM map_transaction")
con.commit()
table5 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

map_tran = pd.DataFrame(table5,columns=columns)
map_tran=map_tran.rename(columns={'District' : 'Districts'})

cursor.execute("SELECT * FROM map_user")
con.commit()
table6 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

map_userr = pd.DataFrame(table6,columns=columns)

cursor.execute("SELECT * FROM top_insurance")
con.commit()
table7 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

top_insura = pd.DataFrame(table7,columns=columns)

cursor.execute("SELECT * FROM top_transaction")
con.commit()
table8 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

top_tran = pd.DataFrame(table8,columns=columns)

cursor.execute("SELECT * FROM top_user")
con.commit()
table9 = cursor.fetchall()

columns=[column[0] for column in cursor.description]

top_userr = pd.DataFrame(table9,columns=columns)


con.close()

def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Insurance_amount",title= f"{year} INSURANCE AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Insurance_count",title= f"{year} INSURANCE COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()


        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Insurance_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Insurance_amount"].min(),aiyg["Insurance_amount"].max()),
                                 hover_name= "States",title = f"{year} INSURANCE AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Insurance_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Insurance_count"].min(),aiyg["Insurance_count"].max()),
                                 hover_name= "States",title = f"{year} INSURANCE COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Insurance_amount",
                            title= f"{aiyq['Years'].min()} AND {quarter} quarter INSURANCE AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Insurance_count",
                            title= f"{aiyq['Years'].min()} AND {quarter} quarter INSURANCE COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Insurance_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Insurance_amount"].min(),aiyqg["Insurance_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} quarter INSURANCE AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Insurance_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Insurance_count"].min(),aiyqg["Insurance_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} quarter INSURANCE COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)

    return aiyq

def Aggre_trans_Y(df,year):
    tiy= df[df["Years"] == year]
    tiy.reset_index(drop= True, inplace= True)

    tiyg=tiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(tiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()


        fig_india_1= px.choropleth(tiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (tiyg["Transaction_amount"].min(),tiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (tiyg["Transaction_count"].min(),tiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)

    return tiy


def Aggre_trans_Y_Q(df,quarter):
    tiyq= df[df["Quarter"] == quarter]
    tiyq.reset_index(drop= True, inplace= True)

    tiyqg= tiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(tiyqg, x= "States", y= "Transaction_amount",
                            title= f"{tiyq['Years'].min()} AND {quarter} quarter TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(tiyqg, x= "States", y= "Transaction_count",
                            title= f"{tiyq['Years'].min()} AND {quarter} quarter TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(tiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (tiyqg["Transaction_amount"].min(),tiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{tiyq['Years'].min()} AND {quarter} quarter TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(tiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (tiyqg["Transaction_count"].min(),tiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{tiyq['Years'].min()} AND {quarter} quarter TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)

    return tiyq



def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)

def Aggre_user_plt_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plt_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plt_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plt_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)

        st.plotly_chart(fig_map_bar_1)

def map_insure_plt_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_amount",
                              width=500, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_count",
                              width=500, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)

        st.plotly_chart(fig_map_pie_1)

def map_user_plt_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plt_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plt_1)

    return muy

def map_user_plt_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plt_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plt_1)

    return muyq

def map_user_plt_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plt_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plt_1)

    with col2:
        fig_map_user_plt_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plt_2)

def top_user_plt_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plt_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plt_1)

    return tuy

def top_user_plt_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plt_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "RegisteredUser",hover_data="Districts",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plt_2)


def ques1():
    brand= agg_userr[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= agg_tran[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_tran[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_tran[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_userr[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_userr[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= agg_tran[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= agg_tran[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= agg_tran[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= map_tran[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


#st.set_option('suppress_callback_exceptions',True)

def main():
    st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")
    st.write("")

    with st.sidebar:
        select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])


    if select == "Home":

        col1,col2= st.columns(2)

        with col1:
            st.header("PHONEPE")
            st.subheader("INDIA'S BEST TRANSACTION APP")
            st.markdown("PhonePe  is an Indian digital payments and financial technology company")
            st.write("****FEATURES****")
            st.write("****Credit & Debit card linking****")
            st.write("****Bank Balance check****")
            st.write("****Money Storage****")
            st.write("****PIN Authorization****")

        col2,col3= st.columns(2)

        with col2:
            st.write("****Easy Transactions****")
            st.write("****One App For All Your Payments****")
            st.write("****Your Bank Account Is All You Need****")
            st.write("****Multiple Payment Modes****")
            st.write("****PhonePe Merchants****")
            st.write("****Multiple Ways To Pay****")
            st.write("****1.Direct Transfer & More****")
            st.write("****2.QR Code****")
            st.write("****Earn Great Rewards****")

        with col3:
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.write("****No Wallet Top-Up Required****")
            st.write("****Pay Directly From Any Bank To Any Bank A/C****")
            st.write("****Instantly & Free****")


    if select == "Data Exploration":
        tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

        with tab1:
            method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

            if method == "Insurance Analysis":
                col1,col2= st.columns(2)
                with col1:
                    agg_insura["Years"]=agg_insura["Years"].astype('int')
                    years= st.slider("**Select the Year**", agg_insura["Years"].min(), agg_insura["Years"].max(), agg_insura["Years"].min())

                df_agg_insur_Y= Aggre_insurance_Y(agg_insura,years)

                col1,col2= st.columns(2)
                with col1:
                    quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

                Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)


            elif method == "Transaction Analysis":
                col1,col2= st.columns(2)
                with col1:
                    agg_tran["Years"]=agg_tran["Years"].astype('int')
                    years_at= st.slider("**Select the Year**", agg_tran["Years"].min(), agg_tran["Years"].max(),agg_tran["Years"].min())

                df_agg_tran_Y= Aggre_trans_Y(agg_tran,years_at)

                col1,col2= st.columns(2)
                with col1:
                    quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

                df_agg_tran_Y_Q= Aggre_trans_Y_Q(df_agg_tran_Y, quarters_at)

                state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

                Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)


            elif method == "User Analysis":
                agg_userr["Years"]=agg_userr["Years"].astype('int')
                year_au= st.selectbox("Select the Year_AU",agg_userr["Years"].unique())
                agg_user_Y= Aggre_user_plt_1(agg_userr,year_au)

                quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
                agg_user_Y_Q= Aggre_user_plt_2(agg_user_Y,quarter_au)

                state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
                Aggre_user_plt_3(agg_user_Y_Q,state_au)

        with tab2:
            method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

            if method_map == "Map Insurance Analysis":
                map_insura["Years"]=map_insura["Years"].astype('int')
                col1,col2= st.columns(2)
                with col1:
                    years_m1= st.slider("**Select the Year_mi**", map_insura["Years"].min(), map_insura["Years"].max(),map_insura["Years"].min())

                df_map_insur_Y= Aggre_trans_Y(map_insura,years_m1)

                col1,col2= st.columns(2)
                with col1:
                    state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

                map_insure_plt_1(df_map_insur_Y,state_m1)

                col1,col2= st.columns(2)
                with col1:
                    quarters_m1= st.slider("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

                df_map_insur_Y_Q= Aggre_trans_Y_Q(df_map_insur_Y, quarters_m1)

                col1,col2= st.columns(2)
                with col1:
                    state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())

                map_insure_plt_2(df_map_insur_Y_Q, state_m2)

            elif method_map == "Map Transaction Analysis":
                col1,col2= st.columns(2)
                
                map_tran["Years"]=map_tran["Years"].astype('int')
                
                with col1:
                    years_m2= st.slider("**Select the Year_mi**", map_tran["Years"].min(), map_tran["Years"].max(),map_tran["Years"].min())

                df_map_tran_Y= Aggre_trans_Y(map_tran, years_m2)

                col1,col2= st.columns(2)
                with col1:
                    state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

                map_insure_plt_1(df_map_tran_Y,state_m3)

                col1,col2= st.columns(2)
                with col1:
                    quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

                df_map_tran_Y_Q= Aggre_trans_Y_Q(df_map_tran_Y, quarters_m2)

                col1,col2= st.columns(2)
                with col1:
                    state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())

                map_insure_plt_2(df_map_tran_Y_Q, state_m4)

            elif method_map == "Map User Analysis":
                col1,col2= st.columns(2)
                map_userr["Years"]=map_userr["Years"].astype('int')
                with col1:
                    year_mu1= st.selectbox("**Select the Year_mu**",map_userr["Years"].unique())
                map_user_Y= map_user_plt_1(map_userr, year_mu1)

                col1,col2= st.columns(2)
                with col1:
                    quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
                map_user_Y_Q= map_user_plt_2(map_user_Y,quarter_mu1)

                col1,col2= st.columns(2)
                with col1:
                    state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
                map_user_plt_3(map_user_Y_Q, state_mu1)

        with tab3:
            method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

            if method_top == "Top Insurance Analysis":
                top_insura["Years"]=top_insura["Years"].astype('int')
                col1,col2= st.columns(2)
                with col1:
                    years_t1= st.slider("**Select the Year_ti**", top_insura["Years"].min(), top_insura["Years"].max(),top_insura["Years"].min())

                df_top_insur_Y= Aggre_trans_Y(top_insura,years_t1)


                col1,col2= st.columns(2)
                with col1:
                    quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

                df_top_insur_Y_Q= Aggre_trans_Y_Q(df_top_insur_Y, quarters_t1)


            elif method_top == "Top Transaction Analysis":
                top_tran["Years"]=top_tran["Years"].astype('int')
                col1,col2= st.columns(2)
                with col1:
                    years_t2= st.slider("**Select the Year_tt**", top_tran["Years"].min(), top_tran["Years"].max(),top_tran["Years"].min())

                df_top_tran_Y= Aggre_trans_Y(top_tran,years_t2)


                col1,col2= st.columns(2)
                with col1:
                    quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

                df_top_tran_Y_Q= Aggre_trans_Y_Q(df_top_tran_Y, quarters_t2)

            elif method_top == "Top User Analysis":
                top_userr["Years"]=top_userr["Years"].astype('int')
                col1,col2= st.columns(2)
                with col1:
                    years_t3= st.selectbox("**Select the Year_tu**", top_userr["Years"].unique())

                df_top_user_Y= top_user_plt_1(top_userr,years_t3)

                col1,col2= st.columns(2)
                with col1:
                    state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

                df_top_user_Y_S= top_user_plt_2(df_top_user_Y,state_t3)

    if select == "Top Charts":
      ques= st.selectbox("select the question",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                    'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                    'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                  'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                  'Top 50 Districts With Lowest Transaction Amount'))
      if ques=="Top Brands Of Mobiles Used":
          ques1()

      elif ques=="States With Lowest Trasaction Amount":
          ques2()

      elif ques=="Districts With Highest Transaction Amount":
          ques3()

      elif ques=="Top 10 Districts With Lowest Transaction Amount":
          ques4()

      elif ques=="Top 10 States With AppOpens":
          ques5()

      elif ques=="Least 10 States With AppOpens":
          ques6()

      elif ques=="States With Lowest Trasaction Count":
          ques7()

      elif ques=="States With Highest Trasaction Count":
          ques8()

      elif ques=="States With Highest Trasaction Amount":
          ques9()

      elif ques=="Top 50 Districts With Lowest Transaction Amount":
          ques10()


if __name__== '__main__':
  main()
