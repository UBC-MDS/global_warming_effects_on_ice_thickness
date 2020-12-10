# author: Sasha Babicki
# date: 2020-11-26

"""Read and process data from local filepath and save locally as csv.

Usage: pre_proccess.py --input_file=<input_file> --output_file=<output_file>

Options:
--input_file=<input_file>    The local path (including filename) of the input file
--output_file=<output_file>  The local path (including filename) of where to write the processed output file
"""
from pathlib import Path

import pandas as pd
from docopt import docopt

from __init__ import getlog

opt = docopt(__doc__)
log = getlog(__file__)

DEFAULT_PATHS = {
    "in" : "../data/raw/ice_thickness.csv",
    "out" :  "../data/processed/ice_thickness.csv"
}

def process_data(input_file = DEFAULT_PATHS["in"], output_file = DEFAULT_PATHS["out"]):
    """Read and process thickness data input_path, write to csv in output_path

    Parameters
    ----------
    input_file : str, optional
        filepath to download data, default in DEFAULT_PATHS
    output_file : str, optional
        filepath to save data, default in DEFAULT_PATHS
    """    

    try:
        df = pd.read_csv(input_file)
        log.info(f'loaded dataframe with shape: {df.shape}')
    except:
        log.error(f'File could not be read at: {input_file}')
        raise

    df_filtered = df.copy()
    df_filtered['Date'] = pd.DatetimeIndex(df_filtered['Date'])
    
    df_filtered = df_filtered.rename(columns={
        "StationID/ID de station" : "station_id", 
        "Station Name/Nom de station" : "station_name", 
        "Date" : "date", 
        "Ice Thickness/Épaisseur de la glace" : "ice_thickness",
        "Snow depth/Profondeur de la neige" : "snow_depth",
        "Measurement Method/Méthode de mesure" : "measurement_method",
        "Surface Topology/Topographie de la surface" : "surface_topology",
        "Cracks and Leads/Fissures et chenaux" : "cracks_leads"
    })

    df_filtered = df_filtered[df_filtered["measurement_method"] == 1]
    df_filtered = df_filtered[df_filtered["ice_thickness"] > 0]
    df_filtered["month"] = df_filtered["date"].dt.month
    df_filtered["year"] = df_filtered["date"].dt.year
    grouped_df = df_filtered.groupby(["station_id", "station_name", "month", "year"]) \
        .agg(mean_ice_thickness=("ice_thickness", "mean")) \
        .reset_index()

    grouped_df = grouped_df[["station_id", "station_name", "month", "year", "mean_ice_thickness"]]
    
    try:
        p = Path(output_file)
        if not p.parent.exists():
            p.parent.mkdir(parents=True)
            
        grouped_df.to_csv(output_file, index=False)
        log.info(f'Successfully pre-processed df to shape: {grouped_df.shape}')
    except: 
        log.error(f"File could not be saved at: {output_file}")
        raise
        
    return grouped_df

if __name__ == "__main__":
    
    process_data(opt["--input_file"], opt["--output_file"])