# author: Jayme Gordon
# date: 2020-11-27

"This script creates a png of ice thickness median values per year,
and a csv of p values for months (1, 2, 3).
NOTE - directories are relative to where script is called from

Usage: ice_thickness_analysis.R  --dir_in=<dir_in>  --dir_out=<dir_out>

Options:
    --dir_in String, directory to read processed ice_thickness.csv from
    --dir_out String, directory to save output png to
" -> doc

library(tidyverse)
library(dplyr, warn.conflicts = FALSE)
library(datateachr)
library(infer)
library(ggplot2)
library(purrr)
library(knitr)
library(docopt)

options(dplyr.summarise.inform = FALSE)
set.seed(2020)

main <- function() {
    # parse docopt args
    opt <- docopt(doc)

    # dir_out <- "../results"
    dir_out <- opt$dir_out

    # dir_in <- "../data/processed/ice_thickness.csv"
    dir_in <- opt$dir_in
    
    df_in <- read_csv(dir_in)

    make_pvalue_table(df_in = df_in, dir_out = dir_out)
    make_chart(df_in = df_in, dir_out = dir_out)
}


#' Generate 95% confidence intervals and save chart
#'
#' @param df_in DataFrame with samples
#' @param dir_out The folder to save the chart in
#'
#' @return
#' @export
#'
#' @examples
#' make_chart(df, "/results")
make_chart <- function(df_in, dir_out) {

    # filter df to all years, and jan 1
    # TODO make this a loop for all 3 months later?
    df <- df_in %>%
        filter(
            month == 1 &
            year >= 1984 &
            year <= 1996) %>%
        mutate(year = as.factor(year))

    medians <- df %>% 
        group_by(year) %>% 
        summarise(median = median(mean_ice_thickness))

    median_est <- df %>% 
        group_by(year) %>% 
        nest() %>% 
        mutate(ci = map(data, ~ci_median(., mean_ice_thickness))) %>% 
        unnest(c(data, ci)) %>%
        left_join(medians) %>%
        group_by(year) %>% 
        nest(data = c(mean_ice_thickness))

    # create plot
    plt <- ggplot(df, aes(x = year, y = mean_ice_thickness)) +
        geom_errorbar(
            data = median_est,
            aes(
                x = year,
                y = median,
                ymin = lower_ci,
                ymax = upper_ci),
            size = 0.5,
            width = 0.5) +
        geom_point(
            data = median_est,
            aes(x = year, y = median),
            size = 3,
            color = "blue") +
        labs(
            x = "Year",
            y = "Median Ice Thickness (cm)",
            title = "95% Confidence Intervals for Median Ice Thickness per Year in January")

    plt + ggsave(paste0(dir_out, "/median_ice_thickness_ci.svg"))

}

#' Run permutation test for diff in means and return result
#'
#' @param month Integer representing month of interest
#' @param years Numeric vector containing 2 years of interest to compare
#' @param df DataFrame containing the sample observations
#' @param reps Integer number of repetitions for the permutation
#'
#' @return Integer - the calculated p-value
#' @export
#'
#' @examples
#' get_p_value(1, c(1984, 1996), df, 1000)
#' > 0.034
get_p_value <- function(month, years, df, reps) {
    
    # pvalue between 2 years, for single month

    medians <- df %>% 
        group_by(year) %>% 
        summarise(median = median(mean_ice_thickness))

    delta_star <- medians %>%
        pull(median) %>%
        diff()

    result <- df %>%
        specify(formula = mean_ice_thickness ~ year)  %>%
        hypothesize(null = "independence") %>%
        generate(reps = reps, type = "permute") %>%
        calculate(stat = "diff in medians", order = years) %>%
        get_pvalue(obs_stat = delta_star, direction = "both")
    
    result$p_value
}

#' Generate and save a table of p-values for each month
#'
#' @param df_in DataFrame with samples
#' @param dir_out String for directory to save the output table in
#' @param reps Integer number of reps to use for the permutation test
#' @param years Numeric vector containing 2 years of interest to compare
#' @param save_img Boolean indicating if the table should be saved as image as well as csv
#'
#' @return 
#' @export
#'
#' @examples
#' make_pvalue_table(df, "data/img_folder")
make_pvalue_table <- function(df_in, dir_out, reps = 1000, years = c(1984, 1994), save_img = FALSE) {
    
    months <- c(1)

    # filter df two specific years
    df <- df_in %>%
        filter(year %in% years) %>%
        mutate(year = as.factor(year))

    df_out <- tibble(month = months) %>%
        mutate(p_value = map_dbl(
            months,
            ~get_p_value(., years = years, df = df, reps = reps)))

    write.csv(df_out, paste0(dir_out, "/p_value.csv"))
    
    if(save_img){
        kable(df_out) %>% save_kable(paste0(dir_out, "/p_value.png"))
    }
}

#' Confidence intervals for the median
#'
#' @author Tiffany Timbers
#' @param sample tibble or data frame containing the sample data
#' @param var unquoted column name of the column for which the confidence 
#' intervals are being calculated
#' @param level numeric vector of length one specifying the confidence level. 
#' Default is 0.95.
#' @param type character vector of length one specifying the method to be used
#' for calculating the confidence intervals. Default is "percentile".
#'
#' @return a tibble with one row and two columns, one for the lower confidence
#' bound and one for the upper confidence bound
#' @export
#'
#' @examples
#'library(palmerpenguins)
#'ci_mean(penguins, body_mass_g)
ci_median <- function(sample, var, level = 0.95, type = "percentile") {
    sample %>% 
        rep_sample_n(nrow(sample), replace = TRUE, reps = 100) %>% 
        summarise(stat = median({{ var }})) %>%
        get_confidence_interval(level = level, type = type) 
}

main()