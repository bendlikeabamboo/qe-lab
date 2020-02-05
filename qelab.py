import qelabscf as qels
import qelabbands as qelb
import os
import time
t0=time.perf_counter()  

myman=qelb.Bands("ZnO","LOG","bands/bands.gnu")
myman.add_to_db()
myman.print_db()
myman.print_info()
dir(myman)
t1=time.perf_counter()
print("\nCalculation Information")
print("\tElapsed Time: %5.3f seconds." % (t1-t0))