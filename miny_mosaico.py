#!/usr/bin/env python

from gimpfu import *
from random import randint

def darken_layer(img, layer, base_directory):
    pdb.gimp_layer_set_opacity(layer, 50)
    brightness = -0.9
    contrast = 0.15
    pdb.gimp_drawable_brightness_contrast(layer, brightness, contrast)
    load_image(img, base_directory + "/background/textura_ebd.png")

    hue_range = 0.0
    hue_offset = 0.0
    lightness = 0.0
    saturation = -100.0
    overlap = 0.0
    pdb.gimp_drawable_hue_saturation(layer, hue_range, hue_offset, lightness, saturation, overlap)

def lighten_layer(img, layer, base_directory):
    pdb.gimp_layer_set_opacity(layer, 50)

DARK_GRAY = (0.239, 0.239, 0.239)
WHITE = (1.0, 1.0, 1.0)
THUMB_TYPE_CONFIG = {
    "ebd": { "background_color" : DARK_GRAY, "logo": "logo_ebd", "effect": darken_layer, "override_text_color": WHITE },
    "culto": { "background_color" : WHITE, "logo": "logo_culto", "effect": lighten_layer, "override_text_color": None}
}

def load_background(img, base_directory, background_name, thumb_config):
    # background layer
    background = gimp.Layer(img, "Background", img.width, img.height,
                            RGB_IMAGE, 100, NORMAL_MODE)

    pdb.gimp_context_set_background(thumb_config['background_color'])
    background.fill(BACKGROUND_FILL)
    img.add_layer(background, 0)

    image_background = base_directory + "/background/" + background_name + ".png"
    layer_background = pdb.gimp_file_load_layer(img, image_background)
    parent = None
    position = 0
    pdb.gimp_image_insert_layer(img, layer_background, parent, position)
    thumb_config["effect"](img, layer_background, base_directory)

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
    width = img.width -10
    height = TEXTBOX_HEIGHT
    pdb.gimp_text_layer_resize(layer, width, height)

def load_title_textbox(img, title, size):
    # nova camada pro titulo
    drawable = None
    x = 500
    y = 40
    text_to_show = title
    border = 10
    antialias = True
    size = size
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
        hue_range = 0.0
        hue_offset = 30.0
        lightness = 0.0
        saturation = 100.0
        overlap = 0.0
        pdb.gimp_drawable_hue_saturation(layer_pregador, hue_range, hue_offset, lightness, saturation, overlap)

    new_width = (new_height * layer_pregador.width) / layer_pregador.height
    local_origin = True
    pdb.gimp_layer_scale(layer_pregador, new_width, new_height, local_origin)
    pdb.gimp_layer_set_offsets(layer_pregador, 0, 0)

def load_image(img, image_path):
    layer = pdb.gimp_file_load_layer(img, image_path)
    parent = None
    position = 0
    pdb.gimp_image_insert_layer(img, layer, parent, position)

def startup(title, headline, text_color, pregador, picture_pregador, photo_count, random_picture, thumb_type, base_directory, background_name):
    width = 960
    height = 540
    img = gimp.Image(width, height, RGB)

    load_background(img, base_directory, background_name, THUMB_TYPE_CONFIG[thumb_type])

    # selecionar preto para fazer sombra
    gimp.set_foreground((0.0, 0.0, 0.0))
    picture_name = picture_pregador + str(randint(1, photo_count)).zfill(3) if random_picture else picture_pregador
    image_pregador = base_directory + "/recortes/" + picture_name  +".png"
    with_cubism = True
    load_pregador(img, image_pregador, with_cubism)
    without_cubism = False
    load_pregador(img, image_pregador, without_cubism)
    load_title_textbox(img, headline, 100.0)

    # selecionar cor
    color_override = THUMB_TYPE_CONFIG[thumb_type]["override_text_color"]
    gimp.set_foreground(text_color if color_override is None else color_override)
    load_title_textbox(img, "\"" + title + "\"", 72.0)
    load_pregador_textbox(img, pregador)

    load_image(img, base_directory + "/background/" + THUMB_TYPE_CONFIG[thumb_type]["logo"] + ".png")

    gimp.Display(img)


register(
    "python-fu-startup",
    "Nova Miniatura Mosaico",
    "Merely registers a plug-in",
    "Ruither Borba", "Ruither Borba", "2022",
    "Nova Miniatura Mosaico",
    "",  # does not require an image
    [
        (PF_STRING, "title", "Texto Thumb", ""),
        (PF_STRING, "headline", "Termo de Destaque", ""),
        (PF_COLOR, "text_color", "Cor do Texto", (0.0, 0.0, 0.0)),
        (PF_STRING, "pregador", "Nome Pregador", "Pr. Felipe Lobo"),
        (PF_STRING, "foto_pregador", "Foto Pregador", "felipe"),
        (PF_INT, "photo_count", "Quantidade de fotos desse pregador", 38),
        (PF_BOOL, "random_picture", "Foto aleatoria", 1),
        (PF_RADIO, "thumb_type", "Tipo Miniatura", "culto",
          (("Culto", "culto"), ("EBD", "ebd"))),
        (PF_DIRNAME, "base_directory", "Pasta Miniaturas", "/home/ruither/Dropbox/Mosaico - Slides/imagens/miniaturas-youtube"),
        (PF_STRING, "background_name", "Imagem de Fundo (PNG)", "fundo_pregacao")
    ],
    [],
    startup,
    menu="<Image>/File/Create")  # second item is menu location

main()
