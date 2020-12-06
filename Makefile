# ice thickness data pipe
# author: Jayme Gordon
# date: 2020-12-03

all: data/raw/ice_thickness.csv data/processed/ice_thickness.csv results/density.svg results/median_ice_thickness_ci.svg results/p_value.csv doc/global_warming_effects_on_ice_thickness.md #doc/global_warming_effects_on_ice_thickness.pdf

# download data
data/raw/ice_thickness.csv: src/import_data.py
	python src/import_data.py --out_path=data/raw --url="https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls"

# pre-process data - clean and group monthly
data/processed/ice_thickness.csv: src/pre_process.py
	python src/pre_process.py --in_file=data/raw/ice_thickness.csv --out_file=data/processed/ice_thickness.csv

# eda
results/median_thickness_year.svg results/density.svg: src/eda_figure_export.py
	python src/eda_figure_export.py --input_file=data/processed/ice_thickness.csv --output_path_results=results --output_path_eda=src/EDA_notebook_visuals

# analysis - calc p-value
results/p_value.csv results/median_ice_thickness_ci.svg: src/ice_thickness_analysis.R
	Rscript src/ice_thickness_analysis.R --dir_in=data/processed/ice_thickness.csv --dir_out=results

# render markdown
doc/global_warming_effects_on_ice_thickness.md: doc/global_warming_effects_on_ice_thickness.Rmd doc/ice_thickness_refs.bib
	Rscript -e "rmarkdown::render('doc/global_warming_effects_on_ice_thickness.Rmd', output_format = 'github_document')"


clean:
	rm -rf data
	rm -rf results
	rm -rf doc/global_warming_effects_on_ice_thickness.md doc/global_warming_effects_on_ice_thickness.pdf