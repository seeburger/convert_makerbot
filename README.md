# convert_makerbot - RepRap G-code flavor to .makerbot converter
---

This script will convert RepRap flavored G-code to a .makerbot file, which may be
printed on a MakerBot 3D Printer via an USB mass storage device.

The RepRap flavor has to be used, because it allows to control the fan speed,
which is impossible with the makerbot flavor.


## DISCLAIMER: This was only tested on a Replicator 5th generation with firmware version 1.9.2! It should also work with the Replicator Mini and the Replicator Z18, but I have __NOT__ tested it with those devices __NOR__ other firmware versions!
## Please be very careful if you are about to test this, as it might __DAMAGE__ your device. Always stay next to your device and be prepared to turn it off immediately in case something goes wrong. I am not responsible for any damage to your device.
## Using this script will void your warranty.

If you are successful at testing, please let me know and send me the device and
firmware version which you were using.


## Known working devices

- MakerBot Replicator 5th generation


## Known working firmware versions

- 1.9.2


## Requisites
---

- python3

If you want to have thumbnails rendered from the G-Code you will need some
additional python modules:

- numpy
- matplotlib


## Installation
---

Make sure all the requisites are installed. Download the script and place it
in a location of your choice and make it executable.

	chmod +x convert_makerbot.py


## Usage
---

This script is designed to be run as a [Slic3r](http://www.slic3r.org/)
post-processing script by default. If you intend to use this with any other
slicer, read the paragraph about the manual mode below.

### General

In general you need to make sure that, whatever slicer you use, the 0/0 (origin)
position is set to be in the __CENTER__ of the print bed. I am using Slic3r and set
the size of my print bed to 252 x 199 and the origin to 125 x 99. If you changed
the z-offset within the MakerBot software, I would suggest you set it to 0 and
use your slicer of choice to set the z-offset.

### Slic3r mode (default)

To use this script as a post-processing script, you have to put Slic3r into
`Expert` mode in the `Preferences`.

If you haven't done so already, you have to setup your printer in the `Printer
Settings` tab. Set the bed shape to the correct dimensions and origin in the
__CENTER__, as mentioned before. Make sure to select `RepRap` G-code flavor.

Also, I would suggest to create a symlink to or a copy of the script named
`force_convert_makerbot.py` for that case, otherwise it will only create the
makerbot file once, but won't overwrite it if you change something and you
export the same file again. Using the `-f` option, or any command line option
at all for that matter, is not possible with Slic3r, because Slic3r does not
permit to specify command line options for post-processing scripts.

Afterwards navigate to the `Print settings` tab. Now choose `Output options`
and enter the full path to the script (e.g. `/path/to/force_convert_makerbot.py`)
inside `Post-processing scripts`.

Now everything should be setup and if you `Export G-code` from the `Plater` you
should find an accompanying `.makerbot` file in the same directory where you
exported the G-code file to.

### Manual mode

If you are using anything other than Slic3r, you should be able to do so by
using the manual mode.

	convert_makerbot.py - RepRap G-code flavor to .makerbot converter

	Usage: convert_makerbot.py [options] </path/to/object.gcode> [</path/to/object.makerbot>]


	Generic options:

	[-f]  Force overwriting of the .makerbot file             (Default: false)

	[-m]  Mode to gather meta information (slic3r, manual)    (Default: slic3r)

	[-x]  Change color every X layers                         (Default: 3)
	[-c]  Color to change to in R,G,B                         (Default: 0.3,0.85,0.1 [r,g,b])
	[-b]  Basecolor in R,G,B                                  (Default: 0,0,0 [r,g,b])

	[-a]  Anchor amount                                       (Default: 5.0 [mm])
	[-s]  Anchor speed                                        (Default: 2.0 [mm/s])
	[-w]  Anchor width                                        (Default: 2.0 [mm])

	[-d]  Density of the material used for weight estimation  (Default: 1.25 [g/cm^3])

	[-h]  Print this help message

	Options for the manual meta information mode:

	 -l   Layer height                                        (E.g. 0.2 [mm])
	 -i   Infill percentage                                   (E.g. 50 [%])
	 -e   Shells                                              (E.g. 3)
	 -u   Support                                             (E.g. true)
	 -r   Raft                                                (E.g. false)
	 -t   Temperature                                         (E.g. 215 [°C])
	 -n   Filament used length                                (E.g. 4639.7 [mm])
	 -g   Filament used mass                                  (E.g. 12.3 [g])

You have to specify a path to an input G-code file which should be converted.
The G-code of the input file has to be in the RepRap flavor.

If you do not specify a path to an output file, the filename of the input file
will be used but the file extension will be changed to `.makerbot`. So if you
call the script with an input file named `foo.gcode` the output file will be
named `foo.makerbot` and will be created in the same directory as the input
file. By default the output file will not be overwritten. If you want that, you
may either specify the `-f` option, or name the script
`force_convert_makerbot.py`.

You also have to provide values for every option that is listed for the manual
meta information mode.

	convert_makerbot.py -m manual -l 0.2 -i 50 -e 3 -u true -r false -t 215 -n 4639.7 -g 12.3 my_object.gcode

#### Thumbnail colors

Thumbnails are rendered by parsing the G-code and generating a graph to plot
with matplotlib. Layers get colored by the base color (`-b`), changing the
color of every x-th (`-x`) layer to color (`-c`) to create some depth in the
graph.

#### Anchor

The "anchor" move is done by the firmware after homing. It's that move where
the print head starts printing a small line to the left edge and afterwards
starts printing the object. The parameters may be changed but should not
require a change, as those are the default values used by the firmware.


## Known limitations
---

The only limitation that is currently known is that changing the temperature
mid-print is not possible, as the firmware does not support this.


## License
---

Copyright (C) 2018 seeburger

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
