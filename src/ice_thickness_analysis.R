
library(tidyverse)
library(dplyr)

# library(broom)
library(datateachr)
library(infer)
# library(knitr)
# library(palmerpenguins)
# library(tidyverse)
# library(datateachr)

p <- '/Users/Jayme/OneDrive/MDS/522/Group-13/data/processed/ice_thickness.csv'

# copied from tiff!
ci_median <- function(sample, var, level = 0.95, type = "percentile") {
    sample %>% 
        rep_sample_n(nrow(sample), replace = TRUE, reps = 100) %>% 
        summarise(stat = median({{ var }})) %>%
        get_confidence_interval(level = level, type = type) 
}


# plot 1 > 3 facets for months 1, 2, 3

# table of month x p value (3)

# plot all years confidence intervals?


years <- c(1984, 1994)
# years <- c(1985, 1995)
# years <- c(1987, 1997)
month <- 1

df_in <- read_csv(p)

df <- df_in %>%
    filter(
        year %in% years &
            month == 1) %>%
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

median_est

# geom_violin(trim = TRUE) +

# facet by month
plt <- ggplot(df, aes(x = year, y = mean_ice_thickness)) +
    geom_point(data = median_est, aes(x = year, y = median),
               shape = 18, size = 3, color = "red") +
    geom_errorbar(data = median_est, aes(x = year,
                                         y = median,
                                         ymin = lower_ci,
                                         ymax = upper_ci),
                  size = 0.5, color = "blue", width = 0.05)

plt + ggsave("chart.png")

# delta_star <- medians %>%
#     pull(median) %>%
#     diff()
# 
# print(delta_star)
# 
# set.seed(2020)
# result <- df %>%
#     specify(formula = mean_ice_thickness ~ year)  %>%
#     hypothesize(null = "independence") %>%
#     generate(reps = 1000, type = "permute") %>%
#     calculate(stat = "diff in medians", order = years) %>%
#     get_pvalue(obs_stat = delta_star, direction = "both")
# 
# print(result$p_value)