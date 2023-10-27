# Simulate churn data

library(charlatan)
library(tidyverse)
library(readr)

file_out <- here::here("data/churn.csv")
file_out_churn_reason <- here::here("data/churn_reason.csv")
file_out_purchases <- here::here("data/purchase_characteristics.csv")

num_customers <- 1e5
churn_reasons <-
  c(
    "Competitor",
    "Price",
    "Dissatisfaction",
    "Other"
  )

# ==============================================================================

set.seed(111)

churn_model <- function(
    total_transactions,
    last_purchase_days_ago,
    contract,
    state
) {

  northeast <- state %in% c("New Jersey", "New York", "Massachusetts", "Pennsylvania")

  south <- state %in% c("South Carolina", "Georgia", "Alabama", "Florida")

  monthly_contract <- contract == "Month-to-month"

  1 / (1 + exp(-(-0.1 - 0.02 * total_transactions + 0.01 * last_purchase_days_ago + .01 * monthly_contract + .1 * northeast - .2 * south))) +
    rnorm(num_customers, mean = 0, sd = 0.1)

}

generate_customer_sample <- function(v) {
  sample(v, size = num_customers, replace = TRUE)
}

# Simulate customer data using the charlatan package
fake_data <-
  tibble(
    customer_id = 1:num_customers,
    contract =
      sample(
        c("Month-to-month", "One year"),
        size = num_customers,
        replace = TRUE
      ),
    product =
      sample(
        c("Standard", "Premium", "Professional"),
        size = num_customers,
        replace = TRUE
      ),
    monthly_charges =
      charlatan::ch_double(num_customers, mean = 30, sd = 4),
    average_purchase_amount =
      charlatan::ch_double(num_customers, mean = 50, sd = 12),
    last_purchase_days_ago =
      charlatan::ch_integer(num_customers, min = 1, max = 365),
    state = generate_customer_sample(state.name),
    date =
      generate_customer_sample(seq(as_date("2022-01-01"), today(), by = "day"))
  ) |>
  mutate(
    total_transactions =
      if_else(
        contract == "Month-to-month",
        ch_integer(n = num_customers, min = 1, max = 36),
        ch_integer(n = num_customers, min = 1, max = 3)
      )
  )

# Generate churn labels based on a predictive model
churn_data <-
  fake_data |>
  mutate(
    churn_prob =
      churn_model(total_transactions, last_purchase_days_ago, contract, state),
    churn = churn_prob > 0.9,
    reason =
      if_else(
        churn,
        sample(
          churn_reasons,
          size = num_customers,
          replace = TRUE,
          prob = c(.33, .29, .17, .21)
        ),
        NA_character_
      ),
    date = if_else(churn, date, NA),
    year = lubridate::year(date),
    quarter = lubridate::quarter(date)
  ) |>
  select(-churn_prob) |> 
  write_csv(file_out)

churn_data |> 
  filter(!is.na(reason)) |> 
  group_by(product, year = year(date), quarter = quarter(date), reason) |> 
  summarize(total_churn = sum(churn), total = n(), .groups = "drop_last") |> 
  mutate(
    year_quarter_total = sum(total),
    percent_churn = total_churn / year_quarter_total
  ) |> 
  ungroup() |> 
  write_csv(file_out_churn_reason)

churn_data |>
  group_by(contract, churn, product) |>
  summarize(
    across(
      c(average_purchase_amount, total_transactions, last_purchase_days_ago),
      median
    ),
    .groups = "drop_last"
  ) |> 
  ungroup() |> 
  mutate(average_purchase_amount = round(average_purchase_amount, 2)) |> 
  rename(
    `Average purchase` = average_purchase_amount,
    `Total transactions` = total_transactions,
    `Days since last purchase` = last_purchase_days_ago
  ) |> 
  mutate(churn = if_else(churn, "Churned", "Did not churn")) |> 
  write_csv(file_out_purchases)


