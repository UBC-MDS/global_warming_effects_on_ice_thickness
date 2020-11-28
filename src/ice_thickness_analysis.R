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
# library(kableExtra)

options(dplyr.summarise.inform = FALSE)
set.seed(2020)

# dependencies - needed for save_kable.. probably dont need this
# install.packages("magick")
# install.packages("webshot")
# webshot::install_phantomjs()

main <- function() {
    # parse docopt args
    opt <- docopt(doc)

    # dir_out <- "./results"
    dir_out <- opt$dir_out

    # dir_in <- "./data/processed/ice_thickness.csv"
    df_in <- read_csv(opt$dir_in)

    make_pvalue_table(df_in = df_in, dir_out = dir_out)
    make_chart(df_in = df_in, dir_out = dir_out)
}


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
            color = "blue",
            width = 0.05) +
        geom_point(
            data = median_est,
            aes(x = year, y = median),
            shape = 18,
            size = 3,
            color = "red") +
        labs(
            x = "",
            y = "Median ice thickness (bootstrap)",
            title = "Bootstrap Samples of Median Ice Thickness per Year")

    plt + ggsave(paste0(dir_out, "/median_ice_thickness.png"))

}


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

make_pvalue_table <- function(df_in, dir_out, reps = 1000, years = c(1984, 1994)) {
    
    months <- c(1, 2, 3)

    # filter df two specific years
    df <- df_in %>%
        filter(year %in% years) %>%
        mutate(year = as.factor(year))

    df_out <- tibble(month = months) %>%
        mutate(p_value = map_dbl(
            months,
            ~get_p_value(., years = years, df = df, reps = reps))) #get_pvalue

    print(df_out)
    write.csv(df_out, paste0(dir_out, "/p_value.csv"))

    # kable(df_out) %>% save_kable(paste0(dir_out, "/p_value.png"))
    # kable save df
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