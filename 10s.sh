rm -f continue.tmp
rm -f no_inhi.tmp
rm -f trained
python2.7 test_net.py

touch trained
python2.7 test_net.py
rm -f trained

