#!/usr/bin/env python

########################################################################
#
#	Author: Michele Berselli
#		University of Padova
#		berselli.michele@gmail.com
#
########################################################################


## Import libraries
import sys, requests, argparse
import json, time


## Functions definition
def request_stable_ID_gene(list_gene_name):
	dict_names = { 'symbols' : list_gene_name }

	server = 'http://rest.ensembl.org'
	ext = '/lookup/symbol/homo_sapiens'
	headers={ 'Content-Type' : 'application/json', 'Accept' : 'application/json'}

	r = requests.post(server+ext, headers=headers, data=json.dumps(dict_names))

	error_code = 0
	if not r.ok:
		error_code = 1
	#end if

	return r.json(), error_code
#end def request_stable_ID_gene

def request_genomic_5prime_3prime(id_gene, prime_5, prime_3):
	server = 'https://rest.ensembl.org'
	ext = '/sequence/id/' + id_gene + '?type=genomic;expand_5prime=' + str(prime_5) + ';expand_3prime=' + str(prime_3)

	r = requests.get(server+ext, headers={ 'Content-Type' : 'application/json'}, timeout=10)

	error_code, json, status_code = 0, r.json(), r.status_code
	if not r.ok:
		error_code = 1
	#end if

	return json, error_code, status_code
#end def request_genomic_5prime_3prime

def request_annotazione_json(name_gene):
	''' request annotation, json '''
	server = 'http://rest.ensembl.org'
	ext = '/lookup/symbol/homo_sapiens/' + name_gene + '?'

	r = requests.get(server+ext, headers={ 'Content-Type' : 'application/json'}, timeout=10)

	error_code, json, status_code = 0, r.json(), r.status_code
	if not r.ok:
		error_code = 1
	#end if

	return json, error_code, status_code
#end def request_annotazione_json

def request_region(chromosome, start_region, end_region, strand, assembly_name):
	''' request exon '''
	server = 'http://rest.ensembl.org'
	ext = '/sequence/region/human/' + str(chromosome) + ':' + str(start_region) + ".." + str(end_region) + ':' + str(strand) + '?coord_system_version=' + assembly_name

	r = requests.get(server+ext, headers={ 'Content-Type' : 'application/json'})

	error_code = 0
	if not r.ok:
		error_code = 1
	#end if

	return r.json(), error_code
#end def request_region

def main(args):

	# Variables
	INTERVAL = 0.2
	donwstreamlength = int(args['downstreamlength']) if args['downstreamlength'] else 0
	promoterlength = int(args['promoterlength'])

	fo = open(args['outputfile'], 'w')

	# Reading name_genes to search
	with open(args['inputfile'], 'r') as fi:
		for line in fi:
			time.sleep(INTERVAL)
			name_gene, status_code, counter = line.rstrip(), 0, 0
			sys.stderr.write('Processing {0}\n'.format(name_gene))
			sys.stderr.flush()

			# Retrieve ensemble ID
			while status_code != 200 and counter < 10:
				counter += 1
				try:
					name_ID_json, error_code, status_code = request_annotazione_json(name_gene)
				except:
					sys.stderr.write('\r error: trial {0}\n'.format(counter))
					sys.stderr.flush()
					continue
				#end try
			#end while

			if not error_code:
				status_code, counter = 0, 0

				# Retrieve sequence
				try:
					sys.stderr.write('-> {0} {1}\n'.format(name_gene, name_ID_json['id']))
					sys.stderr.flush()

					while status_code != 200 and counter < 10:
						counter += 1
						try:
							promoter_seq, error_code, status_code = request_genomic_5prime_3prime(name_ID_json['id'], promoterlength, donwstreamlength)
						except:
							sys.stderr.write('\r error: trial {0}\n'.format(counter))
							sys.stderr.flush()
							continue
						#end try
					#end while

					sys.stderr.write('-> retrieved promoter\n')
					sys.stderr.flush()

					if not error_code:
						try:
							seq = promoter_seq['seq'][:promoterlength + donwstreamlength]
						except:
							seq = promoter_seq['seq']
						#end try
						fo.write('>{0}|{1}|{2}\n'.format(name_gene, name_ID_json['id'], promoter_seq['desc']))
						fo.write('{0}\n'.format(seq))
					else:
						with open('log_errors.txt', 'a+') as fw:
							fw.write('{0}_error_downloading_promoter\n'.format(name_gene))
						#end with
					#end if
				except:
					with open('log_errors.txt', 'a+') as fw:
						fw.write('{0}_promoter_not_found\n'.format(name_gene))
					#end with
				#end try
			else:
				with open('log_errors.txt', 'a+') as fw:
					fw.write('{0}_Error_retrieving_IDs\n'.format(name_gene))
				#end with
			#end if
		#end for
	#end with

	fo.close()

#end def main

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='It is a script that allows to retrieve the promoter regions for a desired list of genes from ENSEMBL')

    parser.add_argument('-i','--inputfile', help='input file with gene names', required=True)
    parser.add_argument('-p','--promoterlength', help='length of the promoter region, region upstream TSS', required=True)
    parser.add_argument('-d','--downstreamlength', help='length of the region retrieved downstream TSS', required=False)
    parser.add_argument('-o','--outputfile', help='output file with promoters sequences', required=True)

    args = vars(parser.parse_args())

    main(args)

# end if
