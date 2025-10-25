import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import requests

def getMedicines(medName):
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_shopping",
        "q": medName,
        "api_key": "ynB5FW3YJVncGdhBztXJrtw2",
        "gl":"in",
    }
    response = requests.get(url, params=params)
    result=response.text
    result=json.loads(result)["shopping_results"]
    return result

def compareMedicines(shopingResults):
    lowestPrice=strToFloat(shopingResults[0]["price"])
    lowestPriceIndex=0
    index=0
    for i in shopingResults:
        price=strToFloat(i["price"])
        if(lowestPrice>price):
             lowestPrice=price
             lowestPriceIndex=index
             index+=1

def strToFloat(str):
    return float(str[1:].replace(",",""))


c1,c2=st.columns(2)
c1.image("poster.png",width=300)
c2.header("E-Pharmacy Price Comparison System")

st.sidebar.title("Enter Name Of Medicine:")
medName=st.sidebar.text_input("Enter Name Name Here:")
opnNo=st.sidebar.text_input("Enter Number Of Options Here:")

medData={
        "company":[],
        "price":[]
    }

if(medName is not None):
    if st.sidebar.button("Price Compare"):
        shopingResults=getMedicines(medName)
        lowestPrice=strToFloat(shopingResults[0]["price"])
        lowestPriceIndex=0
        for i in range(int(opnNo)):
            st.title(f"Option-{i+1}")

            c1,c2=st.columns(2)
            c1.write("Company :")
            c2.write(shopingResults[i]["seller"])

            c1.write("Title :")
            c2.write(shopingResults[i]["title"])

            c1.write("Price :")
            c2.write(shopingResults[i]["price"])
            
            url=shopingResults[i]["product_link"]
            c1.write("Buy Link :")
            c2.write("[Link](%s)"%url)
            price=strToFloat(shopingResults[i]["price"])
            medData["company"].append(shopingResults[i]["seller"])
            medData["price"].append(price)
            """----------------------------------------"""
            if(lowestPrice>price):
                lowestPrice=price
                lowestPriceIndex=i
        st.sidebar.image(shopingResults[lowestPriceIndex]["thumbnail"])
        
        st.title(f"Best Option-{lowestPriceIndex+1}")
        c1,c2=st.columns(2)
        c1.write("Company :")
        c2.write(shopingResults[lowestPriceIndex]["seller"])

        c1.write("Title :")
        c2.write(shopingResults[lowestPriceIndex]["title"])

        c1.write("Price :")
        c2.write(shopingResults[lowestPriceIndex]["price"])
            
        url=shopingResults[lowestPriceIndex]["product_link"]
        c1.write("Buy Link :")
        c2.write("[Link](%s)"%url)
        df=pd.DataFrame(medData)
        st.title("Chart Comparison :")
        st.bar_chart(df,x="company",y="price")

        fig,ax=plt.subplots()
        ax.pie(medData["price"],labels=medData["company"],shadow=True)
        ax.axis("equal")
        st.pyplot(fig)