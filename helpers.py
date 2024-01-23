import pandas as pd
from plotnine import ggplot, options, aes, geom_point, geom_line, geom_boxplot, scale_color_manual, scale_fill_manual, scale_y_continuous, theme_minimal, labs
from mizani.formatters import percent_format

options.figure_size = (9, 6)
theme = theme_minimal(18)

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

  plot = (ggplot(churn_reason_product, aes(x="'Q' + quarter.astype(str)", y='percent_churn', color='reason')) +
          geom_point() +
          geom_line(aes(group='reason')) +
          scale_color_manual(values=color_palette) +
          scale_y_continuous(labels=percent_format()) +
          theme +
          labs(x="Quarter", y="Percent", color="Reason"))
 
  print(plot)
  
def plot_contract_type(df, product_type, y_var="last_purchase_days_ago", y_var_label="Days since last purchase"):
  churn_df = df[df["product"]==product_type]
  plot = (ggplot(churn_df, aes(x='contract', y=y_var, fill='churn')) +
            geom_boxplot() +
            scale_fill_manual(values=color_palette) +
            theme +
            labs(
                x="Contract type",
                y=y_var_label,
                fill="Churned"
            ) 
           )
  print(plot)
  
def table_purchases(df, product_type):
  df_product = df[df["product"]==product_type]
  df_product = df_product.rename(columns={'contract': 'Contract type', 'churn': 'Churn'})
  df_product = df_product.drop("product", axis=1)
  df_product = df_product.reset_index()
  return df_product
