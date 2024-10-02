import pygame
from pygame.locals import *

# Inicialización de pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1100, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clue - Resolver el caso")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ROOM_COLORS = {
    "Estudio": (255, 200, 200),
    "Salón de Baile": (255, 0, 0),
    "Biblioteca": (200, 200, 255),
    "Comedor": (255, 255, 150),
    "Cocina": (200, 255, 200),
    "Salón": (255, 255, 200),
    "Sala": (200, 255, 255),
    "Invernadero": (255, 200, 255),
    "Sala de Billar": (150, 255, 200)
}

# Posiciones de las habitaciones
room_positions = {
    "Estudio": (400, 50),
    "Salón de Baile": (700, 50),
    "Biblioteca": (400, 300),
    "Comedor": (700, 300),
    "Cocina": (400, 550),
    "Salón": (700, 550),
    "Sala": (550, 50),
    "Invernadero": (550, 550),
    "Sala de Billar": (550, 300),
}

# Fuentes
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Personajes, armas y habitaciones posibles
suspects = ["Profesor Plum", "Coronel Mustard", "Señorita Scarlet", "Reverendo Green", "Señora Peacock", "Señora White"]
weapons = ["Candelabro", "Cuchillo", "Llave Inglesa", "Pistola", "Cuerda", "Tubo de plomo"]
rooms = list(room_positions.keys())

# Información de pistas
descartados_sospechosos = ["Coronel Mustard", "Profesor Plum"]
descartados_habitaciones = ["Cocina", "Salón de Baile"]
descartados_armas = ["Pistola"]

# Adivinanza basada en una sugerencia previa
adivinanza = {
    "sospechoso": "Señorita Scarlet",
    "habitación": "Biblioteca",
    "arma": "Cuchillo"
}

# Función lógica para evaluar la solución
def And(*args):
    return all(args)

def Or(*args):
    return any(args)

def evaluar_solucion(sospechoso, arma, habitacion):
    return And(
        sospechoso not in descartados_sospechosos,
        habitacion not in descartados_habitaciones,
        arma not in descartados_armas,
        Or(sospechoso != adivinanza["sospechoso"], habitacion != adivinanza["habitación"], arma != adivinanza["arma"])
    )

# Variables para almacenar la selección del jugador
selected_suspect = None
selected_weapon = None
selected_room = None
message = ""
mostrar_pistas = False

# Función para resolver automáticamente con IA
def resolver_con_ia():
    global selected_suspect, selected_weapon, selected_room, message

    # Simulación de IA que "adivina" correctamente
    selected_suspect = adivinanza["sospechoso"]
    selected_weapon = adivinanza["arma"]
    selected_room = adivinanza["habitación"]
    message = f"¡{selected_suspect} es el culpable con el {selected_weapon} en la {selected_room}!"

# Función para mostrar las pistas
def mostrar_pistas_func():
    global mostrar_pistas
    mostrar_pistas = not mostrar_pistas

# Función para dibujar el texto en pantalla
def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Función para dibujar botones y opciones
def draw_buttons():
    global selected_suspect, selected_weapon, selected_room, message, mostrar_pistas

    screen.fill(WHITE)

    # Dibujar habitaciones en el tablero con colores
    for room, pos in room_positions.items():
        pygame.draw.rect(screen, ROOM_COLORS[room], (*pos, 150, 150))  # Reducido a 150x150 para mejor alineación
        draw_text(room, small_font, BLACK, pos[0] + 20, pos[1] + 60)

    # Dibujar opciones de sospechosos a la izquierda
    draw_text("Sospechosos:", font, BLACK, 20, 20)
    for i, suspect in enumerate(suspects):
        color = RED if suspect == selected_suspect else BLACK
        draw_text(suspect, small_font, color, 20, 60 + i * 30)

    # Dibujar opciones de armas a la derecha
    draw_text("Armas:", font, BLACK, 250, 20)
    for i, weapon in enumerate(weapons):
        color = RED if weapon == selected_weapon else BLACK
        draw_text(weapon, small_font, color, 250, 60 + i * 30)

    # Mostrar pistas debajo de las listas en formato vertical si está activado
    if mostrar_pistas:
        # Mostrar las pistas en el siguiente orden: armas, habitaciones y sospechosos.
        y_offset = 400  # Coordenada Y inicial para las pistas
        draw_text("Pistas descartadas:", font, BLACK, 20, y_offset)
        y_offset += 40

        # Mostrar armas descartadas
        draw_text("Armas descartadas:", font, BLACK, 20, y_offset)
        for i, arma in enumerate(descartados_armas):
            draw_text(f"- {arma}", small_font, BLACK, 40, y_offset + 30 + (i * 30))
        y_offset += 30 * (len(descartados_armas) + 1)

        # Mostrar habitaciones descartadas
        draw_text("Habitaciones descartadas:", font, BLACK, 20, y_offset)
        for i, habitacion in enumerate(descartados_habitaciones):
            draw_text(f"- {habitacion}", small_font, BLACK, 40, y_offset + 30 + (i * 30))
        y_offset += 30 * (len(descartados_habitaciones) + 1)

        # Mostrar sospechosos descartados
        draw_text("Sospechosos descartados:", font, BLACK, 20, y_offset)
        for i, sospechoso in enumerate(descartados_sospechosos):
            draw_text(f"- {sospechoso}", small_font, BLACK, 40, y_offset + 30 + (i * 30))

    # Botón para resolver el caso
    pygame.draw.rect(screen, BLACK, (50, 700, 200, 50))
    draw_text("Resolver el caso", font, WHITE, 70, 710)

    # Botón para mostrar pistas
    pygame.draw.rect(screen, BLACK, (270, 700, 200, 50))
    draw_text("Ver Pistas", font, WHITE, 290, 710)

    # Botón para resolución automática con IA
    pygame.draw.rect(screen, BLACK, (490, 700, 200, 50))
    draw_text("Resolver con IA", font, WHITE, 510, 710)

    # Mostrar el mensaje de resultado
    draw_text(message, font, BLACK, 300, 650)

# Función principal del juego
def main():
    global selected_suspect, selected_weapon, selected_room, message

    running = True

    while running:
        draw_buttons()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos

                # Selección de sospechoso
                if 20 <= x <= 200:
                    for i, suspect in enumerate(suspects):
                        if 60 + i * 30 <= y <= 90 + i * 30:
                            selected_suspect = suspect

                # Selección de arma (ajustado las coordenadas a la derecha)
                elif 250 <= x <= 450:
                    for i, weapon in enumerate(weapons):
                        if 60 + i * 30 <= y <= 90 + i * 30:
                            selected_weapon = weapon

                # Selección de habitación desde el tablero
                for room, pos in room_positions.items():
                    if pos[0] <= x <= pos[0] + 150 and pos[1] <= y <= pos[1] + 150:
                        selected_room = room

                # Botón de resolver
                if 50 <= x <= 250 and 700 <= y <= 750:
                    if selected_suspect and selected_weapon and selected_room:
                        if evaluar_solucion(selected_suspect, selected_weapon, selected_room):
                            message = f"¡{selected_suspect} es el culpable con el {selected_weapon} en la {selected_room}!"
                        else:
                            message = "La solución no es correcta."
                    else:
                        message = "Por favor, selecciona un sospechoso, un arma y una habitación."

                # Botón para mostrar pistas
                elif 270 <= x <= 470 and 700 <= y <= 750:
                    mostrar_pistas_func()

                # Botón para resolución automática con IA
                elif 490 <= x <= 690 and 700 <= y <= 750:
                    resolver_con_ia()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
