import pygame
import time
import sys
import math
pygame.init()
width = 1500
height = 800
fps = 144
screen = pygame.display.set_mode((width, height))
canvas=pygame.Surface((width, height))
canvas.fill('black')
name = pygame.display.set_caption("paint")
timer = pygame.time.Clock()
hex_text = ""
font = pygame.font.SysFont(None, 32)
x=10
size=2
drawing = False
color='white'
purple='#5f13d1'
block_rect=pygame.Rect(0,0,220,30)
black_rect=pygame.Rect(width-35,80,25,25)
blue_rect=pygame.Rect(width-35, 10, 25,25)
white_rect=pygame.Rect(width-35, 45, 25, 25)
red_rect=pygame.Rect(width-70, 10, 25,25)
green_rect=pygame.Rect(width-70, 45, 25,25)
purple_rect=pygame.Rect(width-70, 80, 25,25)
slider_rect=pygame.Rect(x,0,10,30)
messagebox_rect=pygame.Rect(width//2-90, height//2-25, 180, 50)
writer_rect=pygame.Rect(width//2-100, height//2-50, 200, 100)
color_rect=pygame.Rect(width//2+120,height//2+70, 50,50)
line_rect=pygame.Rect(width//2, 20,10,50)
ui_rect=pygame.Rect(0,0,width, 110)
just_applied_color=False
show_ui=False
grid=False
color_w=False
line_draw=False
first_mpos=None
last_mpos=None
filename=f"drawing_{int(time.time())}.png"
ui_rects = [block_rect,slider_rect,blue_rect,white_rect,red_rect,green_rect,purple_rect,black_rect, messagebox_rect,writer_rect, color_rect, line_rect]
def over_ui(pos):
    if color_w:
        return writer_rect.collidepoint(pos)
    # toolbar UI only when shown
    if show_ui:
        return any(rect.collidepoint(pos) for rect in [block_rect, slider_rect,blue_rect, white_rect, red_rect,green_rect, purple_rect, black_rect, ui_rect])
    return False
def draw_lines():
    for i in range(height//20):
        line_rect=(0,i*height//20, width, 2)
        pygame.draw.rect(screen,'white', line_rect)
def color_write():
    pygame.draw.rect(screen,'white', writer_rect)
    pygame.draw.rect(screen,'black', messagebox_rect)
    text_surface = font.render(hex_text, True, 'white')
    screen.blit(text_surface,(messagebox_rect.x + 5, messagebox_rect.y + 12))
    if len(hex_text)==7:
        pygame.draw.rect(screen, hex_text, color_rect)
    else:
        pygame.draw.rect(screen, color, color_rect)

def ruler():
    pygame.draw.line(canvas,color, last_mpos, first_mpos, size)
    
while True:
    screen.fill('black')
    screen.blit(canvas, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                show_ui=not show_ui
            if event.key==pygame.K_l:
                grid=not grid
            if event.key==pygame.K_w:
                color_w = not color_w
                if color_w:
                    pygame.key.start_text_input()
                    hex_text = ""
                else:
                    pygame.key.stop_text_input()
        if event.type==pygame.KEYDOWN and event.key==pygame.K_LCTRL:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                pygame.image.save(canvas, filename)
                print("saved")
        if event.type == pygame.KEYDOWN and color_w:
            if event.key == pygame.K_BACKSPACE:
                hex_text = hex_text[:-1]
            elif event.key == pygame.K_RETURN:
                if len(hex_text) <= 7 and hex_text.startswith("#"):
                    try:
                        color = pygame.Color(hex_text)
                        color_w = False
                        pygame.key.stop_text_input()
                    except ValueError:
                        pass        
        if event.type == pygame.TEXTINPUT and color_w:
            if len(hex_text) < 7:        
                hex_text += event.text
        if event.type == pygame.MOUSEBUTTONDOWN and line_draw:
            if event.button == 1:
                first_mpos=pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and line_draw:
            if event.button == 1:
                line_draw= not line_draw
        if event.type == pygame.MOUSEBUTTONUP and line_draw:
            if event.button == 1:
                last_mpos=pygame.mouse.get_pos()
    #ui display
    if show_ui==True:
        pygame.draw.rect(screen,"#564F4F",ui_rect)
    if show_ui==True and not color_w:
        pygame.draw.rect(screen,'white', line_rect)
        pygame.draw.rect(screen,purple, purple_rect)     
        pygame.draw.rect(screen, 'blue', blue_rect)
        pygame.draw.rect(screen, 'white', white_rect)
        pygame.draw.rect(screen, 'red', red_rect)
        pygame.draw.rect(screen, 'green', green_rect)        
        pygame.draw.rect(screen, 'grey', block_rect)
        pygame.draw.rect(screen, 'white', slider_rect)
        pygame.draw.rect(screen,'black', black_rect)
    mpos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    if grid:
        draw_lines()
    if color_w:
        color_write()
    if mouse_buttons[0] and line_rect.collidepoint(mpos):
        line_draw=not line_draw
    if line_draw and not drawing:
        if last_pos is not None:
            first_mpos=[mpos[0], 0]
            last_mpos=[last_pos[0], 0]
            pygame.draw.line(canvas,color, last_mpos, first_mpos, size)
            pygame.draw.circle(canvas,color, first_mpos, size//2)
            last_pos = mpos  
        else:
            last_pos = mpos
    if not mouse_buttons[0]:
        drawing = False
        last_pos = None
    #color changing
    if not color_w and show_ui and not just_applied_color:
        if mouse_buttons[0] and blue_rect.collidepoint(mpos):
            color='blue'
        if mouse_buttons[0] and white_rect.collidepoint(mpos):
            color='white'
        if mouse_buttons[0] and red_rect.collidepoint(mpos):
            color='red'
        if mouse_buttons[0] and green_rect.collidepoint(mpos):
            color='green'
        if mouse_buttons[0] and purple_rect.collidepoint(mpos):
            color='#5f13d1'
        if mouse_buttons[0] and black_rect.collidepoint(mpos):
            color='black'
    #size
    if mouse_buttons[0] and block_rect.collidepoint(mpos):
        x = mpos[0] - block_rect.x
        x = max(10, min(x, 200))
        slider_rect.width = x
        size=x//4
    #line
    
    elif mouse_buttons[0] and not over_ui(mpos) and not color_w and not line_draw:
        drawing = True
        if last_pos is not None:
            pygame.draw.line(canvas,color, last_pos, mpos, size)
            pygame.draw.circle(canvas,color, mpos, size//2)
            last_pos = mpos  
        else:
            last_pos = mpos
    pygame.display.update()
    timer.tick(fps)
