#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:29:53 2020

@author: syad
"""
import pandas as pd
import altair as alt
alt.renderers.enable('altair_viewer')
alt.data_transformers.disable_max_rows()

#1984 - #1996

df = pd.read_csv('../data/processed/ice_thickness.csv')
df = df.groupby(["station_id", "station_name", "month", "year"]).mean().reset_index()

#df = df.iloc[0:500]

mean_thickness_year = alt.Chart(df).mark_bar(size=16).encode(
        y = alt.Y("median(ice_thickness)", title="Median Ice Thickness (cm)"),
        x = alt.X("year:O", title="Year")
    ).properties(
        background='white', title='Median Ice Thickness over Time'
    )


mean_thickness_year

#mean_thickness_year.save('filename.png')
#mean_thickness_year.save('chart.png')