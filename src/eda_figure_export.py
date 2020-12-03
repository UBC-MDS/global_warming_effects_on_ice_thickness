#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Syad Khan
# date: 2020-11-27

"""This script reads processed data from a specified input filepath and produces EDA figures to
to a specificed output filepaths
Usage: eda_figure_export.py <input_path> <output_path_results> <output_path_eda>

Options:
<input_path>                Path to the input data file
<output_path_results>       Path to save figures to for report
<output_path_eda>           Path to save figures to for eda notebook
"""

import pandas as pd
import altair as alt
from docopt import docopt
from altair_saver import save
import chromedriver_binary

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
    
    # third figure - boxplot of mean ice thickness
    month_boxplot = alt.Chart(df, 
                              title="Mean Ice Thickness by Month").mark_boxplot().encode(
        y=alt.Y("mean_ice_thickness", title="Ice Thickness (cm)"),
        x=alt.X("month", title="Month"),
        tooltip=["mean_ice_thickness", "month", "station_name"])
    
    # fourth figure - distribution of icet hickness over time (monthly)
    ice_histogram = alt.Chart(df, 
                              title="Ice thickness measurements over all time").mark_bar().encode(
        x = alt.X("mean_ice_thickness", title="Ice Thickness (cm)", bin=alt.Bin(maxbins=40)),
        y = alt.Y("count()", title="Number of measurements"), 
        ).properties(
            width=150,
            height=150
        ).facet(
                "month",
                columns=4)
    
    return(mean_thickness_year, density, month_boxplot, ice_histogram)
      
def save_figures(figure1, figure2, figure3, figure4, output_path_results, output_path_eda):
    """Input Altair figures
    
    Parameters
    ----------
    figure1, figure2, figure3, figure4 : Altair.Chart
        Altair charts to be saved
    """
    # results folder
    # save figure 1 to eda
    figure_1_path = output_path_results + '/median_thickness_year.svg'
    try:
        save(figure1, figure_1_path)
    except:
        print(f"Figure 1 could not be saved at {figure_1_path}")
    
    # save figure 2 to eda
    figure_2_path = output_path_results + '/density.svg'
    try:
        save(figure2, figure_2_path)  
    except:
        print(f"Figure 2 could not be saved at {figure_2_path}")
    
    
    # eda folder
    # save figure 1 to eda
    figure_1_path = output_path_eda + '/median_thickness_year.svg'
    try:
        save(figure1, figure_1_path)
    except:
        print(f"Figure 1 could not be saved at {figure_1_path}")
    
    # save figure 2 to eda
    figure_2_path = output_path_eda + '/density.svg'
    try:
        save(figure2, figure_2_path)  
    except:
        print(f"Figure 2 could not be saved at {figure_2_path}")
        
     # save figure 3 to eda
    figure_3_path = output_path_eda + '/month_boxplot.svg'
    try:
        save(figure3, figure_3_path)  
    except:
        print(f"Figure 3 could not be saved at {figure_3_path}")
        
    # save figure 4 to eda
    figure_4_path = output_path_eda + '/ice_histogram.svg'
    try:
        save(figure4, figure_4_path)  
    except:
        print(f"Figure 4 could not be saved at {figure_4_path}")
 
def main(input_path, output_path_results, output_path_eda):
    dataframe = read_data(input_path)
    figure1, figure2, figure3, figure4 = create_figures(dataframe)
    save_figures(figure1, figure2, figure3, figure4, output_path_results, output_path_eda)

if __name__ == "__main__":
    main(opt["<input_path>"], opt["<output_path_results>"], opt["<output_path_eda>"])

