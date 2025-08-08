from decimal import Decimal, getcontext
import pygame
import math
import keyboard as k

getcontext().prec = 14
pygame.init()
pygame.display.set_caption("Калькулятор")
screen = pygame.display.set_mode((450,700))
"""
i_icon = os.getcwd()[:-4] + 'i.ico'                  # Доделай
pygame.display.set_icon(pygame.image.load('i.ico'))"""


Run = True
texts = pygame.font.Font(None,67)
otv = ''
zap = 0
primer = ['0']
primer1 = ''
primer2 = ''

def drob(prim):
    otv_drob = []
    left = 0
    prom = ''
    for i in prim:
        if i in {':', '*', '+', '-'}:
            otv_drob.append(prom)
            otv_drob.append(i)
            prom = ''
        else:
            prom += i
    otv_drob.append(prom)
    a1 = 'Decimal("'
    a2 = '")'
    otv_n = ''

    for i in otv_drob:
        if i in {'/', '*', '+', '-'}:
            otv_n += i
        else:
            otv_n += a1 + i + a2
            print(otv_n)
    return otv_n


def ravno(prim):
    krug = pygame.draw.circle(screen, (237,118,14), (370, 625), 48) 
    mouse_pos = pygame.mouse.get_pos()
    if krug.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:  # ЛКМ нажата?
            if prim[-1] in {':', '*', '+', '-', ','}:
                return 'Error'
            prim = prim.replace(',', '.')
            prim = prim.replace(':', '/')

            if '.' in prim or '/' in prim:
                prim = drob(prim)

            otv = str(eval(prim)).replace('.', ',')
            print(f'{prim} = {otv}')
            if list(otv)[-1] == '0' and list(otv) == ',':
                otv = int(otv)
            return otv

def knop(a, x=0, y=0, rgb=(255,255,255), knop_x=31, knop_y=25): # Функция для отображения кнопок
    invize_object = pygame.Rect(x - knop_x, y - knop_y, 95, 100)
    pygame.draw.rect(screen, (0, 0, 0), invize_object)
    mouse_pos = pygame.mouse.get_pos()
    otv1 = ''

    if invize_object.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (33,33,33), invize_object)  # Подсветка при наведении
        if pygame.mouse.get_pressed()[0]:  # ЛКМ нажата?
            pygame.draw.rect(screen, (0,0,0), invize_object)
            otv1 = str(a)
                
    screen.blit(texts.render(str(a), False, rgb), (x,y))
    return list(otv1)

def zapet(primer, zap=0):
    if knop(',', 260, 600) == [',']: # Запятая
        print(primer[-1], zap, primer)
        if zap == 0:
            primer += ','
            zap = 1
    elif primer[-1] in {':', '*', '+', '-'}:
        zap = 0
    return zap



def text(a, x=0, y=0, rgb=(255,255,255)):
    screen.blit(texts.render(str(a), False, rgb), (x,y))


while Run:
    screen.fill((0,0,0))
    knop('|||', 55, 600, (237,118,14), 26) # Первая строка
    primer += (knop('0', 155, 600))

    primer += (knop('1', 60, 500)) # Вторая строка
    primer += (knop('2', 155, 500))
    primer += (knop('3', 250, 500))
    primer += (knop('+', 355, 500, (237,118,14)))

    primer += (knop('4', 60, 400)) # Третья строка
    primer += (knop('5', 155, 400))
    primer += (knop('6', 250, 400))
    primer += (knop('-', 360, 400, (237,118,14), 36))

    primer += (knop('7', 60, 300)) # Четвёртая строка
    primer += (knop('8', 155, 300))
    primer += (knop('9', 250, 300))
    primer += (knop('*', 360, 300, (237,118,14), 36))

    n = knop('C', 60, 200, (237,118,14)) # Полное удаление      Перенести в функцию
    if n == ['C']:
        primer = ['0']
        otv = ''
        zap = 0

    n = knop('Del', 135, 200, (237,118,14), 11) # Еденичное удаление      Перенести в функцию
    if n == ['D', 'e', 'l']:
        if len(primer) > 1:
            if primer[-1] == ',':
                zap = 0
            del primer[-1]
        else:
            primer = ['0']
        otv = ''
        

    zap = zapet(primer, zap)


    n = (knop('%', 250, 200, (237,118,14)))
    if n == ['%'] and not primer[-1] in {':', '*', '+', '-', ','}:
        proc = ''
        i = len(primer) - 1
        while not(primer[i] in {':', '*', '+', '-'}) and i > -1:
            i -= 1
        proc = ''.join(primer[i + 1:])
        proc = proc.replace(',', '.')
        print(proc,primer[i + 1:])
        if (float(proc) / 100) == int(float(proc) / 100):
            proc = [str(float(proc) // 100).replace('.', ',')]
        else:
            proc = [str(float(proc) / 100).replace('.', ',')]
        del primer[i + 1:]
        primer += proc





    primer += (knop(':', 350, 200, (237,118,14), 36))


    if ((len(primer) > 1) and (primer[-1] in {':', '*', '+', '-', ','}) and (primer[-2] in {':', '*', '+', '-', ','})):
        del primer[-1]
    
    if len(primer) > 1 and primer[0] == '0' and not primer[1] in {':', '*', '+', '-', ','}:
        del primer[0]

    if primer != list(primer1):
        primer1 = ''
        for i in primer:
            primer1 += i

    otv1, b = ravno(primer1), text('=', 357, 600) # Доделай
    if otv1 != None and otv1 != otv:
        otv = otv1

    primer2 = primer1


    text(primer1, 150, 125)
    text(otv, 150, 75)

    pygame.display.update()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Run = False
            pygame.quit()
    pygame.time.Clock().tick(10)