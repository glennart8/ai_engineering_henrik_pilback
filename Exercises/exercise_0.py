import pandas as pd
import matplotlib.pyplot as plt

#   a) Do some EDA with info, find out column names, shape of dataset, describe method to get summary descriptive statistics.

df = pd.read_csv("data/norway_new_car_sales_by_month.csv")
df.info()
#   b) Draw a line chart of quantity for each year. Is there a year that should be skipped?

# Ta först bort år 2017
# df["Year"].value_counts().sort_index() # 2017 har bara en månad, denna borde tas bort
# print(df)
df = df[df["Year"] != 2017]
print(df)

df_yearly = df.groupby("Year")["Quantity"].sum().reset_index()
print(df_yearly)

# Bygg en plot
plt.figure(figsize=(10,6))
plt.plot(df_yearly["Year"], df_yearly["Quantity"], marker="o") # marker="o" gör att en symbol ritas ut vid varje punkt
plt.title("Total quantity per year")
plt.xlabel("Year")
plt.ylabel("Quantity")
# plt.show()

#   c) Draw a line chart of average CO2 emissions for same years that as in b)

df_co2 = df.groupby("Year")["Avg_CO2"].mean().reset_index()

plt.figure(figsize=(10,6)) # (10,6) för att den ska ha en tuple med två värden
plt.plot(df_co2["Year"], df_co2["Avg_CO2"], marker="o", color="green")
plt.title("Average CO2 emissions per Year")
plt.xlabel("Year")
plt.ylabel("Average CO2")
# plt.show()

#   d) Draw a line chart of all years and months for import
df_import = df.groupby("Year")["Import"].sum().reset_index()
print(df_import)
plt.figure(figsize=(10,6)) # (10,6) för att den ska ha en tuple med två värden
plt.plot(df_import["Year"], df_import["Import"], marker="o")
plt.title("Yearly imported cars")
plt.xlabel("Year")
plt.ylabel("Imported cars")
plt.show()

#   e) Draw a line chart of all years and months for average CO2 emissions



#   f) Draw a line chart of all years and months for electric cars import where it's relevant.

df_electric = df.groupby("Year")["Import_Electric"]

#   g) Draw a line chart of average diesel share per year



#   h) Discuss some findings with a friend based on this dataset, and do plot more graphs





