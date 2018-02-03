#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""RepRap G-code flavor to .makerbot converter"""

# Copyright (C) 2018 seeburger

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# Classic :) :m
# TODO: this is stupid
# """ Not a generator because that would be stupid. """


import os
import sys
import getopt

import math
import re
import base64
import json
import zipfile


class GenericGcodeParser(object):
    """Generic parser for G-code, that will parse and convert the moves to the makerbot JSON format"""

    # These constants contain base64 encoded pre-generated PNG thumbnails with the phrase "No preview"
    THUMBNAIL_SMALL = 'iVBORw0KGgoAAAANSUhEUgAAADcAAAAoCAYAAABaW2IIAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QoXEBcPH6gvdwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAClklEQVRo3u3YPUgjURSG4ffGn8JgoYNaRiQgGFBEQTEjkSmDEBARiaCVlYVFqoAE1MJWazvTiYM/haQJA4KIKEgcUFGQQOwGQYg4lZ4tFsKKG13XhV2W+1UzczmHebjnTjFKRIT/NAH+42icxmmcxmmcxmmcxmmcxmmcxv2B3N3doZRCKUVrayurq6tf6nd1dcXk5OTXX0x+yNHRkdTX10uxWBQRkfn5eTk5OZGPUiqVJBqNiojIzc2NGIYh5XJZ/nbe7JxpmiwvL//+KAS+tywUCoyOjmKaJolEAoB0Oo1hGIRCIfb39wFIpVLs7e0B4Ps+PT09XF5evtq5n9UtLi6ys7ODiNDS0kIul+P5+Zn+/v7qY9nb28vj4yPX19eVZ57nMTw8TDAYJB6P4/v+G9Th4SFKKQYGBkin0wSDQQqFAhsbG+zu7pLL5SgWi9ze3uI4DgsLCwDMzMyQzWYB2N7eJpFIoJSq9K1WZ1kW+Xye8/NzhoaGyOfznJ6e0tfX9/6Zy2QyLC0tVe7X19cZGxvj/v6eSCTC1tbWm5poNIqI4HkeqVQKgFgsRkdHBwCu67K5uUlzczPhcJizszPK5TLd3d2USiUeHh7IZrNMT0+/6lutbnBwkOPjYxzHYW5ujouLCxzHwbKs93FdXV3U1NTgum7VsfuV1NbWVq4jkQjJZBLP83h5eUFEaGxsBGBiYoK1tTWenp4Ih8OvelSrq6urwzAMbNvGNE2ampqwbZuRkZGPv5aZTIaDgwMAZmdnsW0bwzBwXZfx8fFPn8V4PE4oFKKzsxOlFO3t7ZW1qakpVlZWSCaTn6qzLItAIEBDQwOxWAzf92lra6usK/1rT+M0TuM0TuM0TuM0TuM0TuM0TuP+tXwDLyi+wN+kVSQAAAAASUVORK5CYII='
    THUMBNAIL_MEDIUM = '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'
    THUMBNAIL_LARGE = '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'

    g_code = []
    duration = 0


    def __init__(self, g_code):
        self.g_code = g_code

    def generate_toolpath_json(self):
        """Generate the toolpath JSON from the G-code"""

        result = [
            # These steps will ensure that nozzle is at 0/0/0 where it would be expected by the G-code, after
            # doing the anchor move that is done by the firmware

            # Retract
            {'command': {'function': 'move', 'parameters': {'x': 0, 'y': 0, 'z': 0.2, 'a': -0.5, 'feedrate': 50}, 'tags': [], 'metadata': {'relative': {'x': True, 'y': True, 'z': False, 'a': False}}}},
            # Lift nozzle
            {'command': {'function': 'move', 'parameters': {'x': 0, 'y': 0, 'z': 0.3, 'a': -0.5, 'feedrate': 23}, 'tags': [], 'metadata': {'relative': {'x': True, 'y': True, 'z': False, 'a': False}}}},
            # Move to 0/0
            {'command': {'function': 'move', 'parameters': {'x': 0, 'y': 0, 'z': 0.3, 'a': -0.5, 'feedrate': 150}, 'tags': [], 'metadata': {'relative': {'x': False, 'y': False, 'z': False, 'a': False}}}},
            # Undo retract and lift
            {'command': {'function': 'move', 'parameters': {'x': 0, 'y': 0, 'z': 0.0, 'a': 0.0, 'feedrate': 30}, 'tags': [], 'metadata': {'relative': {'x': False, 'y': False, 'z': False, 'a': False}}}}
        ]

        current_x = 0.0
        current_y = 0.0
        current_z = 0.0
        current_a = 0.0
        last_x = 0.0
        last_y = 0.0
        last_z = 0.0
        relative_a = 0.0
        current_feedrate = 0

        for line in self.g_code:
            fields = line.split(' ')
            command = fields[0]

            # Move
            if command == 'G1':
                for field in fields[1:]:
                    if field.startswith('X'):
                        last_x = current_x
                        current_x = float(field[1:])
                    if field.startswith('Y'):
                        last_y = current_y
                        current_y = float(field[1:])
                    if field.startswith('Z'):
                        last_z = current_z
                        current_z = float(field[1:])
                    if field.startswith('E'):
                        current_a = relative_a + float(field[1:])
                    if field.startswith('F'):
                        current_feedrate = float(field[1:])/60.0

                if current_x != last_x or current_y != last_y or current_z != last_z:
                    distance = math.sqrt(pow((current_x-last_x), 2) + pow((current_y-last_y), 2) + pow((current_z-last_z), 2))
                    self.duration = self.duration + (distance / current_feedrate)

                result.append(
                    {
                        'command': {
                            'function': 'move',
                            'parameters': {
                                'x': current_x, # X
                                'y': current_y, # Y
                                'z': current_z, # Z
                                'a': current_a, # (A)mount
                                'feedrate': current_feedrate # Feedrate mm/s
                            },
                            'tags': [],
                            'metadata': {
                                'relative': {
                                    'x': False,
                                    'y': False,
                                    'z': False,
                                    'a': False
                                }
                            }
                        }
                    }
                )
            # Reset axis
            elif command == 'G92':
                for field in fields[1:]:
                    if field.startswith('E'):
                        relative_a = current_a
            # Fan on
            elif command == 'M106':
                result.append(
                    {
                        'command': {
                            'function': 'toggle_fan',
                            'parameters': {
                                'value': True,
                            },
                            'tags': [],
                            'metadata': {}
                        }
                    }
                )

                for field in fields[1:]:
                    if field.startswith('S'):
                        fan_speed = (1/255) * float(field[1:])
                result.append(
                    {
                        'command': {
                            'function': 'fan_duty',
                            'parameters': {
                                'value': fan_speed,
                            },
                            'tags': [],
                            'metadata': {}
                        }
                    }
                )
            # Fan off
            elif command == 'M107':
                result.append(
                    {
                        'command': {
                            'function': 'toggle_fan',
                            'parameters': {
                                'value': False,
                            },
                            'tags': [],
                            'metadata': {}
                        }
                    }
                )

        if len(result) == 4:
            raise RuntimeError('Failed to parse G-code')

        return json.dumps(result)

    def generate_meta_json(self, anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature):
        """Generate the meta JSON from the arguments"""

        result = {
            'miracle_config': {
                'anchorExtrusionAmount': anchor_amount,
                'anchorExtrusionSpeed': anchor_speed,
                'anchorWidth': anchor_width
            },
            'printer_settings': {
                'materials': [
                    'PLA'
                ],
                'layer_height': layer_height,
                'infill': infill / 100.0,
                'shells': shells,
                'support': support,
                'raft': raft,
            },
            'duration_s': int(self.duration),
            'extrusion_distance_a_mm': filament_used_mm,
            'extrusion_distance_mm': filament_used_mm,
            'extrusion_mass_a_grams': filament_used_g * density,
            'extrusion_mass_g': filament_used_g * density,
            'toolhead_0_temperature': temperature
        }

        return json.dumps(result)

    def generate_thumbnails(self, base_color, color, layer_count):
        """Generate thumbnails from the G-code"""

        try:
            import io

            import numpy as np
            import matplotlib as mpl
            import mpl_toolkits.mplot3d as mplot3d
            import matplotlib.pyplot as plt


            lines = []
            line_xs = []
            line_ys = []
            line_zs = []

            relative_e = 0.0
            last_e = 0.0
            current_x = 0.0
            current_y = 0.0
            current_z = 0.0
            current_e = 0.0

            for line in self.g_code:
                fields = line.split(' ')
                command = fields[0]

                # Move
                if command == 'G1':
                    for field in fields[1:]:
                        if field.startswith('X'):
                            current_x = float(field[1:])
                        if field.startswith('Y'):
                            current_y = float(field[1:])
                        if field.startswith('Z'):
                            current_z = float(field[1:])
                        if field.startswith('E'):
                            current_e = relative_e + float(field[1:])

                    # Retraction / Travel move (Start a new line segment)
                    if current_e <= last_e:
                        # If there are at least 2 points, otherwise there won't be a line
                        if len(line_xs) > 1:
                            lines.append([np.array(line_xs), np.array(line_ys), np.array(line_zs)])
                            line_xs = []
                            line_ys = []
                            line_zs = []
                            # If the extrusion amount is the same, record the point as start for the next line
                            if current_e == last_e:
                                line_xs.append(current_x)
                                line_ys.append(current_y)
                                line_zs.append(current_z)
                        # If not skip the one point, because that is a travel move only without unretract
                        else:
                            line_xs = []
                            line_ys = []
                            line_zs = []
                    # Extrusion (Keep adding points to the line)
                    else:
                        line_xs.append(current_x)
                        line_ys.append(current_y)
                        line_zs.append(current_z)

                    last_e = current_e
                # Reset axis
                elif command == 'G92':
                    for field in fields[1:]:
                        if field.startswith('E'):
                            relative_e = current_e

            fig = plt.figure(dpi=100)
            axis = fig.gca(projection='3d')

            # Plot the lines in different colors
            layer = 1
            col = [0, 0, 0]
            last_z = 0.0
            for line in lines:
                axis.plot(line[0], line[1], line[2], color=col, linewidth=1, antialiased=True)
                if line[2][0] > last_z:
                    last_z = line[2][0]

                    if layer % layer_count == 0:
                        col = color
                    else:
                        col = base_color

                    layer = layer + 1

            # Remove labels, ticks etc.
            axis.spines['top'].set_visible(False)
            axis.spines['right'].set_visible(False)
            axis.spines['bottom'].set_visible(False)
            axis.spines['left'].set_visible(False)
            plt.axis('off')
            plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off')

            # "Center" the object, and scale the axes equally
            x_limits = axis.get_xlim3d()
            y_limits = axis.get_ylim3d()
            z_limits = axis.get_zlim3d()
            x_range = abs(x_limits[1] - x_limits[0])
            x_middle = float(sum(x_limits)) / max(len(x_limits), 1)
            y_range = abs(y_limits[1] - y_limits[0])
            y_middle = float(sum(y_limits)) / max(len(y_limits), 1)
            z_range = abs(z_limits[1] - z_limits[0])
            z_middle = float(sum(z_limits)) / max(len(z_limits), 1)
            plot_radius = 0.3 * max([x_range, y_range, z_range])
            axis.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
            axis.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
            axis.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

            # Generate and save the small thumbnail
            buffer = io.BytesIO()
            fig.set_size_inches(63.0/100, 44.0/100) # 55x40@100
            plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
            buffer.seek(0)
            small = buffer.read()

            # Generate and save the medium thumbnail
            buffer = io.BytesIO()
            fig.set_size_inches(134.0/100, 96.0/100) # 110x80@100
            plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
            buffer.seek(0)
            medium = buffer.read()

            # Generate and save the large thumbnail
            buffer = io.BytesIO()
            fig.set_size_inches(405.0/100, 251.0/100) # 320x200@100
            plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
            buffer.seek(0)
            large = buffer.read()

        except ImportError:
            small = base64.decodebytes(bytes(self.THUMBNAIL_SMALL, encoding='UTF-8'))
            medium = base64.decodebytes(bytes(self.THUMBNAIL_MEDIUM, encoding='UTF-8'))
            large = base64.decodebytes(bytes(self.THUMBNAIL_LARGE, encoding='UTF-8'))

        return (small, medium, large)


class Slic3rConverter(GenericGcodeParser):
    """Specific converter for Slic3r, that will parse and convert the meta information to the makerbot JSON format"""

    def generate_meta_json(self, anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature):
        """Generate the meta JSON from the G-code"""

        matches = [False, False, False, False, False, False, False]

        for line in self.g_code:
            fields = line.split(' ')
            command = fields[0]

            # Material used (g) and (mm)
            filament_used_match = re.match(r'; filament used = ([0-9\.]+)mm \(([0-9\.]+)cm3\)', line)
            if filament_used_match:
                filament_used_g = float(filament_used_match.group(2))
                filament_used_mm = float(filament_used_match.group(1))
                matches[0] = True

            # Layer height
            layer_height_match = re.match(r'; layer_height = ([0-9\.]+)', line)
            if layer_height_match:
                layer_height = float(layer_height_match.group(1))
                matches[1] = True

            # Infill
            infill_match = re.match(r'; fill_density = ([0-9\.]+)%', line)
            if infill_match:
                infill = float(infill_match.group(1))
                matches[2] = True

            # Shells
            shell_match = re.match(r'; perimeters = ([0-9]+)', line)
            if shell_match:
                shells = int(shell_match.group(1))
                matches[3] = True

            # Support
            support_match = re.match(r'; support_material = ([0-9]+)', line)
            if support_match:
                support = bool(int(support_match.group(1)) > 0)
                matches[4] = True

            # Raft
            raft_match = re.match(r'; raft_layers = ([0-9]+)', line)
            if raft_match:
                raft = bool(int(raft_match.group(1)) > 0)
                matches[5] = True

            # Temperature
            if command == 'M104':
                for field in fields[1:]:
                    if field.startswith('S') and int(field[1:]) > 0:
                        temperature = int(field[1:])
                        matches[6] = True

        if False in matches:
            raise RuntimeError('Failed to extract meta information from G-code')

        return super(Slic3rConverter, self).generate_meta_json(anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature)


class ManualConverter(GenericGcodeParser):
    """Manual converter, that will convert the meta information to the makerbot JSON format"""

    def generate_meta_json(self, anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature):
        """Generate the meta JSON from the arguments"""

        if None in [filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature]:
            raise ValueError('Missing required arguments for manual mode')

        return super(ManualConverter, self).generate_meta_json(anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature)


def usage():
    """Print usage information"""

    print('convert_makerbot.py - RepRap G-code flavor to .makerbot converter')
    print('')
    print('Usage: convert_makerbot.py [options] </path/to/object.gcode> [</path/to/object.makerbot>]')
    print('')
    print('')
    print('Generic options:')
    print('')
    print('[-f]  Force overwriting of the .makerbot file             (Default: false)')
    print('')
    print('[-m]  Mode to gather meta information (slic3r, manual)    (Default: slic3r)')
    print('')
    print('[-x]  Change color every X layers                         (Default: 3)')
    print('[-c]  Color to change to in R,G,B                         (Default: 0.3,0.85,0.1 [r,g,b])')
    print('[-b]  Basecolor in R,G,B                                  (Default: 0,0,0 [r,g,b])')
    print('')
    print('[-a]  Anchor amount                                       (Default: 5.0 [mm])')
    print('[-s]  Anchor speed                                        (Default: 2.0 [mm/s])')
    print('[-w]  Anchor width                                        (Default: 2.0 [mm])')
    print('')
    print('[-d]  Density of the material used for weight estimation  (Default: 1.25 [g/cm^3])')
    print('')
    print('[-h]  Print this help message')
    print('')
    print('Options for the manual meta information mode:')
    print('')
    print(' -l   Layer height                                        (E.g. 0.2 [mm])')
    print(' -i   Infill percentage                                   (E.g. 50 [%])')
    print(' -e   Shells                                              (E.g. 3)')
    print(' -u   Support                                             (E.g. true)')
    print(' -r   Raft                                                (E.g. false)')
    print(' -t   Temperature                                         (E.g. 215 [°C])')
    print(' -n   Filament used length                                (E.g. 4639.7 [mm])')
    print(' -g   Filament used mass                                  (E.g. 12.3 [g])')
    print('')


def handle_error(message):
    """Handle errors"""

    print('>> ERROR occured: %s' % message)
    sys.exit(1)


def main(force=False):
    """Main function"""

    input_file = None
    output_file = None

    anchor_amount = 5.0
    anchor_speed = 2.0
    anchor_width = 2.0
    base_color = [0, 0, 0]
    color = [0.3, 0.85, 0.1]
    density = 1.25
    filament_used_g = None
    filament_used_mm = None
    layer_count = 3
    layer_height = None
    mode = 'slic3r'
    infill = None
    shells = None
    support = None
    raft = None
    temperature = None

    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'a:b:c:d:e:fg:hi:l:m:n:r:s:t:u:w:x:')
    except getopt.GetoptError as err:
        handle_error(str(err))

    for option, argument in options:
        if option == '-a':
            anchor_amount = float(argument)
        if option == '-b':
            base_color = [float(n) for n in argument.split(',')]
        if option == '-c':
            color = [float(n) for n in argument.split(',')]
        if option == '-d':
            density = float(argument)
        if option == '-e' and argument.isdigit():
            shells = int(argument)
        if option == '-f':
            force = True
        if option == '-g':
            filament_used_g = float(argument)
        if option == '-h':
            usage()
            sys.exit(0)
        if option == '-i' and argument.isdigit():
            infill = int(argument)
        if option == '-l':
            layer_height = float(argument)
        if option == '-m' and argument in ('slic3r', 'manual'):
            mode = argument
        if option == '-n':
            filament_used_mm = float(argument)
        if option == '-r':
            if argument == 'true':
                raft = True
            elif argument == 'false':
                raft = False
        if option == '-s':
            anchor_speed = float(argument)
        if option == '-t' and argument.isdigit():
            temperature = int(argument)
        if option == '-u':
            if argument == 'true':
                support = True
            elif argument == 'false':
                support = False
        if option == '-w':
            anchor_width = float(argument)
        if option == '-x' and argument.isdigit():
            layer_count = int(argument)

    if len(arguments) < 1:
        handle_error('Missing input file name')

    input_file = arguments[0]

    if len(arguments) == 1:
        output_file = os.path.splitext(os.path.realpath(input_file))[0] + '.makerbot'
    elif len(arguments) == 2:
        output_file = arguments[1]
    else:
        handle_error('Unrecognized additional arguments: %s' % arguments[2:])

    if os.path.isfile(output_file) and force != True:
        handle_error('The makerbot file (%s) already exists and force (-f) was not specified' % output_file)

    try:
        g_code = open(input_file).read().splitlines()

        if mode == 'manual':
            converter = ManualConverter(g_code)
        elif mode == 'slic3r':
            converter = Slic3rConverter(g_code)

        toolpath_json = converter.generate_toolpath_json()
        meta_json = converter.generate_meta_json(anchor_amount, anchor_speed, anchor_width, density, filament_used_g, filament_used_mm, layer_height, infill, shells, support, raft, temperature)
        thumbnail_small, thumbnail_medium, thumbnail_large = converter.generate_thumbnails(base_color, color, layer_count)

        makerbot_file = zipfile.ZipFile(output_file, 'w')
        makerbot_file.writestr('meta.json', meta_json)
        makerbot_file.writestr('print.jsontoolpath', toolpath_json)
        makerbot_file.writestr('thumbnail_55x40.png', thumbnail_small)
        makerbot_file.writestr('thumbnail_110x80.png', thumbnail_medium)
        makerbot_file.writestr('thumbnail_320x200.png', thumbnail_large)
        makerbot_file.close()
    except Exception as err:
        handle_error(str(err))


if __name__ == '__main__':
    if 'force_convert_makerbot.py' in sys.argv[0]:
        main(True)
    else:
        main(False)
