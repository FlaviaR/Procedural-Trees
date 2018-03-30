# Procedural-Trees

 There are a number of packages that have to be installed before using this code: <br>
 - On <A HREF="https://start.fedoraproject.org">Fedora</A>: <br>
 -# sudo dnf install openscad-MCAD <br>
 - On <A HREF="https://www.ubuntu.com/desktop">Ubuntu</A>: <br>
 -# sudo apt-get install openscad-mcad <br>
 - On MacOS (using <A HREF="https://www.macports.org">macports</A>): <br>
 -# sudo port install OpenSCAD <br>
 - sudo pip install solidpython <br>
 or for python3: <br>
 - sudo pip3 install solidpython<br>

 To see the created model example in Turtle:<br>
 - python turtle.py \<example_number\><br>
 - openscad turtle.scad & <br><br>

 Note: The GUI has to be run with python3:<br>
 - <A HREF="https://www.python.org/downloads/">Download Python</A><br>

 To use the pregenerated rules, simply run: <br>
 - python3 interface.py <br>
   -> python3 should be able to open the generated file automatically, but in case the file can not be oppened, type: <br>
 - openscad lSystemModel[n].scad, where [n] is the number of the file you want to open. <br>
   E.g. openscad lSystemModel5.scad<br>

 If you are trying to create your own rules with the interface, read ahead for more information regarding parameters: <br>
 - Ang - rotation angle in degrees <br>
 - Depth - recursion depth to generate the L-System rules <br>
 - Base Phrase - base sentence to initialize the L-System rules <br>
 - Prod. Rules - Production rules separated by a comma- Ex: A, FF^A, B, F&&FB <br>
Which will generate the following rules: <A:FF^A, B:F&&B>

 @see http://www.openscad.org/<br>
 @see https://github.com/SolidCode/SolidPython

<br>

This project uses L-Systems to generate Trees and other models procedurally. 
