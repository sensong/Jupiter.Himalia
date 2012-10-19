for ((i=0;i<5;i++)) 
do 
python2.7 test_net.py
done
rm -f continue.tmp

touch no_inhi.tmp
for ((i=0;i<5;i++)) 
do 
python2.7 test_net.py
done
rm -f continue.tmp
rm -f no_inhi.tmp


python2.7 stat_net.py
