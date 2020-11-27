import pandas as pd
import import_data

DEFAULT_PATHS = {
    "in" : "../data/raw/ice_thickness.csv",
    "out" :  "../data/processed/ice_thickness.csv"
}

def process_data(input_path = DEFAULT_PATHS["in"], output_path = DEFAULT_PATHS["out"]):
    """Read and process thickness data input_path, write to csv in output_path

    Parameters
    ----------
    input_path : str, optional
        filepath to download data, default in DEFAULT_PATHS
    output_path : str, optional
        filepath to save data, default in DEFAULT_PATHS
    """    
    try:
        df = import_data.load_data()
    except:
        import_data.download_data()
        df = import_data.load_data()

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
    
    try: 
        grouped_df.to_csv(output_path, index=False)
    except: 
        print(f"File could not be saved at: {output_path}")
        
    return grouped_df

process_data()