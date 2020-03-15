PROCESSED_FILE=zinc_smiles.csv 

cat ./raw_downloads/page_*.txt > $PROCESSED_FILE 
sed -i 's/},{/\n/g' $PROCESSED_FILE
sed -i 's/\[{/\n/g' $PROCESSED_FILE
sed -i 's/}\]/\n/g' $PROCESSED_FILE
sed -i 's/"zinc_id": //g' $PROCESSED_FILE
sed -i 's/ "smiles": //g' $PROCESSED_FILE
sed -i '/^$/d' $PROCESSED_FILE


wc -l zinc_smiles.csv 
tail zinc_smiles.csv

# if you are in windows 
cp zinc_smiles.csv /mnt/c/Users/Lu\ Wang/Documents/School/Software\ Capstone/zinc_smiles.csv
