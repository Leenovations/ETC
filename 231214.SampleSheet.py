#!/usr/bin/python3
import sys
import os

LIST = sys.argv[1:]

with open('Datalist.txt', 'w') as note2:
	for data in LIST:
		note2.write(data + '\n')

if len(LIST) % 2 == 0:
	pass
else:
	raise ValueError("\033[91mThe number of raw data files is odd\033[0m")

with open('SampleSheet.txt', 'w') as note1:
	for data in LIST:
		if data.split('.')[-1] == 'fastq' or data.split('.')[-1] == 'gz':
			if '_R1' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_R1')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_R1')[0]
				First = data
				Second = data.replace('_R1', '_R2')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')

				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					name = data.split('_R1')[0]
					First = data
					Second = data.replace('_R1', '_R2')
					note2.write(Name + '\t' + First+ '\t' + Second + '\n')

			elif '_1.fastq.gz' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq.gz')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_1.fastq.gz')[0]
				First = data
				Second = data.replace('_1.fastq.gz', '_2.fastq.gz')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')

				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					name = data.split('_1.fastq.gz')[0]
					First = data
					Second = data.replace('_1.fastq.gz', '_2.fastq.gz')
					note2.write(Name + '\t' + First+ '\t' + Second + '\n')

			elif '_1.fastq' in data:
				Name = data.split('/')[-1]
				Name = Name.split('_1.fastq')[0]
				command = f'mkdir {Name}'
				os.system(command)
				Size = os.path.getsize(data)

				name = data.split('_1.fastq')[0]
				First = data
				Second = data.replace('_1.fastq', '_2.fastq')
				note1.write(Name + '\t' + First+ '\t' + Second + '\t' + str(Size) + '\n')

				with open(f'{Name}/SampleSheet.txt', 'w') as note2:
					name = data.split('_1.fastq')[0]
					First = data
					Second = data.replace('_1.fastq', '_2.fastq')
					note2.write(Name + '\t' + First+ '\t' + Second + '\n')

		elif data.split('.')[-1] == 'bam':
			Name = data.split('/')[-1]
			Name = Name.split('.bam')[0]
			Bam = data

			command = f'mkdir -p {Name}/03.Align/'
			os.system(command)

			command = f'mv {Bam} {Name}/03.Align/'
			os.system(command)
			command = f'mv {Bam}.bai {Name}/03.Align/'
			os.system(command)

			note1.write(Name + '\t' + Name + '\t' + Name + '\n')

			with open(f'{Name}/SampleSheet.txt', 'w') as note2:
				Name = data.split('/')[-1]
				Name = Name.split('.bam')[0]
				Bam = data

				note2.write(Name + '\t' + Name + '\t' + Name + '\n')