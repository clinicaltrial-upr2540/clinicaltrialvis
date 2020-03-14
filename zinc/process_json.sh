PROCESSED_FILE=zinc_smiles.csv 

cat ./raw_downloads/page_2*.txt > $PROCESSED_FILE 
sed -i 's/},{/\n/g' $PROCESSED_FILE
sed -i 's/\[{/\n/g' $PROCESSED_FILE
sed -i 's/}\]/\n/g' $PROCESSED_FILE
sed -i 's/"zinc_id": //g' $PROCESSED_FILE
sed -i 's/ "smiles": //g' $PROCESSED_FILE
sed -i '/^$/d' $PROCESSED_FILE
