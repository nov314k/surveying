import ezdxf
import yaml
from datetime import datetime


def distance_to_first_standard_value(coord):
    limit = 100
    while (coord >= limit):
        limit += 100
    return limit - coord


def add_leading_zeros(number):
    if number < 10:
        return "00" + str(number)
    elif number < 100:
        return "0" + str(number)
    return number


with open('settings.yaml', 'r') as stream:
    try:
        file = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
        print(ex)

print('''
This is DXF Drawing Frame Generator.
Please provide required information,
or hit Enter to load information from settings.yaml.
''')

dwg = ezdxf.new(file['settings']['dwg_standard'])
msp = dwg.modelspace()

aux = input("Enter x coordinate: ")
if not aux:
    value_x = file['settings']['value_x']
else:
    value_x = int(aux)

aux = input("Enter y coordinate: ")
if not aux:
    value_y = file['settings']['value_y']
else:
    value_y = int(aux)

aux = input("Enter frame width : ")
if not aux:
    frame_width = file['settings']['frame_width']
else:
    frame_width = int(aux)

aux = input("Enter frame height: ")
if not aux:
    frame_height = file['settings']['frame_height']
else:
    frame_height = int(aux)

origin_x = value_x
origin_y = value_y
layer_name = file['settings']['layer_name']
tick_spacing = file['settings']['tick_spacing']
x_text_alignment = file['settings']['x_text_alignment']
y_text_alignment = file['settings']['y_text_alignment']
save_as_filename = file['settings']['save_as_filename']

text_height = file['settings']['text_height']
line_to_line_spacing = file['settings']['line_to_line_spacing']
axis_to_text_spacing = file['settings']['axis_to_text_spacing']
tick_half_size = file['settings']['tick_half_size']
digit_width_ratio = file['settings']['digit_width_ratio']

dwg.layers.new(name=layer_name, dxfattribs={'color': 0})
line_attribs = {'layer': layer_name}
x_text_attribs = {'height': text_height, 'layer': layer_name, 'rotation': 270}
y_text_attribs = {'height': text_height, 'layer': layer_name}

msp.add_line(
    (origin_x, origin_y),
    (origin_x + frame_width, origin_y),
    dxfattribs=line_attribs)
msp.add_line(
    (origin_x + frame_width, origin_y),
    (origin_x + frame_width, origin_y + frame_height),
    dxfattribs=line_attribs)
msp.add_line(
    (origin_x + frame_width, origin_y + frame_height),
    (origin_x, origin_y + frame_height),
    dxfattribs=line_attribs)
msp.add_line(
    (origin_x, origin_y + frame_height),
    (origin_x, origin_y),
    dxfattribs=line_attribs)

x_text_3 = add_leading_zeros(value_x % 1000)
x_text_2 = add_leading_zeros((value_x // 1000) % 1000)
x_text_1 = ((value_x // 1000) // 1000) % 1000

msp.add_text(x_text_3, dxfattribs=x_text_attribs).set_pos(
    (origin_x + 1 * line_to_line_spacing + 1 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)
msp.add_text(x_text_2, dxfattribs=x_text_attribs).set_pos(
    (origin_x + 2 * line_to_line_spacing + 2 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)
msp.add_text(x_text_1, dxfattribs=x_text_attribs).set_pos(
    (origin_x + 3 * line_to_line_spacing + 3 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)

current_position = origin_x + distance_to_first_standard_value(int(x_text_3))
while current_position < origin_x + frame_width:
    msp.add_line(
        (current_position, origin_y),
        (current_position, origin_y + tick_half_size),
        dxfattribs=line_attribs)
    msp.add_text(int(x_text_3) + current_position - origin_x,
                 dxfattribs=x_text_attribs).set_pos(
        (current_position + 0.5 * text_height,
         origin_y - axis_to_text_spacing),
        align=x_text_alignment)
    current_position += tick_spacing

value_x_max = value_x + frame_width
x_text_3 = add_leading_zeros(value_x_max % 1000)
x_text_2 = add_leading_zeros((value_x_max // 1000) % 1000)
x_text_1 = ((value_x_max // 1000) // 1000) % 1000

msp.add_text(x_text_1, dxfattribs=x_text_attribs).set_pos(
    (origin_x + frame_width + 3 * line_to_line_spacing + 3 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)
msp.add_text(x_text_2, dxfattribs=x_text_attribs).set_pos(
    (origin_x + frame_width + 2 * line_to_line_spacing + 2 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)
msp.add_text(x_text_3, dxfattribs=x_text_attribs).set_pos(
    (origin_x + frame_width + 1 * line_to_line_spacing + 1 * text_height,
     origin_y - axis_to_text_spacing),
    align=x_text_alignment)

y_text_3 = add_leading_zeros(value_y % 1000)
y_text_2 = add_leading_zeros((value_y // 1000) % 1000)
y_text_1 = ((value_y // 1000) // 1000) % 1000

msp.add_text(y_text_3, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + 1 * line_to_line_spacing + 1 * text_height),
    align=y_text_alignment)
msp.add_text(y_text_2, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + 2 * line_to_line_spacing + 2 * text_height),
    align=y_text_alignment)
msp.add_text(y_text_1, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + 3 * line_to_line_spacing + 3 * text_height),
    align=y_text_alignment)

current_position = origin_y + distance_to_first_standard_value(int(y_text_3))
while current_position < origin_y + frame_height:
    msp.add_line(
        (origin_x + frame_width - tick_half_size, current_position),
        (origin_x + frame_width, current_position),
        dxfattribs=line_attribs)
    msp.add_text(int(y_text_3) + current_position - origin_y,
                 dxfattribs=y_text_attribs).set_pos(
        (origin_x + frame_width + axis_to_text_spacing,
         current_position + 0.5 * text_height),
        align=y_text_alignment)
    current_position += tick_spacing

value_y_max = value_y + frame_height
y_text_3 = add_leading_zeros(value_y_max % 1000)
y_text_2 = add_leading_zeros((value_y_max // 1000) % 1000)
y_text_1 = ((value_y_max // 1000) // 1000) % 1000

msp.add_text(y_text_3, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + frame_height + 1 * line_to_line_spacing + 1 * text_height),
    align=y_text_alignment)
msp.add_text(y_text_2, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + frame_height + 2 * line_to_line_spacing + 2 * text_height),
    align=y_text_alignment)
msp.add_text(y_text_1, dxfattribs=y_text_attribs).set_pos(
    (origin_x + frame_width + axis_to_text_spacing,
     origin_y + frame_height + 3 * line_to_line_spacing + 3 * text_height),
    align=y_text_alignment)

prefix = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')

file_name = ".\\___generated-dxfs\\" + prefix + save_as_filename
dwg.saveas(file_name)
print("\nDXF file generated: " + file_name + '\n')
aux = input("Press Enter to exit.")
