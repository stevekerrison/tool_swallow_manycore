Swallow Manycore tools
.......

:Version:  0.0.1

:Status:  Alpha

:Maintainer:  https://github.com/stevekerrison

:Description:  Build tools and sample code for University of Bristol "Swallow" many-core board arrays


Key Features
============

* Allow mesh networks of Swallow to be assembled
* Fast, parallel compilation of many-core code
* Regular XMOS channel support plus a hybrid streaming channel implementation

To Do
=====

* Better documentation

Known Issues
============

* JTAG loading of many cores is (unavoidably) slow
* Debug symbols missing from final XE file

Required Repositories
=====================

None - tool_xesection is a submodule, however

Usage
=====

#. Make sure the tools folder from this repository is in your PATH
#. Write some code (don't use the repository - create a suitable directory structure for yourself)
#. Write a many-core main file (an example is in the code directory - it's a bit buggy)
#. Old style: run `Swallow-mcsc.py manycoremain.xc board.cfg [extra files] [compiler parameters]`
 - board.cfg is a file describing the board layout, you can generate them with Swallow-routegen.py
#. New style: `run swallow-mcsc.py manycoremain.xc [extra files] [compiler parameters]`
 - No board.cfg needed, SGB file is produced, booting is done over TFTP, not xrun
 
To TFTP:

* `tftp 192.168.128.3` (or IP of the ethernet device controlling the grid)
* `mode binary`
* `put myfile.sgb`

Running `get` on any filename will return the board configuration as the string "w,h" to the filename requested.


.sgb File Format
================

SGB (Swallow Grid Binary) files produced by swallow-mcsc.py can boot a swallow grid via TFTP. Here is a description
of the file format.

An SGB file contains a group of binary format memory images that can be loaded onto cores in the grid, along with some
additional sections for configuration purposes. Creating SGB files is relatively straightforward and uses the XMOS
compiler tools and standard binutils to do a lot of its work.

An SGB file starts with a magic number 0x5b followed by a version byte of 0.
The next field "reset" is an 8-bit field, which is set to 1 if the grid
should be reset prior to loading images (which is usually the case).
"cores" is a 16-bit field expressing the number of cores used in the system, *including holes* (nodes with no image).
"PLL" is an 8-bit field which states how many PLL settings follow (this is currently always 0 as the format for PLL
settings is not described yet).

+-------------+---------------+-------------+--------------+------------+
|Magic (8-bit)|Version (8-bit)|Reset (8-bit)|Cores (16-bit)|PLL (8-bit) |
+-------------+---------------+-------------+--------------+------------+
|    0x5b     |       0       |     0/1     | num. cores   | 0 (for now)|
+-------------+---------------+-------------+--------------+------------+

Then, for the number of cores in the image, is a section containing a 32-bit value describing the offset of the image
in the grid (contiguous core reference), and how many words are in the image as a 32-bit value, followed by the image
data.

+---------------+---------------+---------------+
|Offset (32-bit)|Length (32-bit)|Image (L-words)|
+---------------+---------------+---------------+
|       O       |       L       |   Code        |
+---------------+---------------+---------------+

Finally, 0xffffffff terminates the SGB file.

Support
=======

Fork, fix and pull-request! Feel free to contact maintainer with any questions.
