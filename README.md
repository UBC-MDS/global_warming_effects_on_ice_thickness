# Global Warming Effects on Ice Thickness

Members:
- Jayme Gordon
- Mo Garoub 
- Sasha Babicki
- Syad Khan 

Data analysis project for DSCI 522 (Data Science workflows)

## About

WWe are trying to answer the question, did the median ice thickness in the Canadian Arctic change by a statistically significant amount from the years 1984 to 1996? This question stems from the rising global temperatures and a curiosity of how this warming impacts the depth of the ice. The dataset used in this analysis contains measurements of ice thickness at various established monitoring stations in the Canadian Arctic on a weekly basis. Using exploratory data analysis (EDA) we determined that the data are skewed. We decided to use a hypothesis test for independence of a difference in medians using permutation for our analysis.

The dataset used in this analysis contains measurements of ice thickness at various  established monitoring stations in the Canadian Arctic on a weekly basis. The data is made available from the Government of Canada and the monitoring is done by the Canadian Ice Thickness Program. Information about the program can be accessed through the Government of Canada and the specific dataset we are using is publicly available [here](https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls).


## Summary Report

The summary report can be found here. 


## Usage

To replicate this analysis:
1. Run the entry script `import_.py`:
```shell
python src/import_data.py --url="https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls" --out_path="data/raw"
```

2. Process the file with `pre_process.py`:
```shell
python src/pre_process.py --in_file="data/raw/ice_thickness.csv" --out_file="data/processed/ice_thickness.csv"
```

3. Generate EDA figures using `eda_figure_export.py`: 
```shell
python src/eda_figure_export.py "data/processed/ice_thickness.csv" "results/"
```

4. Perform analysis and export figures using `ice_thickness_analysis.R`: 
```shell
Rscript src/ice_thickness_analysis.R  --dir_in="data/processed/ice_thickness.csv"  --dir_out="results/"
```

## Dependencies

  - Python 3.8.0 and Python packages:
      - docopt==0.6.2
      - pandas
      - ipykernel
      - xlrd
      - docopt
      - altair
      - pandas-profiling
      - pytest
      - altair_saver
      - chromedriver_binary
  - R 4.0.3 and R libraries:
      - tidyverse
      - dplyr
      - datateachr
      - infer
      - ggplot2
      - purrr
      - knitr
      - docopt

## License

The Ice Thickness Program Collection, 1947-2002 data contains information licensed under the [Open Government Licence – Canada (version 2.0)](https://open.canada.ca/en/open-government-licence-canada).

# References

<div id="refs" class="references">

  <div id="ref-___">
Government of Canada (2020). Ice thickness data. Retrieved from: https://www.canada.ca/en/environment-climate-change/services/ice-forecasts-observations/latest-conditions/archive-overview/thickness-data.html 
  

Timbers, T. (2020). DSCI 522 Statistical Inference and Computation I. Retreved from: https://github.ubc.ca/MDS-2020-21/DSCI_552_stat-inf-1_students

  </div>

</div>
