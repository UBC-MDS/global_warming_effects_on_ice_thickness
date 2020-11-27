#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:29:53 2020

@author: syad
"""
import pandas as pd
import altair as alt
#alt.renderers.enable('altair_viewer')
#alt.data_transformers.disable_max_rows()

df = pd.read_csv('../data/processed/ice_thickness.csv')
df = df.groupby(["station_id", "station_name", "month", "year"]).mean().reset_index()

mean_thickness_year = alt.Chart(df).mark_bar(size=16).encode(
        y = alt.Y("median(ice_thickness)", title="Median Ice Thickness (cm)"),
        x = alt.X("year:O", title="Year")
    ).properties(
        background='white', title='Median Ice Thickness over Time'
    )
mean_thickness_year


(alt.Chart(df.query('(year == 1996 | year == 1984) & month == 2')).transform_density(
    'ice_thickness',
    groupby = ['year'],
    as_=['ice_thickness','density']
    )
 .mark_area(opacity=0.4).encode(
     x=alt.X('ice_thickness', title="Ice Thickness (cm)"),
     y=alt.Y('density:Q', title="Density of Observations"),
     color=alt.Color('year:O', scale=alt.Scale(scheme="set1")))
 .properties(
        background='white', title='Distribution of Ice Thickness for Analysis Month'
    ))
