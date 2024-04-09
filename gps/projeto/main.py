import tkinter as tk
from tkinter import messagebox
from collections import deque

from dicionario import mapa_romenia
from dicionario import coordenadas_cidades_romenia

# Função para obter dicionario
def get_dictionary(dictionary):
    return dictionary

# Coleta das informações principais a partir de dicionarios
romenian_map = get_dictionary(mapa_romenia.mapa)
city_coordinates = get_dictionary(coordenadas_cidades_romenia.cidades)

def bfs_shortest_path(graph, start, goal):
    # Inicializa a fila com o ponto de origem
    queue = deque([[start]])
    # Enquanto a fila não estiver vazia
    while queue:
        # Retira o caminho da fila
        path = queue.popleft()
        # Obtém o último nó do caminho
        node = path[-1]
        # Se o último nó for o objetivo, retorna o caminho
        if node == goal:
            return path
        # Para cada vizinho do último nó
        for neighbor in graph[node]:
            # Cria um novo caminho e o adiciona à fila
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)

def bfs_best_path(graph, start, goal):
    # Inicializa a fila com o ponto de origem
    queue = deque([[start]])
    # Enquanto a fila não estiver vazia
    while queue:
        # Retira o caminho da fila
        path = queue.popleft()
        # Obtém o último nó do caminho
        node = path[-1]
        # Se o último nó for o objetivo, retorna o caminho
        if node == goal:
            return path
        # Para cada vizinho do último nó
        for neighbor in graph[node]:
            # Cria um novo caminho e o adiciona à fila
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)
            # Verifica se há uma maneira de remover cidades intermediárias do caminho
            if len(set(new_path)) == len(new_path):
                return new_path

# Função para obter as coordenadas de um caminho
def get_coordinates(path):
    coordinates = []
    for city in path:
        coordinates.append(city_coordinates[city])
    return coordinates

# Função para calcular a distância total de um caminho
def calculate_distance(path):
    distance = 0
    for i in range(len(path) - 1):
        distance += romenian_map[path[i]][path[i+1]]
    return distance

#Função que mostra a mensagem de erro
def error_message(start_city, goal_city):
    if(start_city not in romenian_map and goal_city in romenian_map):
        return messagebox.showerror("Erro", f'A cidade "{start_city}" está inválida. Certifique-se de digitar cidades existentes no mapa da Romênia.')
    elif(start_city in romenian_map and goal_city not in romenian_map):
        return messagebox.showerror("Erro", f'A cidade "{goal_city}" está inválida. Certifique-se de digitar cidades existentes no mapa da Romênia.')
    else:
        return messagebox.showerror("Erro", f'As cidades "{start_city}" e "{goal_city}" estão inválidas. Certifique-se de digitar cidades existentes no mapa da Romênia.')

# Função para calcular os resultados
def show_results():
    start_city = entry_start.get().capitalize()
    goal_city = entry_goal.get().capitalize()

    # Verifica se os pontos de origem e destino estão no mapa
    if start_city not in romenian_map or goal_city not in romenian_map:
        error_message(start_city, goal_city)
    else:
        # Encontrando os caminhos
        path_to_goal = bfs_shortest_path(romenian_map, start_city, goal_city)
        best_path = bfs_best_path(romenian_map, start_city, goal_city)

        # Calcula as coordenadas dos caminhos
        path_to_goal_coords = get_coordinates(path_to_goal)
        best_path_coords = get_coordinates(best_path)

        # Calcula as distâncias dos caminhos
        path_to_goal_distance = calculate_distance(path_to_goal)
        best_path_distance = calculate_distance(best_path)

        # Atualiza a tela com os resultados
        label_path_to_goal.config(text=f'Caminho para o objetivo: {path_to_goal}\nDistância: {path_to_goal_distance} km\nCoordenadas: {path_to_goal_coords}')
        label_best_path.config(text=f'Melhor caminho: {best_path}\nDistância: {best_path_distance} km\nCoordenadas: {best_path_coords}')

# Cria a janela principal
window = tk.Tk()
window.title("Calculadora de Rotas")

# Cria os widgets
label_start = tk.Label(window, text="Insira o local de partida:")
label_start.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_start = tk.Entry(window)
entry_start.grid(row=0, column=1, padx=5, pady=5)

label_goal = tk.Label(window, text="Insira o local de destino:")
label_goal.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_goal = tk.Entry(window)
entry_goal.grid(row=1, column=1, padx=5, pady=5)

button_calculate = tk.Button(window, text="Calcular", command=show_results)
button_calculate.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

label_path_to_goal = tk.Label(window, text="")
label_path_to_goal.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

label_best_path = tk.Label(window, text="")
label_best_path.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Ajusta a posição dos widgets para se centralizarem quando a janela for expandida
for i in range(5):
    window.grid_rowconfigure(i, weight=1)
    window.grid_columnconfigure(i, weight=1)

# Inicia o loop principal da janela
window.mainloop()
