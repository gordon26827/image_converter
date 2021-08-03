import pygame as pg
import tkinter.simpledialog
from tkinter import filedialog
import os

pg.init()


def get_text_weights(chars, font, point):
    weights = {}

    surface_color = (0, 0, 0)
    text_color = (255, 255, 255)

    size = (point*6//10, point)
    # font = pg.font.Font("CourierPrime.ttf", point)

    # display = pg.display.set_mode(size)
    surface = pg.surface.Surface(size)

    for char in chars:
        surface.fill(surface_color)

        text = font.render(char, False, text_color)
        surface.blit(text, (0, 0))
        avg = 0

        for x in range(size[0]):
            for y in range(size[1]):
                rgb = surface.get_at((x, y))
                avg += rgb[0] + rgb[1] + rgb[2]

        avg /= size[0] * size[1] * 3
        weights[avg] = char

        # display.blit(surface, (0, 0))
        # pg.display.update()
        # pg.time.wait(750)

    weights = {key: weights[key] for key in sorted(weights.keys())}
    # weights = remove_similar(weights)

    return weights


# test function, doesn't really change much
def remove_similar(weights):
    min_diff = 10
    keys = list(weights.keys())
    prev = keys[0]

    for key in keys[1:]:
        if key - prev < min_diff:
            weights.pop(key)
        else:
            prev = key

    return weights


def image_to_text(image, weights):
    text = []

    for y in range(image.get_height()):
        text.append("")
        for x in range(image.get_width()):
            rgb = image.get_at((x, y))
            avg = rgb[0]*0.3 + rgb[1]*0.59 + rgb[2]*0.11

            best = None
            for key in weights:
                if not best:
                    best = key
                elif abs(avg - key) <= abs(avg - best):
                    best = key
                else:
                    break

            text[-1] += weights[best]

    return text


def get_image(filename, desired_size):
    image = pg.image.load(filename)
    size = list(image.get_size())
    size[0] *= 10 / 6
    factor = desired_size / max(size)
    image = pg.transform.scale(image, (int(size[0] * factor), int(size[1] * factor)))
    return image


def main(chars, image):
    point = 10
    font = pg.font.SysFont("courier", point)
    # print(font.get_height())
    weights = get_text_weights(chars, font, point)
    text = image_to_text(image, weights)
    # print("\n".join(text))
    display = pg.display.set_mode((len(text[0])*point*6//10, len(text)*point))
    clock = pg.time.Clock()

    running = True
    while running:
        clock.tick(20)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        display.fill((0, 0, 0))

        delta_y = 0
        for string in text:
            render = font.render(string, False, (255, 255, 255))
            display.blit(render, (0, delta_y))
            delta_y += point

        pg.display.update()

    pg.image.save(display, os.path.join(os.getcwd(), "images", "result.png"))


with open("characters.txt", "r", encoding="utf-8") as file:
    characters = file.read()

# characters1 = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌¦ÌÓßÔÒõÕµþÞÚÛÙýÝ¯´±‗¾¶§÷¸°¨·¹³²"""
# characters2 = r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌¦ÌÓßÔÒõÕµþÞÚÛÙýÝ¯´±‗¾¶§÷¸°¨·¹³²"""

file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), "images"), title="Select a file", filetypes=(("Image files", "*.jpg"), ("Image files", "*.png"), ("Image files", "*.gif"), ("All files", "*.*")))
resolution = tkinter.simpledialog.askinteger("Resolution", "Please input the desired character resolution (recommended between 50 and 300)")

if file_path and resolution:
    main(characters, get_image(file_path, resolution))
