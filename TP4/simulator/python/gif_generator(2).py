import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os


def get_k_folders(base_path='outputs/multiple/'):
    return [f for f in os.listdir(base_path) if f.startswith('k_')]


def get_verlet_folders(k_folder, base_path='outputs/multiple/'):
    k_path = os.path.join(base_path, k_folder)
    return [f for f in os.listdir(k_path) if f.startswith('verlet_')]


def create_animation_for_folder(k_folder, verlet_folder):
    base_path = 'outputs/multiple/'
    folder_path = os.path.join(base_path, k_folder, verlet_folder)

    # Leer archivos CSV
    df = pd.read_csv(os.path.join(folder_path, 'particle.csv'))
    static_df = pd.read_csv(os.path.join(folder_path, 'static.csv'), header=None, skiprows=1)

    # Asignar nombres de columnas
    static_df.columns = ['n', 'k', 'mass', 'distance', 'amplitud', 'w0', 'wf']

    # Convertir valores de columnas a float
    n = float(static_df['n'].values[0])
    k = float(static_df['k'].values[0])
    mass = float(static_df['mass'].values[0])
    distance = float(static_df['distance'].values[0])
    amplitud = float(static_df['amplitud'].values[0])
    wf = float(static_df['wf'].values[0])

    # Definir el nuevo timestep
    new_timestep = 0.005  # Por ejemplo, 0.05 segundos

    # Filtrar los tiempos únicos
    times = df['time'].unique()

    # Quedarse solo con los tiempos que sean múltiplos del nuevo timestep
    times = times[(times % new_timestep) < 1e-4]

    # Crear figura y eje
    fig, ax = plt.subplots()
    ax.set_xlim(0, distance * n)
    ax.set_ylim(-(1.1 * df['position'].max()), df['position'].max() * 1.1)
    ax.set_xlabel('Posición horizontal (m)')
    ax.set_ylabel('Posición vertical (m)')

    # Inicializar el scatter plot y la línea
    scatter = ax.scatter([], [], s=50, c='blue')
    line, = ax.plot([], [], lw=2, color='blue')

    # Inicializar líneas de max y min
    max_line, = ax.plot([], [], lw=1, color='red', linestyle='--')
    min_line, = ax.plot([], [], lw=1, color='green', linestyle='--')

    # Inicializar valores max y min globales
    global_max = -np.inf
    global_min = np.inf

    # Función para actualizar la animación en cada cuadro
    def update(frame):
        nonlocal global_max, global_min
        current_time = times[frame]

        # Filtrar datos para el tiempo actual
        current_data = df[df['time'] <= current_time]

        # Calcular posiciones x
        particle_indices = current_data['id'].unique()
        x_positions = particle_indices * distance

        # Obtener posiciones y para el tiempo actual
        y_positions = current_data[current_data['time'] == current_time]['position']

        # Actualizar max y min globales
        frame_max = current_data['position'].max()
        frame_min = current_data['position'].min()
        global_max = max(global_max, frame_max)
        global_min = min(global_min, frame_min)

        # Crear un array de colores
        colors = ['red' if id == 0 else 'blue' for id in particle_indices]

        # Actualizar scatter plot
        scatter.set_offsets(list(zip(x_positions, y_positions)))
        scatter.set_color(colors)

        # Actualizar la línea de conexión
        line.set_data(x_positions, y_positions)

        # Añadir líneas de max y min estáticas
        ax.axhline(y=df['position'].max(), color='black', linestyle='--', lw=1)
        ax.axhline(y=df['position'].min(), color='black', linestyle='--', lw=1)

        # Actualizar las líneas de max y min actuales
        max_line.set_data([0, distance * n], [global_max, global_max])
        min_line.set_data([0, distance * n], [global_min, global_min])

        # Actualizar el título
        ax.set_title(f'k={k}, w={wf}, Time: {current_time:.3f}')

        return scatter, line, max_line, min_line

    # Crear la animación
    anim = FuncAnimation(fig, update, frames=len(times), blit=False)

    # Guardar la animación como un GIF
    gif_path = os.path.join(folder_path, f'animation_k_{k}_w_{wf}.gif')
    anim.save(gif_path, writer='imagemagick', fps=10)

    print(f'Guardado GIF en: {gif_path}')
    plt.close(fig)


# Buscar todas las carpetas k_{valor_de_k}
k_folders = get_k_folders()

# Crear la animación y guardar el GIF para cada combinación de k y w
for k_folder in k_folders:
    verlet_folders = get_verlet_folders(k_folder)
    for verlet_folder in verlet_folders:
        create_animation_for_folder(k_folder, verlet_folder)
