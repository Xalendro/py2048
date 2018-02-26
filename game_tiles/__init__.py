import pygame


# Function to render tiles
def render(surface, tile_type, pos):
    tile_data = tile_assoc[tile_type]
    # Fill background
    rect = pygame.Rect([pos[0], pos[1], 100, 100])
    surface.fill(tile_data[0], rect)
    # Prepare text
    font = pygame.font.SysFont('courier', 37)
    # Making text white if tile backgroung is black
    if tile_ladder.index(tile_type) < 11:
        rendered_text = font.render(tile_data[1], 1, (0, 0, 0))
    else:
        rendered_text = font.render(tile_data[1], 1, (255, 255, 255))
    # Adjusting font size font start position for different lengths
    if len(tile_data[1]) == 1:
        rendered_rect = rendered_text.get_rect(x=rect.x + 40, centery=rect.centery)
    elif len(tile_data[1]) == 2:
        rendered_rect = rendered_text.get_rect(x=rect.x + 27, centery=rect.centery)
    elif len(tile_data[1]) == 3:
        rendered_rect = rendered_text.get_rect(x=rect.x + 15, centery=rect.centery)
    else:
        rendered_rect = rendered_text.get_rect(x=rect.x + 4, centery=rect.centery)
    # Draw the border
    pygame.draw.rect(surface, (210, 180, 140), (pos[0], pos[1], 100, 100), 8)
    # Draw text
    surface.blit(rendered_text, rendered_rect)


# Tile colors, labels and numbers
tile_assoc = {'0': ((214, 197, 180), ''), '1': ((240, 227, 209), '2'), '2': ((255, 226, 148), '4'),
              '3': ((245, 167, 0), '8'), '4': ((255, 59, 0), '16'), '5': ((252, 164, 252), '32'),
              '6': ((204, 128, 255), '64'), '7': ((128, 0, 255), '128'), '8': ((0, 0, 255), '256'),
              '9': ((190, 245, 116), '512'), 'A': ((127, 255, 0), '1024'), 'B': ((0, 0, 0), '2048'),
              'C': ((0, 0, 0), '4096'), 'D': ((0, 0, 0), '8192'), 'E': ((0, 0, 0), '2^14'),
              'F': ((0, 0, 0), '2^15')}

tile_ladder = '0123456789ABCDEF'
