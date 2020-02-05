import os
import qelabscf as qels
import matplotlib as mpl
import numpy as np
import time
class Bands(qels.Scf):
	def __init__(self,name,scflog,bandsdata,etolmin=None,etolmax=None):
		"""
		bandsdata: string
			path to gnu-compatible format of the bands
		cbm:	int
			band number of Conduction Band Minimum (CBM)
		vbm:	int
			band number of Valence Band Maximum (VBM)
		NOTE: vbm < cbm
		"""
		super().__init__(name,scflog)
		self.etolmin=self.fermi_level_ev-5
		self.etolmax=self.fermi_level_ev+5
		#t0=time.perf_counter()
		self.data=bandsdata
		self.bandgap=0.0
		self.determine_band_gap()
		#t1=time.perf_counter()
		#print("Elapsed Time: %5.3f seconds." % (t1-t0))

	def determine_band_gap(self):
		"""
		f:	file
			file instance
		data:	string
			string representation of the file
		kpoints: list
			list of kpoints used in the calculation
		kpoint_pairs: list inside list
			set of adjacent kpoints for the determination
			of interval
		number_of_kpoints: int
			determines the number of sampled kpoints
		number_of_bands: int
			determines the number of bands per kpoint

		Algorithm
		1. Open and read GNU-compatible bands structure data file
		2. Declare variables above
		3. List the value of the sampled kpoints
		
			Note: The GNU-compatible band structure data file is
			
			kpoint_1 energy_1_1
			kpoint_2 energy_1_2
			...
			kpoint_n energy_1_n
		{empty line}
			kpoint_1 energy_2_1
			kpoint_2 energy_2_2
			...
			kpoint_n energy_2_n
		{empty line}
			...
		{empty line}
			kpoint_1 energy_m_1
			kpoint_2 energy_m_2
			...
			kpoint_n energy_m_n

			Thus, we can obtain the list of sampled kpoints (i.e., the set
			kpoint_1, kpoint_2,..., kpoint_n) by iterating through the first
			set of values before an {empty line} is encountered (var number_of_kpoints)

		4. Determine number of bands for each kpoint by counting
		the number of {empty line} + 1 (var number_of_bands)
		5. Create a 2D-array that is (number_of_kpoints) x (number_of_bands)
		6. Create another 2D-array that will compute the vertical difference between two adjacent bands
		across each sampled k-point (i.e. computes the band gap for each band pairs for each kpoint)
		(array band_gap_array)
		7. Obtain the horizontal sum for each band gap (i.e., sum of the difference between the same band interval
		across all sampled kpoints) (array_band_gap_sum_array)
		8. The highest horizontal band gap sum will distinguish the conduction band from the valence band
		(assuming that there is coupling). Here we can then define the top_valence_band and bottom_conduction_band
		since they will comprise the bands that will yield the highest horizontal band gap sum. 
			NOTE: EXCEPTION
				This will usually yield intervals found deep in the valence band or conduction band. This is
				wrong since we need the one near the Fermi level. The workaround is to limit the considered
				intervals within a specified energy levels near the Fermi level. Default value: +/- 5eV w.r.t Fermi level.
		9. Obtain the highest point of the top_valence_band from the array in 5 (returns var valence_band_maximum)
		10. Obtain the lowest point of the bottom_conduction_band from the array in 5 (returns var conduction_band_minimum)
		11. The band gap is determined by conduction_band_minimum - valence_band_maximum
		12. Additional: if the value obtained in 9 and the value obtained in 10 has different indices (i.e., the
		conduction_band_minimum and the valence_band_maximum belongs to different kpoints), then the band gap is indirect,
		otherwise, direct.
		13. Additional: The number of bands is easily obtained once the interval in 8 is determined (i.e., the valence
		band and conduction band is determined) by comparing with the total number of bands.
		"""

		f=open(self.data,"r")
		data=f.read()
		kpoints=[]
		bands=[]
		for line in data.split("\n"):
			if len(line.strip())==0:
				break
			#print(line[4:11].strip())
			kpoints.append(float(line[4:11].strip()))
		self.number_of_kpoints=len(kpoints)
		self.number_of_bands=sum(1 for line in data.split("\n") if len(line.strip()) == 0)-1

		band_structure_array=np.zeros((self.number_of_kpoints,self.number_of_bands))
		band_gap_array=np.zeros((self.number_of_kpoints,self.number_of_bands-1))

		#FILL ARRAY WITH VALUES
		j=0
		k=0
		for line in data.split("\n"):
			if len(line.split())==0:
				k=0
				j+=1
				continue
			band_structure_array[k,j]=float(line[12:20].strip())
			k+=1
		
		for k in range(self.number_of_kpoints):
			for j in range(self.number_of_bands-1):
					if band_structure_array[k,j]>self.etolmax:
						continue
					if band_structure_array[k,j]<self.etolmin:
						continue
					band_gap_array[k,j]=band_structure_array[k,j+1]-band_structure_array[k,j]
		band_gap_sum_array = np.sum(band_gap_array,0)

		for i,band_gap_sum in enumerate(band_gap_sum_array):
			if i==0:
				largest_value_index=0
				largest_value=band_gap_sum
				continue
			if band_gap_sum>largest_value:
				largest_value_index=i
				largest_value=band_gap_sum
		self.largest_sum_of_intervals=largest_value
		self.top_valence_band=largest_value_index
		self.bottom_conduction_band=largest_value_index+1
		self.number_of_valence_bands=largest_value_index
		self.number_of_conduction_bands=self.number_of_bands-self.number_of_valence_bands
		


		for i in range(self.number_of_kpoints):
			if i==0:
				largest_value=band_structure_array[i,self.top_valence_band]
				largest_value_index=i
				continue
			if band_structure_array[i,self.top_valence_band]>largest_value:
				largest_value=band_structure_array[i,self.top_valence_band]
				largest_value_index=i
		self.valence_band_maximum=largest_value-self.fermi_level_ev


		for i in range(self.number_of_kpoints):
			if i==0:
				least_value=band_structure_array[i,self.bottom_conduction_band]
				least_value_index=i
				continue
			if band_structure_array[i,self.bottom_conduction_band]<least_value:
				least_value=band_structure_array[i,self.bottom_conduction_band]
				least_value_index=i
			#print(band_structure_array[i,top_valence_band])
		self.conduction_band_minimum=least_value-self.fermi_level_ev
		self.band_gap=self.conduction_band_minimum-self.valence_band_maximum
		self.nature=(True if (least_value_index==largest_value_index) else False)
		

	def print_info(self):
		print("\nSCF INFORMATION")
		print("\tSCF Name: "+self.name)
		print("\tFermi level:  %.4f eV  (%.4f Ry)" % (self.fermi_level_ev, self.fermi_level_ry))
		print("\tTotal Energy:  \t%.4f eV  (%.4f Ry)" % (self.total_energy_ev, self.total_energy_ry))
		print("\n")
		print("BAND STRUCTURE INFORMATION")
		print("\tNumber of Bands: "+str(self.number_of_bands))
		print("\tNumber of K-Points: "+ str(self.number_of_kpoints))
		print("\tBand Pair w/ largest sum: %4i to %4i (%8.4f eV)" \
		% (self.top_valence_band, self.top_valence_band+1, self.largest_sum_of_intervals))
		print("\tTop valence band number: %4i." % (self.top_valence_band))
		print("\tBottom conduction band number: %4i." % (self.bottom_conduction_band))
		print("\tNumber of valence bands: %4i" %(self.number_of_valence_bands))
		print("\tNumber of conduction bands: %4i" %(self.number_of_conduction_bands))
		print("\tValence Band Maximum (w.r.t. Fermi level): %8.4f eV" %(self.valence_band_maximum))
		print("\tConduction Band Minimum (w.r.t. Fermi level): %8.4f eV" % (self.conduction_band_minimum))
		print ("\tNature: direct" if self.nature else "Nature: indirect")
		print("\tBand Gap Value: %5.2f eV" % (self.band_gap))