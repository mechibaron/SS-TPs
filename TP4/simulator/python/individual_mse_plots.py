import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_mse(positions1, positions2):
    """Calcula el error cuadrático medio entre dos listas de posiciones."""
    return np.mean((positions1 - positions2) ** 2)

def calculate_pointwise_error(positions1, positions2):
    """Calcula el error punto por punto (cuadrático) entre dos listas de posiciones."""
    return (positions1 - positions2) ** 2

def plot_error_curve(time, errors, method_name):
    """Grafica el error cuadrático punto por punto a lo largo del tiempo."""
    plt.figure(figsize=(10, 6))
    plt.plot(time, errors, label=f'Error Cuadrático ({method_name})', color='purple')
    plt.xlabel('Tiempo')
    plt.ylabel('Error Cuadrático')
    plt.title(f'Curva del Error Cuadrático - Método: {method_name}')
    plt.legend()
    plt.grid(True)
    plt.show()

def process_files(analitic_file, base_dir):
    # Leer el archivo analitic/particles.csv
    analitic_df = pd.read_csv(analitic_file)

    # Obtener las posiciones y tiempos del archivo analítico
    analitic_positions = analitic_df.set_index(['time', 'id'])['position']
    analitic_time = analitic_df['time'].unique()

    # Recorrer todos los archivos en la carpeta base excepto la carpeta 'analitic'
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d != 'analitic']  # Excluir la carpeta 'analitic'

        for file in files:
            if file.endswith('particle.csv'):
                file_path = os.path.join(root, file)
                method_name = os.path.basename(root)  # Nombre del método (beeman, verlet, etc.)

                # Leer el archivo de partículas
                particles_df = pd.read_csv(file_path)

                # Obtener las posiciones y tiempos del archivo numérico
                numeric_positions = particles_df.set_index(['time', 'id'])['position']
                numeric_time = particles_df['time'].unique()

                # Comparar posiciones entre el archivo actual y el archivo analitic
                common_index = numeric_positions.index.intersection(analitic_positions.index)

                if len(common_index) > 0:
                    mse = calculate_mse(numeric_positions.loc[common_index], analitic_positions.loc[common_index])

                    # Calcular el error punto por punto
                    pointwise_error = calculate_pointwise_error(numeric_positions.loc[common_index], analitic_positions.loc[common_index])

                    # Escribir el MSE en un archivo mse.txt en la misma carpeta del archivo comparado
                    mse_file_path = os.path.join(root, 'mse.txt')
                    with open(mse_file_path, 'w') as mse_file:
                        mse_file.write(f'MSE: {mse}\n')
                        print(f'MSE calculado para {file} y guardado en {mse_file_path}')

                    # Graficar la curva del error
                    plot_error_curve(analitic_time, pointwise_error, method_name)
                else:
                    print(f'No hay partículas comunes en {file} y el archivo analitic.')


# Ruta del archivo analitic/particles.csv
analitic_file = 'outputs/analitic/particle.csv'

# Directorio base donde están las demás carpetas
base_dir = 'outputs'

# Procesar los archivos
process_files(analitic_file, base_dir)