#!/usr/bin/env python

from gimpfu import *
from random import randint

def load_background(img, image_path):
    # Background layer.
    background = gimp.Layer(img, "Background", img.width, img.height,
                            RGB_IMAGE, 100, NORMAL_MODE)
    background.fill(BACKGROUND_FILL)
    img.add_layer(background, 0)
    image_background = image_path + "/background/fundo_pregacao.png"
    layer_background = pdb.gimp_file_load_layer(img, image_background)
    pdb.gimp_layer_set_opacity(layer_background, 50)
    parent = None
    position = 0
    pdb.gimp_image_insert_layer(img, layer_background, parent, position)

def load_pregador_textbox(img, pregador):
    TEXTBOX_HEIGHT = 40

    drawable = None
    x = 0
    y = img.height - TEXTBOX_HEIGHT
    text_to_show = pregador
    border = 0
    antialias = True
    size = 38.0
    size_type = PIXELS
    fontname = "Eastman Condensed Trial Ultra-Bold Condensed"
    layer = pdb.gimp_text_fontname(img, drawable, x, y, text_to_show, border, antialias, size, size_type, fontname)
    # The justification for your text. { TEXT-JUSTIFY-LEFT (0), TEXT-JUSTIFY-RIGHT (1), TEXT-JUSTIFY-CENTER (2), TEXT-JUSTIFY-FILL (3) }
    pdb.gimp_text_layer_set_justification(layer, TEXT_JUSTIFY_RIGHT)
    # caixa de texto do tamanho restante da tela
    width = img.width
    height = TEXTBOX_HEIGHT
    pdb.gimp_text_layer_resize(layer, width, height)

def load_title_textbox(img, title):
    # nova camada pro titulo
    drawable = None
    x = 500
    y = 40
    text_to_show = "\"" + title + "\""
    border = 10
    antialias = True
    size = 72.0
    size_type = PIXELS
    fontname = "Eastman Condensed Trial Ultra-Bold Condensed"
    layer = pdb.gimp_text_fontname(img, drawable, x, y, text_to_show, border, antialias, size, size_type, fontname)
    # caixa de texto do tamanho restante da tela
    width = 450
    height = 500
    pdb.gimp_text_layer_resize(layer, width, height)

def load_pregador(img, image_pregador, toggle_cubism_effect):
    layer_pregador = pdb.gimp_file_load_layer(img, image_pregador)
    parent = None
    position = 0
    pdb.gimp_image_insert_layer(img, layer_pregador, parent, position)

    brightness = 0.0
    contrast = 0.15
    pdb.gimp_drawable_brightness_contrast(layer_pregador, brightness, contrast)

    new_height = 560

    if (toggle_cubism_effect):
        tile_saturation = 5.0
        tile_size = 22.0
        background_color = 0
        pdb.plug_in_cubism(img, layer_pregador, tile_size, tile_saturation, background_color)

    new_width = (new_height * layer_pregador.width) / layer_pregador.height
    local_origin = True
    pdb.gimp_layer_scale(layer_pregador, new_width, new_height, local_origin)
    pdb.gimp_layer_set_offsets(layer_pregador, 0, 0)

def load_logo_culto(img, image_path):
    image_logo_culto = image_path + "/background/logo_culto.png"
    layer = pdb.gimp_file_load_layer(img, image_logo_culto)
    parent = None
    position = 0
    pdb.gimp_image_insert_layer(img, layer, parent, position)

def startup(title, image_path, text_color, pregador):
    width = 960
    height = 540
    img = gimp.Image(width, height, RGB)

    load_background(img, image_path)

    # selecionar cor
    gimp.set_foreground(text_color)

    image_pregador = image_path + "/recortes/felipe"+ str(randint(1, 36)).zfill( 3)  +".png"
    with_cubism = True
    load_pregador(img, image_pregador, with_cubism)
    without_cubism = False
    load_pregador(img, image_pregador, without_cubism)
    load_title_textbox(img, title)
    load_pregador_textbox(img, pregador)
    load_logo_culto(img, image_path)

    gimp.Display(img)


register(
    "python-fu-startup",
    "Importation Demonstration",
    "Merely registers a plug-in",
    "Ruither Borba", "Ruither Borba", "2022",
    "Nova Miniatura Mosaico",
    "",  # does not require an image
    [
       (PF_STRING, "title", "Texto Thumb", ""),
       (PF_STRING, "image_path", "Pasta Pregadores", "/home/ruither/Dropbox/Mosaico - Slides/imagens/miniaturas-youtube"),
       (PF_COLOR, "text_color", "Cor do Texto", (0.0, 0.0, 0.0)),
       (PF_STRING, "pregador", "Nome Pregador", "Pr. Felipe Lobo")
    ],
    [],
    startup,
    menu="<Image>/File/Create")  # second item is menu location

main()
