import pickle

wfile = open('trained_weights.txt','r')
raw = pickle.load(wfile)
print(len(raw))
