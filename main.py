# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 20:37:10 2022

@author: Ronald Nyasha Kanyepi
@email : kanyepironald@gmail.com
"""

import os
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import folium
import requests
from requests.exceptions import RequestException
import geocoder

def config():
    file_path = "./components/img/"
    try:
        img = Image.open(os.path.join(file_path, 'logo.ico'))
        st.set_page_config(page_title='GEO LOCATION APP', page_icon=img, layout="wide", initial_sidebar_state="expanded")
    except:
        st.set_page_config(page_title='GEO LOCATION APP', layout="wide", initial_sidebar_state="expanded")

    # Hide main menu and footer
    st.markdown("""
        <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>
    """, unsafe_allow_html=True)


def get_geolocation():
    try:
        # First try external IP API
        key = "1c5f04e925bc4b40b4c83b04175e321e"
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={key}")
        data = response.json()
        if "latitude" in data and "longitude" in data:
            return data
        else:
            raise ValueError("Incomplete data from IP API")
    except RequestException:
        st.warning("IP API failed. Falling back to geocoder...")
        g = geocoder.ip('me')
        return {
            "ip": g.ip,
            "latitude": g.latlng[0],
            "longitude": g.latlng[1],
            "city": g.city,
            "state_prov": g.state,
            "district": "N/A",
            "calling_code": "N/A",
            "country_name": g.country,
            "country_flag": "https://flagcdn.com/256x192/in.png",
            "currency": {"code": "N/A", "name": "N/A", "symbol": "N/A"},
            "isp": "N/A",
            "connection_type": "N/A",
            "organization": "N/A",
            "time_zone": {"name": "N/A", "offset": "N/A"}
        }

def other_tab():
    st.header("Other TAB")

def home():
    try:
        with st.spinner("Please wait, your request is being processed..."):
            response = get_geolocation()
            st.header("IP Geolocation App 🕵️‍♂️")
            col1, col2 = st.columns([8, 4])

            with col1:
                m = folium.Map(location=[response["latitude"], response["longitude"]], zoom_start=16)
                tooltip = "Approximate Location"
                folium.Marker(
                    [response["latitude"], response["longitude"]],
                    popup="You are here", tooltip=tooltip
                ).add_to(m)
                st_folium(m, width=500, height=400)

            with col2:
                st.markdown(f"""
                    <table>
                        <thead><th>Data</th><th>Value</th></thead>
                        <tr><td>IP Address</td><td>{response["ip"]}</td></tr>
                        <tr><td>City</td><td>{response["city"]}</td></tr>
                        <tr><td>District</td><td>{response["district"]}</td></tr>
                        <tr><td>Province</td><td>{response["state_prov"]}</td></tr>
                        <tr><td>Calling Code</td><td>{response["calling_code"]}</td></tr>
                        <tr><td>Latitude</td><td>{response["latitude"]}</td></tr>
                        <tr><td>Longitude</td><td>{response["longitude"]}</td></tr>
                        <tr><td>Country</td>
                            <td><img src="{response['country_flag']}" style="width:30%;max-width:40%">
                            {response["country_name"]}</td></tr>
                    </table>
                """, unsafe_allow_html=True)

            with st.expander("More Information regarding this IP"):
                st.subheader("Currency")
                df = pd.DataFrame.from_dict(response["currency"], orient="index", dtype=str, columns=['Value'])
                st.write(df)
                st.subheader("ISP")
                st.write("ISP:", response["isp"])
                st.write("Connection Type:", response["connection_type"])
                st.write("Organization:", response["organization"])
                st.subheader("TimeZone")
                df_1 = pd.DataFrame.from_dict(response["time_zone"], orient="index", dtype=str, columns=['Value'])
                st.write(df_1)

            st.success("Location fetched successfully!")
            st.balloons()

    except Exception as e:
        st.error(f"The app has failed to connect. Error: {e}")

def main():
    config()
    with st.sidebar:
        choice = option_menu("Main Menu", ["Home", 'Other Tab'], icons=['house', 'list-task'], menu_icon="cast", default_index=0)

    if choice == "Home":
        home()
    else:
        other_tab()

if __name__ == '__main__':
    main()
