#!/bin/bash

# For some reason, doesnt work if executed in the same script as get_data.sh so we created a separate script

echo "Unzip the NCI data"
cd Data/NCI

mv ComboCompoundNames_all.txt?version=1 ComboCompoundNames_all.txt
mv ComboCompoundNames_small.txt?version=1 ComboCompoundNames_small.txt
mv ComboCompoundSet.sdf?version=1 ComboCompoundSet.sdf
mv ComboDrugGrowth_Nov2017.zip?version=1 ComboDrugGrowth_Nov2017.zip
mv ALMANAC_DataFields.txt?version=1 ALMANAC_DataFields.txt

unzip ComboDrugGrowth_Nov2017.zip

cd ../..