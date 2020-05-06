#!/bin/bash 

for i in {456..1000} 
do 
	echo "curl http://zinc15.docking.org/substances/subsets/in-man-only.json?page=$i"
	curl http://zinc15.docking.org/substances/subsets/in-man-only.json?page=$i >> ./raw_downloads/page_$i.txt
done 
