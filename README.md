# Global Warming Effects on Ice Thickness

Members:
- Jayme Gordon
- Mo Garoub 
- Sasha Babicki
- Syad Khan 

Data analysis project for DSCI 522: Data Science Workflows

## About

We are trying to answer the question, did the median ice thickness in the Canadian Arctic change by a statistically significant amount from the years 1984 to 1996? This question stems from the rising global temperatures and a curiosity of how this warming impacts the depth of the ice. The dataset used in this analysis contains measurements of ice thickness at various established monitoring stations in the Canadian Arctic on a weekly basis. Using exploratory data analysis (EDA) we determined that the data are skewed. We decided to use a hypothesis test for independence of a difference in medians using permutation for our analysis.

The dataset used in this analysis contains measurements of ice thickness at various  established monitoring stations in the Canadian Arctic on a weekly basis. The data is made available from the Government of Canada and the monitoring is done by the Canadian Ice Thickness Program. Information about the program can be accessed through the Government of Canada and the specific dataset we are using is publicly available [here](https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls).


## Summary Report

The summary report can be found [here](https://github.com/UBC-MDS/global_warming_effects_on_ice_thickness/blob/main/doc/global_warming_effects_on_ice_thickness.pdf). 


## Usage

To replicate the analysis, clone this GitHub repository, install all the dependencies listed under the "Dependencies" header. 

Python dependencies can be installed using the conda environment file provided in the [522_grp_13.yaml](https://github.com/UBC-MDS/global_warming_effects_on_ice_thickness/blob/main/522_grp_13.yaml). To create and activate the environment, run the following commands in the command line from the root directory of this project:

```shell
conda env create --file 522_grp_13.yaml
conda activate 522_grp_13
```

R dependencies can be installed by running the following command in the R terminal:

```r
install.packages(c("tidyverse", "dplyr", "datateachr", "infer", "ggplot2", "purrr", "knitr", "docopt", "svglite", "rmarkdown"))
``` 

Once dependencies are installed, run the following command at the command line from the root directory of this project:

```shell
make all
```

To reset the repo to a clean state, with no intermediate or results files, run the following command at the command line from the root directory of this project:

```shell
make clean
```

## Dependencies

  - Python 3.8.0 and Python packages:
      - pandas=1.1.4
      - ipykernel=5.3.4
      - xlrd=1.2.0
      - docopt=0.6.2
      - altair=4.1.0
      - pandas-profiling=2.9.0
      - pytest=6.1.2
      - altair_saver=0.5.0
      - vega_datasets=0.9.0 
      - python-chromedriver-binary=88.0.*
      
  - R 4.0.3 and R libraries:
      - tidyverse=1.3.0
      - dplyr=1.0.2
      - datateachr=0.2.1
      - infer=0.5.3
      - ggplot2=3.3.2
      - purrr=0.3.4
      - knitr=1.30
      - docopt=0.7.1
      - svglite=1.2.3.2

## License

The Ice Thickness Program Collection, 1947-2002 data contains information licensed under the [Open Government Licence – Canada (version 2.0)](https://open.canada.ca/en/open-government-licence-canada).

# References

Government of Canada (2020). Ice thickness data. Retrieved from: https://www.canada.ca/en/environment-climate-change/services/ice-forecasts-observations/latest-conditions/archive-overview/thickness-data.html 
  
Timbers, T. (2020). DSCI 522 Statistical Inference and Computation I. Retrieved from: https://github.ubc.ca/MDS-2020-21/DSCI_552_stat-inf-1_students

<div id="refs" class="references">

  <div id="ref-___">
 </div>

</div>
