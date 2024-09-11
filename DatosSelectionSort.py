import pandas as pd
import time
inicio= time.time()
class Employee:
    def __init__(self, index, satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company, Work_accident, left, promotion_last_5years, Department, salary):
        self.index = index
        self.satisfaction_level = satisfaction_level
        self.last_evaluation = last_evaluation
        self.number_project = number_project
        self.average_montly_hours = average_montly_hours
        self.time_spend_company = time_spend_company
        self.Work_accident = Work_accident
        self.left = left
        self.promotion_last_5years = promotion_last_5years
        self.Department = Department
        self.salary = salary

pd.set_option('display.max_rows', None)

datitos= pd.read_csv(r'C:\Users\Cesar\Documents\Datos_csv\HR_capstone_dataset.csv', sep=';', header=None)

departments = {
    'sales': [],
    'accounting': [],
    'hr': [],
    'technical': [],
    'support': [],
    'management': [],
    'IT': [],
    'product_mng': [],
    'marketing': [],
    'RandD': []
}
totales=[]

employee_objects = []

for i in range(len(datitos)):
    department_name = datitos.iloc[i, 8]
    if department_name in departments:
        row = datitos.iloc[i, :].tolist()
        row[0] = float(row[0])  # satisfaction_level
        row[1] = float(row[1])  # last_evaluation
        row[2] = int(row[2])  # number_project
        row[3] = int(row[3])  # average_montly_hours
        row[4] = int(row[4])  # time_spend_company
        row[5] = int(row[5])  # Work_accident
        row[6] = int(row[6])  # left
        row[7] = int(row[7])  # promotion_last_5years

        employee = Employee(i, *row)
        employee_objects.append(employee)
        departments[department_name].append(employee)

for department_name, department_data in departments.items():
    total_time_spend = sum(int(employee.time_spend_company) for employee in department_data)
    print(f"El valor para ordenar el departamento {department_name} teniendo en cuenta la variable ""time_spend_company"" es de : ", total_time_spend)
    totales.append(total_time_spend)
    print("_"*20)

print("Por esto el orden de los departamentos con mayor valor al menor es el siguiente: ")
print(" ")
sorted_totals = sorted(totales, reverse=True)
for i in range(len(sorted_totals)):
    print(f"El departamento {list(departments.keys())[totales.index(sorted_totals[i])]} es el {i+1} en la lista")
    print("_"*20)

def selection_sort(department_data):
    n = len(department_data)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            employee1 = department_data[min_index]
            employee2 = department_data[j]

            if employee1.time_spend_company != employee2.time_spend_company:
                should_swap = employee1.time_spend_company > employee2.time_spend_company

            elif employee1.satisfaction_level != employee2.satisfaction_level:
                should_swap = employee1.satisfaction_level > employee2.satisfaction_level
            else:
                should_swap = False
            if should_swap is True:
                min_index = j
        department_data[i], department_data[min_index] = department_data[min_index], department_data[i]

department_totals = [(department_name, sum(employee.time_spend_company  + employee.satisfaction_level  for employee in department_data)) for department_name, department_data in departments.items()]

# Ordenar la lista en orden descendente por el total
department_totals.sort(key=lambda x: x[1], reverse=True)

# Crear un DataFrame vacío para almacenar todos los datos
all_data = pd.DataFrame()

# Iterar sobre la lista ordenada
for department_name, _ in department_totals:
    # Ordenar los datos del departamento con el método de selección
    selection_sort(departments[department_name])

    # Convertir los datos ordenados del departamento en un DataFrame
    data = [[employee.satisfaction_level, employee.last_evaluation, employee.number_project,
             employee.average_montly_hours, employee.time_spend_company, employee.Work_accident, employee.left,
             employee.promotion_last_5years, employee.Department, employee.salary] for employee in
            departments[department_name]]
    df = pd.DataFrame(data,columns=['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours',
                               'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years', 'Department',
                               'salary'])

    # Agregar una nueva columna que es la suma de 'Work_accident', 'time_spend_company' y 'satisfaction_level'
    df['total'] = df['time_spend_company']  + df['satisfaction_level']

    # Ordenar el DataFrame por la nueva columna en orden descendente
    df = df.sort_values(by='total', ascending=False)

    # Agregar los datos del departamento al DataFrame total
    all_data = pd.concat([all_data, df], ignore_index=True)

    # Crear un DataFrame con el mensaje
    separator = pd.DataFrame([f"El ultimo departamento ordenado fue: {department_name.upper()}"],
                             columns=['Department'])

    # Concatenar el DataFrame principal con el DataFrame del mensaje
    all_data = pd.concat([all_data, separator], ignore_index=True)

# Guardar el DataFrame total en un archivo Excel
all_data.to_excel(f"C:\\Users\\Cesar\\PycharmProjects\\Datos_Parcial_III\\DatosSelectionSort.xlsx", index=False)
ubicacion = f"C:\\Users\\Cesar\\PycharmProjects\\Datos_Parcial_III\\DatosSelectionSort.xlsx"
fin = time.time()
print("El archivo se ha ordenado con exito y se ha guardado en la ruta especificada", ubicacion)
print(f"El tiempo de ejecución del metodo de Selección fue de {fin - inicio} segundos")

