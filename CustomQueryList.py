import sys, getopt

usage_prompt = """
python customQueryList.py [-h] -i <input> -o <output> -c <config>

	<input>
                input file in FASTA format (with sequence naming format of "contig_<sequence name>")
                containing sequences that will be processed
        <output>
                output file in FASTA format containing processed sequences,
                excluding sequences that were specified to be filtered out
        <config>
                input file in .config configuration file format (specified at the Github page)

options:
	-h, --help
         	prints out the above usage statement
"""

def process_assembly(infilepath, outfilepath, configfilepath):

        configfile = open(configfilepath, 'r')
        move_contig_directory = {}
        delete_list = []
        for line in configfile:
                inputs = line.split(':', 1)
                operation = inputs[0]
                if operation == 'd': #delete
                        for contig in inputs[1].rstrip().split(','):
                                delete_list.append(contig)
                elif operation == 'm': #move to below the given contig
                        contigs_list = inputs[1].rstrip().split('->')
			if len(contigs_list) > 1:
                                move_contig_directory[contigs_list[-1]] = []
                                for contig in contigs_list:
                                        move_contig_directory[contigs_list[-1]].append(contig)
                
        configfile.close()
        infile = open(infilepath, 'r')
        outfile = open(outfilepath, 'w')
        for line in infile:
                if len([contig for contig in delete_list if 'contig_' + contig + '\t' in line or 'scaffold_' + contig + '\t' in line]) > 0:
                       continue
                elif len([contig for contig in move_contig_directory.keys() if 'contig_' + contig + '\t' in line or 'scaffold_' + contig + '\t' in line]) > 0:
                        contig_name = [contig for contig in move_contig_directory.keys() if 'contig_' + contig + '\t' in line or 'scaffold_' + contig + '\t' in line]
			for contig in move_contig_directory[contig_name[0]]:
                               outfile.write('contig_' + contig + '\n')
                else:
                        is_accounted_for = False
                        for contig_list in move_contig_directory.values():
				if len([contig for contig in contig_list if 'contig_' + contig + '\t'in line or 'scaffold_' + contig + '\t' in line]) > 0:
                                        is_accounted_for = True
                                        break
                        if not is_accounted_for:
                                outfile.write(line)
                
                
def main():
        infile = ''
        outfile = ''
        configfile = ''
        try:
                opts, args = getopt.getopt(sys.argv[1:], "hi:o:c:", ["help"])
        except getopt.GetoptError as err:
                print(usage_prompt)
                print(str(err))
        for opt, arg in opts:
                if opt in ('-h', '--help'):
                        print(usage_prompt)
                	return
		elif opt == '-i':
                        infile = arg
                elif opt == '-o':
                        outfile = arg
                elif opt == '-c':
                        configfile = arg
                else:
                        print(usage_prompt)
                        return
        process_assembly(infile,outfile,configfile)


if __name__ == "__main__":
        main()

