for ((i=1;i<=5;i++)) 
do  
    python2.7 generate_source_b.py
    python2.7 train.py
    python2.7 test_net.py a on trained
    python2.7 test_net.py a on random
    python2.7 test_net.py b on trained
    python2.7 test_net.py b on random
    python2.7 test_net.py a off off
    python2.7 test_net.py b off off
    python2.7 stat_patterns.py 
done

