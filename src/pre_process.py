# author: Sasha Babicki
# date: 2020-11-26

"""Read and process data from local filepath and save locally as csv.

Usage: pre_proccess.py --in_file=<in_file> --out_file=<out_file>

Options:
--in_file=<in_file>    The local path (including filename) of the input file
--out_file=<out_file>  The local path (including filename) of where to write the processed output file
"""

from docopt import docopt
import pandas as pd
import import_data

opt = docopt(__doc__)

DEFAULT_PATHS = {
    "in" : "../data/raw/ice_thickness.csv",
    "out" :  "../data/processed/ice_thickness.csv"
}

def process_data(in_file = DEFAULT_PATHS["in"], out_file = DEFAULT_PATHS["out"]):
    """Read and process thickness data input_path, write to csv in output_path

    Parameters
    ----------
    in_file : str, optional
        filepath to download data, default in DEFAULT_PATHS
    out_file : str, optional
        filepath to save data, default in DEFAULT_PATHS
    """    

    try:
        df = import_data.read_file(in_file)
    except:
        print(f"File could not be read at: {in_file}")

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
    grouped_df = df_filtered.groupby(["station_id", "station_name", "month", "year"]).mean()
    grouped_df = grouped_df.reset_index()
    grouped_df = df_filtered[["station_id", "station_name", "month", "year", "ice_thickness"]]
    
    try: 
        grouped_df.to_csv(out_file, index=False)
    except: 
        print(f"File could not be saved at: {out_file}")
        
    return grouped_df

if __name__ == "__main__":
    
    process_data(opt["--in_file"], opt["--out_file"])