python decryptor.py -vt europarl-v7.es-en.en -n .05 >> europarl.results &
python decryptor.py -vt newstest2012.en -n .05 >> newstest2012.results &
python decryptor.py -vt newstest2013.en -n .05 >> newstest2013.results & 
python decryptor.py -vt original -n .05 >> original.results &
echo 'Running algorithm on testfiles in background. Call tail -f <file>.result to see logs as they come in'
