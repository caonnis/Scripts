def calcular_salario(rate_por_hora, horas_por_mes):
    """
    Calcula el salario mensual basado en la tarifa por hora y las horas trabajadas por mes.

    :param rate_por_hora: Tarifa por hora en USD.
    :param horas_por_mes: Número de horas trabajadas por mes.
    :return: Salario mensual calculado.
    """
    salario = rate_por_hora * horas_por_mes
    return salario

# Solicitar al usuario los parámetros
rate_por_hora = float(input("Ingrese la tarifa por hora (USD): "))
horas_mensuales_primer_tramo = int(input("Ingrese las horas mensuales para los primeros 3 meses: "))
#horas_mensuales_segundo_tramo = int(input("Ingrese las horas mensuales para los siguientes 3 meses: "))

# Calcular salario para el primer tramo (primeros 3 meses)
salario_primer_tramo = calcular_salario(rate_por_hora, horas_mensuales_primer_tramo)

# Calcular salario para el segundo tramo (siguientes 3 meses)
#salario_segundo_tramo = calcular_salario(rate_por_hora, horas_mensuales_segundo_tramo)
28
# Mostrar resultados
print(f"\nSalario para los primeros 3 meses: {salario_primer_tramo:.2f} USD/mes")
#print(f"Salario para los siguientes 3 meses: {salario_segundo_tramo:.2f} USD/mes")

# Punto de salida
print("\nChau! Chau! :)")
