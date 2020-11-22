# CustomQueryList

This program is a Python script used to reorganize and filter a query list that would be used in [mScaffolder](https://github.com/mahulchak/mscaffolder) to scaffold a [Flye](https://github.com/fenderglass/Flye) assembly.

# Overview
This tool is designed to take in a query list (format discussed below) of a [Flye](https://github.com/fenderglass/Flye) assembly, and use a configuration file to reorganize the order of contigs in the query list and output it to a new query list, as well as remove specified contigs from the query list. This outputted query list can then be used with [mScaffolder](https://github.com/mahulchak/mscaffolder) to scaffold the original assembly that the query list was generated from. 

# Usage
Since this program assists with modifying query lists for use with [mScaffolder](https://github.com/mahulchak/mscaffolder), be sure to follow the mScaffolder workflow in order to prepare the assembly for scaffolding and generate the query list to be used as input here. 

### Input and ouput query list file formats
For the query list input of CustomQueryList, the contig ids must be in the format of 
"contig_{contig name}" or "scaffold_{sequence name}" in order to properly be processed.
As well, the query list output will write the contig ids as "contig_{sequence name}".

### Running the program
Usage of `CustomQueryList` is as follows:

	python customQueryList.py [-h] -i <input> -o <output> -c <config>
		
		<input>
			input file in mScaffolder query list format (with contig ids of "contig_<contig name>" or "scaffold_<contig name>") 
			containing contig ids that will be processed
		<output>
			output file in mScaffolder query list format containing processed contig ids,
			excluding contigs that were specified to be filtered out.
		<config>
			input file in .config configuration file format (specified below)

	options:
		-h, --help
			prints out the above usage statement

### Configuration file format
The configuration file should be formatted as a .config file that specifies two possible operations 
that can be done on the assembly (each on a new line), and which sequences should be included in the operation.

The operations are as follows:
```
d: delete - all specified contigs name are removed from the main output file.
	format: d:<contig name>,<contig name>,...
m: move - all specified contigs are reorganized into order given, with the first contig remaining in its original position, and all following contigs being placed after the contig that immediately preceded it in the ordering.
        format: m:<contig name>-><contig name>-><contig name>...
```
Given the following example query list,  
```
y tics
contig_1
contig_2
contig_3
contig_4
contig_5
contig_6
contig_7
contig_8
contig_9
contig_10
```
an example configuration file would be:
```
d:4,5
m:3->9->2
m:7->6
```
After running CustomQueryList with the example query list and configuration files as inputs, the outputted query list would be:
```
y tics
contig_1
contig_3
contig_9
contig_2
contig_7
contig_6
contig_8
contig_10
```
The configuration file does not need to include specifications for all operations, and you can have multiple lines
for the same operations (for example, you can have multiple sets of reorder contigs, can specify contigs to be deleted over multiple lines).

# Disclaimer
This tool was primarily used as an internal tool to process query lists that were used when scaffolding Flye assemblies with [mScaffolder](https://github.com/mahulchak/mscaffolder). 
Feel free to modify and/or build upon this code to fit your specific usage and needs.

# License
This program is licensed under the Apache License Version 2.0. A copy of the Apache 2.0 license can be found [here](https://github.com/AvivBenchorin/CustomQueryList/blob/main/LICENSE).
