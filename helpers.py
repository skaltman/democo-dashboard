import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_line, geom_boxplot, scale_color_manual, scale_fill_manual, scale_y_continuous, theme_minimal, labs
from mizani.formatters import percent_format

color_palette=[
    "#86C7ED",
    "#050548",
    "#7A6C5D",
    "#A54657",
    "#EEF3F6",
    "#BCFFC3"
]

def plot_churn_reason(df, product_type):
  churn_reason_product=df[(df["product"]==product_type)]

  plot = (ggplot(churn_reason_product, aes(x="year.astype(str) + ' Q' + quarter.astype(str)", y='percent_churn', color='reason')) +
          geom_point() +
          geom_line(aes(group='reason')) +
          scale_color_manual(values=color_palette) +
          scale_y_continuous(labels=percent_format()) +
          theme_minimal() +
          labs(x="Quarter", y="Percent", color="Reason", title="Reason for churn by quarter"))
  
  print(plot)
  
def plot_contract_type(df, product_type):
  churn_df = df[df["product"]==product_type]
  plot = (ggplot(churn_df, aes(x='contract', y='last_purchase_days_ago', fill='churn')) +
            geom_boxplot() +
            scale_fill_manual(values=color_palette) +
            theme_minimal() +
            labs(
                x="Contract type",
                y="Days since last purchase",
                fill="Churned",
                title="Churn status by contract type and days since purchase"
            ) 
           )
  print(plot)
  
def table_purchases(df, product_type):
  df_product = df[df["product"]==product_type]
  df_product = df_product.rename(columns={'contract': 'Contract type', 'churn': 'Churn'})
  df_product = df_product.drop("product", axis=1)
  df_product = df_product.reset_index()
  return df_product
