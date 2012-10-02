# -*- mode: python; coding: utf-8 -*-
#
# Pigment Python binding text example
#
# Copyright © 2006, 2007, 2008 Fluendo Embedded S.L.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# Author: Loïc Molinari <loic@fluendo.com>

import sys, pgm, gobject

# Align the text function of the button pressed
def on_button_press(viewport, event, gl, txt):
    if event.type == pgm.BUTTON_PRESS:
        if event.button == pgm.BUTTON_LEFT:
            txt.alignment = pgm.TEXT_ALIGN_LEFT
        elif event.button == pgm.BUTTON_MIDDLE:
            txt.alignment = pgm.TEXT_ALIGN_CENTER
        elif event.button == pgm.BUTTON_RIGHT:
            txt.alignment = pgm.TEXT_ALIGN_RIGHT

# Terminate the mainloop on a delete event
def on_delete(viewport, event):
    pgm.main_quit()

def main(args):
    # GObject threads initialization
    gobject.threads_init()

    # OpenGL viewport creation
    gl = pgm.viewport_factory_make('opengl')
    gl.title = '60ème Festival de Cannes'

    # Canvas and text drawable creation
    cvs = pgm.Canvas()
    fd = open('about.html')
    txt = pgm.Text(fd.read())
    fd.close()

    # Bind the canvas to the OpenGL viewport
    gl.set_canvas(cvs)

    # Text properties tweaking
    txt.size = (1.5, 1.5)
    txt.position = (1.25, 0.75, 0.0)
    txt.fg_color = (220, 220, 220, 255)
    txt.bg_color = (20, 20, 20, 255)

    # Change the size of the text
    txt.font_height = 1/17.0 #  1/17 to ensure around 16 lines of text.

    # A drawable needs to be shown
    txt.show()

    # Add it to the middle layer of the canvas
    cvs.add(pgm.DRAWABLE_MIDDLE, txt)

    # Let's connect our callbacks and start the mainloop
    gl.connect('button-press-event', on_button_press, gl, txt)
    gl.connect('delete-event', on_delete)
    gl.show()
    pgm.main()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
