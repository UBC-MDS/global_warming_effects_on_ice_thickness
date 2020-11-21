# Global Warming Effects on Ice Thickness

Members:
- Jayme Gordon
- Mo Garoub 
- Sasha Babicki
- Syad Khan 

Data analysis project for DSCI 522 (Data Science workflows)

## Project proposal

We are trying to answer the question, did the mean ice thickness in the Canadian Arctic change by a statistically significant amount from the years 1984 to 1996? 
This question stems from the rising global temperatures and a curiosity of how this warming impacts the depth of the ice. 
The dataset used in this analysis contains measurements of ice thickness at various  established monitoring stations in the Canadian Arctic on a weekly basis. The data is made available from the Government of Canada and the monitoring is done by the Canadian Ice Thickness Program. Information about the program can be accessed through the Government of Canadafrom this website,  and the specific dataset we are using is publicly available [here](https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls )

Ice thickness is measured to the nearest centinmetre using one of two methods: an auger kit or a hot wire ice thickness gauge. It contains data dating back to 1947; however, this data is sparse so it serves our analysis to only use measurements from 1984 onwards. Each row of the dataset contains information including Station ID, Date, and Ice Thickness among other variables. Data was collected weekly at various stations.

To answer the questions mentioned above, we will select a data sample from a specific range of time for each year, ensuring to use the same range for both 1984 and 1996. We want to avoid the situation where we take data from a warmer timeframe in one year and colder temperatures in another as this will not be a fair comparison. We will then use this sample to conduct a hypothesis test to determine whether the means of the ice thickness in 1984 and 1996 are the same or different. To share the results, we will create a visualization that compares the two distributions of data, paying particular attention to the means. Furthermore, we will report the difference between the mean values along with the specific estimates in a table.


To explore our dataset and help identify specific details that will be used in the analysis such as the date rate for each year, we will perform exploratory data analysis. Visualizations that show how many records we have for each station and which months or years are most populated with data will be helpful for determining whether the available dataset will allow us to answer our inferential question and help us decide on how to generate our samples. We will also need to parse through the measurements to identify possible outliers and determine whether these are errors with the reporting or if they should be kept in our sample. Furthermore, we will showcase general trends in ice thickness over time which will lead to more rigorous statistical analysis.


## Usage

To replicate this analysis:
1. Run the entry script `download.py`:
```py
# default no args
python -m download
```

```py
# specify download url and save directory
python -m download --save_dir /path/to/save_directory --url https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls
```

2. Run all cells in `/scr/ice_thickness_eda.ipynb`

## Dependencies

  - Python 3.7.3 and Python packages:
      - docopt==0.6.2

## License

The Ice Thickness Program Collection, 1947-2002 data contains information licensed under the [Open Government Licence – Canada (version 2.0)](https://open.canada.ca/en/open-government-licence-canada).

# References

<div id="refs" class="references">

  <div id="ref-___">


  </div>

</div>
