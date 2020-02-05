import os

"""
CONSTANTS DECLARATION
"""

RYDERBG_CONSTANT=13.6056980659
class Scf:
	scf_db=[]
	"""
	SCF class represents an instance of SCF calculation.
	"""

	def __init__(self,name,log):
		"""
		Attributes
		----------------
		name:   string
		    name of the SCF calculation
		scflog:    string
			log file containing the scf calculation
		fermi_level: float
			value of the fermi energy level in electron-volts
		total_energy_ev: float
			value of the total energy level in electron-volts
        total_energy_Ry: float  
    		value of the total energy level in Ry
		"""
		self.name = str(name)
		self.scflog = str(log)
		self.fermi_level_ev = 0.0
		self.fermi_level_ry = 0.0
		self.total_energy_ev = 0.0
		self.total_energy_ry = 0.0
		self.determine_total_energy()
		self.determine_fermi()

	def determine_fermi(self):
		"""
		Function for determining the Fermi level
		"""

		file = open(self.scflog,"r")
		log = file.read()
		for item in log.split("\n"):
			if "Fermi" in item:
				self.fermi_level_ev = float(item.strip()[22:30])
				self.fermi_level_ry = self.fermi_level_ev/RYDERBG_CONSTANT
		file.close()

	def determine_total_energy(self):
		"""
		Function for determining the total energy in Ry and eV
		"""

		file = open(self.scflog,"r")
		log = file.read()
		for item in log.split("\n"):
			if "!" in item:
				self.total_energy_ry = float(item.strip()[33:49])
				self.total_energy_ev = self.total_energy_ry*RYDERBG_CONSTANT
		file.close()

	def print_info(self):
		print("\n\nSCF INFORMATION")
		print("SCF Name: "+self.name)
		print("Fermi level:")
		print("\t%.4f eV  (%.4f Ry)") % (self.fermi_level_ev, self.fermi_level_ry)
		print("Total Energy:")
		print("\t%.4f eV  (%.4f Ry)") % (self.total_energy_ev, self.total_energy_ry)
		print("\n\n")

    
	def add_to_db(self):
		"""
		Method for adding the scf calculation to the database
		"""
		Scf.scf_db.append(self)
    
	@staticmethod
	def print_db():
		print("Name            Fermi Level (eV)  Total Energy (eV) | Fermi Level (Ry)  Total Energy (Ry)")
		for item in Scf.scf_db:
			print("%-15s %16.4f  %17.4f | %16.4f %18.4f" % (item.name, item.fermi_level_ev, \
			item.total_energy_ev, item.fermi_level_ry, item.total_energy_ry))