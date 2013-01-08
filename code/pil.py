
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

Note: this program requires the Python Imaging Library (PIL)
and the ImageTk module.  On Ubuntu, you can install the
python-imaging and python-imaging-tk packages.

"""

import Image
import ImageDraw
import ImageTk
import Gui

image = Image.new(mode='1', size=[300, 200], color=255)
draw = ImageDraw.Draw(image)

x, y, width, height = 100, 50, 100, 100
draw.rectangle([x, y, x+width, y+height], outline=0, fill=128)

gui = Gui.Gui()
button = gui.bu(command=gui.quit, relief=Gui.FLAT)

tkpi = ImageTk.PhotoImage(image)
button.config(image=tkpi)

gui.mainloop() 
image.save('image.gif')
