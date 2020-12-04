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

from pathlib import Path

import altair as alt
import pandas as pd
from altair_saver import save
from docopt import docopt

from __init__ import getlog

opt = docopt(__doc__)
log = getlog(__file__)

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
        log.error(f"File could not be read from: {input_path}")
        raise
        
    return df

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

def save_figures(figures : dict, save_dir : str, ext : str = 'svg'):
    """Save figure objs to specified path with extension

    Parameters
    ----------
    figures : dict
        dict of {name: Altair figure obj}
    save_dir : str
        root dir to save figures, eg save_dir / name.ext
    ext : str
        extension to save figures with
    """

    # create root dir if doesn't exist
    p_root = Path(save_dir)
    if not p_root.exists():
        p_root.mkdir(parents=True)
        log.info(f'Created dir: {p_root}')

    # loop input dict and save figs
    for name, fig in figures.items():
        p = p_root / f'{name}.{ext}'

        try:
            save(fig, str(p))
        except:
            log.error(f'Could not save figure at: {p}')
            raise # re raise error, don't continue if saving fig fails
 
def main(input_path, output_path_results, output_path_eda):
    df = read_data(input_path)
    figure1, figure2, figure3, figure4 = create_figures(df)

    # create dicts of {fig_name : fig_obj}
    m_results = dict(
        median_thickness_year=figure1,
        density=figure2)
    
    m_eda = dict(
        median_thickness_year=figure1,
        density=figure2,
        month_boxplot=figure3,
        ice_histogram=figure4)
    
    # save figs at specified paths
    ext = 'svg'
    save_figures(figures=m_results, save_dir=output_path_results, ext=ext)
    save_figures(figures=m_eda, save_dir=output_path_eda, ext=ext)

if __name__ == "__main__":
    main(
        input_path=opt["<input_path>"],
        output_path_results=opt["<output_path_results>"],
        output_path_eda=opt["<output_path_eda>"])
