# Elections Scaper
data_volby_20217.py: the third project to the Engeto Online Python Academy

## Project description
The purpose is to obtain data from the results of the parliamentary elections in 2017 for the selected district 
and save them in a csv file.

## Installing libraries
The list of libraries used in the code is stored in the requirements.txt file.

## Starting the project
The data_volby_2017.py file is run from the command line and requires two arguments.
The first argument is a reference to the territorial entity
The second argument is the name of the output file
The output is a csv file with data for the given territorial unit.

## Sample project

### Arguments for the district Uherské Hradiště:
The first argument: 'https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202'
The second argument: Uherské_Hradiště_volby_2017

### Starting the program:
python data_volby_2017.py 'https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202' 'Uherské_Hradiště_volby_2017'

### Program steps:
Argument checking: Argument checking is OK
File creation: CSV file "Uherské_Hradiště_volby_2017.csv" has been created.

## Sample output:
code;location;registered;envelopes;valid;Česká pirátská strana;Referendum o Evropské unii;TOP 09;ANO 2011;...
592013;Babice;1452;873;866;74;0;23;254;1;0;95;5;1;0;133;4
592021;Bánov;1707;1070;1063;71;1;11;293;1;0;148;6;0;0;156;2
592030;Bílovice;1473;1018;1008;90;0;28;264;0;2;147;4;3;1;92;35