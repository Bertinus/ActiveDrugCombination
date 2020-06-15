#!/bin/bash

echo "Starting to download data for use in running.  This may take a few minutes..."
echo ""

cwd=$(echo $PWD)

mkdir -p Data

cd Data

# Decagon data
wget http://snap.stanford.edu/decagon/bio-decagon-ppi.tar.gz
wget http://snap.stanford.edu/decagon/bio-decagon-targets.tar.gz
wget http://snap.stanford.edu/decagon/bio-decagon-targets-all.tar.gz
wget http://snap.stanford.edu/decagon/bio-decagon-combo.tar.gz
wget http://snap.stanford.edu/decagon/bio-decagon-mono.tar.gz
wget http://snap.stanford.edu/decagon/bio-decagon-effectcategories.tar.gz

tar -xzf bio-decagon-ppi.tar.gz
tar -xzf bio-decagon-targets.tar.gz
tar -xzf bio-decagon-targets-all.tar.gz
tar -xzf bio-decagon-combo.tar.gz
tar -xzf bio-decagon-mono.tar.gz
tar -xzf bio-decagon-effectcategories.tar.gz

# NCI data
wget https://wiki.nci.nih.gov/download/attachments/338237347/ComboCompoundSet.sdf?version=1&modificationDate=1493822360000&api=v2
wget https://wiki.nci.nih.gov/download/attachments/338237347/ComboCompoundNames_small.txt?version=1&modificationDate=1493822467000&api=v2
wget https://wiki.nci.nih.gov/download/attachments/338237347/ComboCompoundNames_all.txt?version=1&modificationDate=1493822512000&api=v2

cd ${cwd}

echo ""
echo "Finished downloading data"