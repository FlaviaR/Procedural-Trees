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

Note: The GUI has to be run with python3:<br>
 - <A HREF="https://www.python.org/downloads/">Download Python</A><br>

<hr>

 To run the example models found in the turtle class:<br>
 - python turtle.py \<example_number\><br>
 - \<example_number\> can be any number from 0 to 11
 - openscad turtle.scad 5 & <br><br>

 To use the pregenerated rules in the GUI, simply run: <br>
 - python3 interface.py <br>
 -> python3 should be able to open the generated scad file automatically, <br>
    however if there are problems when opening the subprocess, the generated file can be manually opened by typing: <br>
 - openscad lSystemModel[n].scad, where [n] is the number of the file you want to open. <br>
   E.g. openscad lSystemModel5.scad<br>

<hr>
Information regarding the GUI: <br>
 - Pre-made Rules - a number of pre-written rules that can be selected to generate models <br><br>

 - Options - <br>
 - Stochastic L-Systems - select this option to generate non-deterministic trees <br>
 - Display multiple - display three models side by side <br>
 - Orientation - select which axis the model should be drawn along <br>
 - Add spheres - select this to add spheres in between the cylinder connections. (Use this if generating a model to be printed) <br>
 - Add base to model - select this to add a base to the tree model <br>
 - Base Diameter - select a diameter for the base <br>
 - No L-System - Recursive Tree - select this to generate a recursive tree that does not use L-Systems <br><br>

 * Make your own rules:
 - Ang - rotation angle in degrees <br>
 - Depth - recursion depth to generate the L-System rules <br>
 - Base Phrase - base sentence to initialize the L-System rules <br>
 - Prod. Rules - Production rules separated by a comma- Ex: A, FF^A, B, F&&FB <br>
Which will generate the following rules: <A:FF^A, B:F&&B> <br><br>
One possible entry would be: <br>
35<br>
5<br>
FFFA<br>
A, >”[&FFFA]////[&FFFA]////[&FFFA]<br>


<hr>

OpenSCAD is a computationally heavy software used to extract models for 3D printing. <br>
As such, even though the preview of the models are quick to open, actually rendering them to extract their STL file is time consuming.<br>
For example, when using the "skeletal tree" rule in the interface, the following times are generated:<br>
 - Open preview: <br>
 - ~20s on a linux machine with intel CORE i7 <br>
 - ~5s on a mac book air with intel CORE i7 <br>
 - Rendering the file: <br>
 - 9 hours and 27 minutes on the mac <br>
 - 5 hours and 9 minutes on a windows machine with NVIDIA GEFORCE 1080 and 16GB of RAM <br><br>

 @see http://www.openscad.org/<br>
 @see https://github.com/SolidCode/SolidPython

<hr>

This project uses L-Systems to generate Trees and other models procedurally. 
