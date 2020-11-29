#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Syad Khan
# date: 2020-11-27

"""This script reads processed data from a specified input filepath and produces EDA figures to
to a specificed output filepath
Usage: eda_figure_export.py <input_path> <output_path>

Options:
<input_path>        Path to the input data file
<output_path>       Path to save figures to
"""

import pandas as pd
import altair as alt
from docopt import docopt
from altair_saver import save
#from selenium import webdriver
import chromedriver_binary
#driver = webdriver.Chrome()

opt = docopt(__doc__)

def read_data(input_path):
    """Read in preprocessed data from input_path, output as a pandas dataframe
    
    Parameters
    ----------
    input_path : str
        filepath to read data from
    """
    
    try:
        df = pd.read_csv(input_path)
    except:
        print(f"File could not be read from: {input_path}")
        
    return(df)

def create_figures(df):
    """Input a pandas dataframe and output Altair plots
    
    Parameters
    ----------
    df : pandas.DataFrame
        processed DataFrame used to create figures
    """
    
    # first figure of mean thickness by year - bar plot
    mean_thickness_year = (alt.Chart(df).mark_bar(size=16).encode(
        y = alt.Y("median(mean_ice_thickness)", title="Median Ice Thickness Averages(cm)"),
        x = alt.X("year:O", title="Year"))
    .properties(background='white', 
                title='Median Ice Thickness over Time'))
    
    
    # second figure of thickness dsitribution for analysis years 
    # prepare dataframe for facetted (monthly) density plot
    df_density = df.query('(year in [1984,1996]) & (month in [1,2,3])')
    month_names = {1: "January", 2:"February", 3:"March"}
    df_density = df_density.replace({"month":month_names})
    
    # create figure
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
    
    return(mean_thickness_year, density)
      
def save_figures(figure1, figure2, output_path):
    """Input Altair figures
    
    Parameters
    ----------
    figure1, figure2 : Altair.Chart
        Altair charts to be saved
    """
    
    # save figure 1
    figure_1_path = output_path + '/median_thickness_year.png'
    try:
        save(figure1, figure_1_path)
    except:
        print(f"Figure 1 could not be saved at {figure_1_path}")
        
    # save figure 2
    figure_2_path = output_path + '/density.png'
    try:
        save(figure2, figure_2_path)  
    except:
        print(f"Figure 2 could not be saved at {figure_2_path}")
 
def main(input_path, output_path):
    dataframe = read_data(input_path)
    figure1, figure2 = create_figures(dataframe)
    save_figures(figure1, figure2, output_path)

if __name__ == "__main__":
    main(opt["<input_path>"], opt["<output_path>"])

