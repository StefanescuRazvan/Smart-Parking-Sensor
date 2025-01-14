import pygame
import serial

# Configurare serial
ser = serial.Serial('COM3', 9600)  # Înlocuiește cu portul COM corect
pygame.init()

# Dimensiunea ferestrei
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Sistem parcare - HC-SR04")

# Culori
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Încarcă imaginea mașinii
car_image_path = r"C:\Users\razva\OneDrive\Desktop\car.png"  # Calea exactă către imagine
car_image = pygame.image.load(car_image_path)
car_image = pygame.transform.scale(car_image, (600, 300))  # Scalează imaginea

running = True
distance = 100  # Valoare inițială

# Poziția și dimensiunile dreptunghiurilor (zonele)
zones = [
    {"rect": pygame.Rect(200, 500, 150, 70), "color": GRAY, "label": "Out of range"},  # Out of range
    {"rect": pygame.Rect(360, 500, 150, 70), "color": GRAY, "label": "Attention"},    # Attention
    {"rect": pygame.Rect(520, 500, 150, 70), "color": GRAY, "label": "Close"},        # Close
    {"rect": pygame.Rect(680, 500, 150, 70), "color": GRAY, "label": "Warning"},      # Warning
]

font = pygame.font.Font(None, 36)  # Font pentru text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Citire distanță de la ESP32
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data == "out of range":
                distance = 100  # Distanță simbolică pentru out of range
            else:
                distance = float(data)  # Convertim la float
        except ValueError:
            pass  # Ignorăm erorile de conversie

    # Actualizează culorile dreptunghiurilor în funcție de distanță
    if distance > 60:
        zones[0]["color"] = GREEN
        zones[1]["color"] = GRAY
        zones[2]["color"] = GRAY
        zones[3]["color"] = GRAY
    elif distance > 30:
        zones[0]["color"] = GRAY
        zones[1]["color"] = YELLOW
        zones[2]["color"] = GRAY
        zones[3]["color"] = GRAY
    elif distance > 10:
        zones[0]["color"] = GRAY
        zones[1]["color"] = GRAY
        zones[2]["color"] = ORANGE
        zones[3]["color"] = GRAY
    else:
        zones[0]["color"] = GRAY
        zones[1]["color"] = GRAY
        zones[2]["color"] = GRAY
        zones[3]["color"] = RED

    # Desenare ecran
    screen.fill(BLACK)

    # Desenează imaginea mașinii
    screen.blit(car_image, (200, 100))  # Poziționează imaginea

    # Desenează dreptunghiurile (zonele)
    for zone in zones:
        pygame.draw.rect(screen, zone["color"], zone["rect"])
        label = font.render(zone["label"], True, (255, 255, 255))
        label_x = zone["rect"].x + (zone["rect"].width - label.get_width()) // 2
        label_y = zone["rect"].y + (zone["rect"].height - label.get_height()) // 2
        screen.blit(label, (label_x, label_y))

    # Text cu distanța actuală centrat sub dreptunghiuri
    distance_text = font.render(f"Distance: {distance:.1f} cm", True, (255, 255, 255))
    total_width = zones[-1]["rect"].right - zones[0]["rect"].left  # Lățimea totală a zonei dreptunghiurilor
    text_x = zones[0]["rect"].left + (total_width - distance_text.get_width()) // 2  # Centrat pe lățimea totală
    text_y = zones[0]["rect"].bottom + 20  # Sub dreptunghiuri
    screen.blit(distance_text, (text_x, text_y))

    pygame.display.flip()
    pygame.time.delay(100)  # Actualizare la fiecare 100ms

pygame.quit()
