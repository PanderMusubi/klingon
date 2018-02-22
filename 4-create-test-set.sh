if [ ! -e words.txt ]; then
	echo 'ERROR: Missing file words.txt'
	exit 1
fi
sed -e 's/ /\n/g' words.txt | sed -e 's/[!,.]//g' | sort | uniq > tmp.txt
grep \' tests.txt | sed -e "s/'/’/g" >> tmp.txt
sort tmp.txt | uniq > tests.txt
rm -f tmp.txt
