import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)
from eppy.modeleditor import IDF

iddfile = "/Applications/OpenStudio-2.9.1/EnergyPlus/Energy+.idd"
IDF.setiddname(iddfile)

idfname = "/Users/abdollahforoutan/ml4iot/in.idf"
epwfile = "/Applications/OpenStudio-2.9.1/EnergyPlus/ITA_Milan.160660_IWEC.epw"

idf = IDF(idfname, epwfile)
idf.run()

