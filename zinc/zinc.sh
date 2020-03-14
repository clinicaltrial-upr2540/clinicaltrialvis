#!/bin/bash 

for i in {1..100} 
do 
	echo "curl http://zinc15.docking.org/substances/subsets/in-man-only.json?page=$i"
	curl http://zinc15.docking.org/substances/subsets/in-man-only.json?page=$i >> raw_json_out.txt
done 
