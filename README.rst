XMP16 Manycore tools
.......

:Version:  0.0.1

:Status:  Alpha

:Maintainer:  https://github.com/stevekerrison

:Description:  Build tools and sample code for University of Bristol "XMP16" many-core board arrays


Key Features
============

* Allow mesh networks of XMP16s to be assembled
* Fast, parallel compilation of many-core code
* Regular XMOS channel support plus a hybrid streaming channel implementation

To Do
=====

* XLink booting
* Better documentation

Known Issues
============

* JTAG loading of many cores is (unavoidably) slow
* Debug symbols missing from final XE file

Required Repositories
================

None - tool_xesection is a submodule, however

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
"cores" is a 16-bit field expressing the number of cores present in the SGB file.
"PLL" is an 8-bit field which states how many PLL settings follow (this is currently always 0 as the format for PLL
settings is not described yet).

+-------------+---------------+-------------+--------------+------------+
|Magic (8-bit)|Version (8-bit)|Reset (8-bit)|Cores (16-bit)|PLL (8-bit) |
+-------------+---------------+-------------+--------------+------------+
|    0x5b     |       0       |     0/1     | num. cores   | 0 (for now)|
+-------------+---------------+-------------+--------------+------------+

Then, for the number of cores in the image, is a section containing a 32-bit value describing how many words are in
the image, followed by the image data.

+---------------+---------------+
|Length (32-bit)|Image (L-words)|
+---------------+---------------+
|       L       |   Code        |
+---------------+---------------+

Support
=======

Fork, fix and pull-request! Feel free to contact maintainer with any questions.
