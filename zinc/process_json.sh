PROCESSED_FILE=json_to_csv.csv 

cat raw_json_out.txt > $PROCESSED_FILE 
sed -i 's/},{/\n/g' $PROCESSED_FILE
sed -i 's/\[{/\n/g' $PROCESSED_FILE
sed -i 's/}\]/\n/g' $PROCESSED_FILE
sed -i 's/"zinc_id": //g' $PROCESSED_FILE
sed -i 's/ "smiles": //g' $PROCESSED_FILE
sed -i '/^$/d' $PROCESSED_FILE
