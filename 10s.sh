rm -f continue.tmp
rm -f no_inhi.tmp
python2.7 test_net.py
rm -f continue.tmp

touch no_inhi.tmp
python2.7 test_net.py
rm -f continue.tmp
rm -f no_inhi.tmp

python2.7 stat_net.py
