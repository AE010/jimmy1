import pandas as pd
import matplotlib.pyplot as plt

df_ventas = pd.read_excel("proyecto1.xlsx", sheet_name="in")
df_sucursales = pd.read_excel("Catalogo_sucursal.xlsx", sheet_name="in")
df = df_ventas.merge(df_sucursales, on="id_sucursal", how="left")

ventas_totales = df["ventas_tot"].sum()
socios_con_adeudo = df[df["B_adeudo"] == "Con adeudo"]["no_clientes"].sum()
socios_sin_adeudo = df[df["B_adeudo"] == "Sin adeudo"]["no_clientes"].sum()
socios_totales = socios_con_adeudo + socios_sin_adeudo
porc_con_adeudo = (socios_con_adeudo / socios_totales) * 100
porc_sin_adeudo = (socios_sin_adeudo / socios_totales) * 100
deuda_total = df["adeudo_actual"].sum()
porcentaje_utilidad = ((ventas_totales - deuda_total) / ventas_totales) * 100

print(f"Conocer las ventas totales del comercio: {ventas_totales}")
print(f"Conocer cuantos socios tienen adeudo y cuantos no tienen adeudo con su porcentaje correspondiente:")
print(f"  - Porcentaje de socios con adeudo: {porc_con_adeudo:.2f}%")
print(f"  - Porcentaje de socios sin adeudo: {porc_sin_adeudo:.2f}%")
print(f"Cuanto es la deuda total de los clientes: {deuda_total}")
print(f"Cuanto es el porcentaje de utilidad del comercio a partir de el total de las ventas respecto del adeudo: {porcentaje_utilidad:.2f}%")

df["B_mes"] = pd.to_datetime(df["B_mes"], errors="coerce")
df_fecha_ventas = df.groupby("B_mes")["ventas_tot"].sum().reset_index()
plt.figure(figsize=(12,6))
plt.bar(df_fecha_ventas["B_mes"].dt.strftime('%Y-%m'), df_fecha_ventas["ventas_tot"], color='blue', alpha=0.7, edgecolor='black', width=0.6)
plt.xticks(rotation=45, ha='right')
plt.title("Ventas Totales a lo Largo del Tiempo")
plt.xlabel("Fecha")
plt.ylabel("Ventas Totales")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

df_std = df.groupby("B_mes")["pagos_tot"].std().reset_index()
plt.figure(figsize=(10,5))
plt.plot(df_std["B_mes"].dt.strftime('%Y-%m'), df_std["pagos_tot"], marker='o', linestyle='-', color='red')
plt.xticks(rotation=90)
plt.title("Desviación Estándar de los Pagos Realizados")
plt.xlabel("Fecha")
plt.ylabel("Desviación Estándar de Pagos")
plt.show()

df_sucursal_ventas = df.groupby("suc")["ventas_tot"].sum()
plt.figure(figsize=(7,7))
plt.pie(df_sucursal_ventas, labels=df_sucursal_ventas.index, autopct='%1.1f%%')
plt.title("Distribución de Ventas por Sucursal")
plt.show()

df_sucursal = df.groupby("suc").agg({"adeudo_actual": "sum", "ventas_tot": "sum"})
df_sucursal["margen_utilidad"] = (df_sucursal["ventas_tot"] - df_sucursal["adeudo_actual"]) / df_sucursal["ventas_tot"] * 100

fig, ax1 = plt.subplots(figsize=(10,5))
ax2 = ax1.twinx()
ax1.bar(df_sucursal.index, df_sucursal["adeudo_actual"], color='r', label='Deuda Total', width=0.6)
ax2.plot(df_sucursal.index, df_sucursal["margen_utilidad"], color='b', marker='o', linestyle='-', label='Margen de Utilidad (%)')
ax1.set_xlabel("Sucursal")
ax1.set_ylabel("Deuda Total", color='r')
ax2.set_ylabel("Margen de Utilidad (%)", color='b')
plt.title("Deudas Totales por Sucursal y Margen de Utilidad")
plt.tight_layout()
plt.show()
