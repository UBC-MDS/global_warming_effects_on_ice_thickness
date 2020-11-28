#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script takes in a filepath.
This script outputs figures
Usage: test.py <var1> --figure1=<figure1> --figure2=<figure2>

Options:
<var1>       Path to the data file
--figure1=<figure1>
--figure2=<figure2>
"""

import pandas as pd
import altair as alt
from docopt import docopt
from altair_saver import save
#from selenium import webdriver
import chromedriver_binary
#driver = webdriver.Chrome()

opt = docopt(__doc__)

def main(input_path, figure1, figure2):
    # read in data
    df = pd.read_csv(input_path)
    #df = df.groupby(["station_id", "station_name", "month", "year"]).mean().reset_index()
    
    # first plot of mean thickness by year
    mean_thickness_year = (alt.Chart(df).mark_bar(size=16).encode(
        y = alt.Y("median(mean_ice_thickness)", title="Median Ice Thickness Averages(cm)"),
        x = alt.X("year:O", title="Year"))
    .properties(
        background='white', title='Median Ice Thickness over Time'
    ))
    
    
    # prepare dataframe for facetted (monthly) density plot
    df_density = df.query('(year in [1984,1996]) & (month in [1,2,3])')
    month_names = {1: "January", 2:"February", 3:"March"}
    df_density = df_density.replace({"month":month_names})
    # second plot of thickness dsitribution for analysis years
    density = (alt.Chart(df_density)
    .transform_density(
    'mean_ice_thickness',
    groupby = ['year', 'month'],
    as_=['mean_ice_thickness','density']
    )
    .mark_area(opacity=0.4).encode(
       x=alt.X('mean_ice_thickness:Q', title="Ice Thickness (cm)"),
       y=alt.Y('density:Q', title="Density of Observations"),
       color=alt.Color('year:O', scale=alt.Scale(scheme="set1")))
    .facet(column=alt.Row("month",
                          title='Distribution of Ice Thickness by Month',
                          sort=['January','February','March']), 
           background='white'))
    
    # save files
    save(mean_thickness_year, figure1)
    save(density, figure2)
        
if __name__ == "__main__":
    main(opt["<var1>"], opt["--figure1"], opt["--figure2"])
    
