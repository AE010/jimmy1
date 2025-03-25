import pandas as pd
import matplotlib.pyplot as plt

df_ventas = pd.read_excel("proyecto1.xlsx", sheet_name="in")
df_sucursales = pd.read_excel("Catalogo_sucursal.xlsx", sheet_name="in")

df = df_ventas.merge(df_sucursales, on="id_sucursal", how="left")

ventas_totales = df["ventas_tot"].sum()
print(f"Ventas Totales: {ventas_totales}")

socios_con_adeudo = df[df["B_adeudo"] == "Con adeudo"]["no_clientes"].sum()
socios_sin_adeudo = df[df["B_adeudo"] == "Sin adeudo"]["no_clientes"].sum()
socios_totales = socios_con_adeudo + socios_sin_adeudo

porc_con_adeudo = (socios_con_adeudo / socios_totales) * 100
porc_sin_adeudo = (socios_sin_adeudo / socios_totales) * 100
print(f"Porcentaje de socios con adeudo: {porc_con_adeudo:.2f}%")
print(f"Porcentaje de socios sin adeudo: {porc_sin_adeudo:.2f}%")

plt.figure(figsize=(10,5))
plt.bar(df["B_mes"], df["ventas_tot"], color='blue')
plt.xticks(rotation=90)
plt.title("Ventas Totales a lo Largo del Tiempo")
plt.xlabel("Fecha")
plt.ylabel("Ventas Totales")
plt.show()

df_std = df.groupby("B_mes")["pagos_tot"].std().reset_index()
plt.figure(figsize=(10,5))
plt.plot(df_std["B_mes"], df_std["pagos_tot"], marker='o', linestyle='-', color='red')
plt.xticks(rotation=90)
plt.title("Desviación Estándar de los Pagos Realizados")
plt.xlabel("Fecha")
plt.ylabel("Desviación Estándar de Pagos")
plt.show()

deuda_total = df["adeudo_actual"].sum()
print(f"Deuda Total de Clientes: {deuda_total}")

porcentaje_utilidad = ((ventas_totales - deuda_total) / ventas_totales) * 100
print(f"Porcentaje de Utilidad: {porcentaje_utilidad:.2f}%")

df_sucursal_ventas = df.groupby("suc")["ventas_tot"].sum()
plt.figure(figsize=(7,7))
plt.pie(df_sucursal_ventas, labels=df_sucursal_ventas.index, autopct='%1.1f%%')
plt.title("Distribución de Ventas por Sucursal")
plt.show()

df_sucursal = df.groupby("suc").agg({"adeudo_actual": "sum", "ventas_tot": "sum"})
df_sucursal["margen_utilidad"] = (df_sucursal["ventas_tot"] - df_sucursal["adeudo_actual"]) / df_sucursal["ventas_tot"] * 100

fig, ax1 = plt.subplots(figsize=(10,5))
ax2 = ax1.twinx()
ax1.bar(df_sucursal.index, df_sucursal["adeudo_actual"], color='r', label='Deuda Total')
ax2.plot(df_sucursal.index, df_sucursal["margen_utilidad"], color='b', marker='o', linestyle='-', label='Margen de Utilidad (%)')

ax1.set_xlabel("Sucursal")
ax1.set_ylabel("Deuda Total", color='r')
ax2.set_ylabel("Margen de Utilidad (%)", color='b')
plt.title("Deudas Totales por Sucursal y Margen de Utilidad")
plt.show()
