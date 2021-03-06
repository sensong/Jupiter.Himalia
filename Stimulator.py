from Jupiter.Ecliptic.Neuron import Neuron
import random
import math

class Constant_Stimulator(Neuron):
    def __init__(self, domain, index, type, value, decay_time = 0.0):
        Neuron.__init__(self, domain, index)
        self.type = type
        self.decay_time = decay_time
        if self.type == 'current':
            self.value = value
        elif self.type == 'voltage':
            self.V_membrane = value
    def update(self, now):
        if self.decay_time > 0.0:
            if self.type == 'current':
                self.value *= 1.0-1.0/self.decay_time
            elif self.type == 'voltage':
                self.V_membrane *= 1.0-1.0/self.decay_time

class Current_Poisson_Stimulator(Neuron):
    def __init__(self, domain, index, freq, scale, decay):
        Neuron.__init__(self, domain, index)
        self.type = 'current'
        self.freq = freq/1000.0  #Probability of occring in 1ms
        self.scale = scale
        self.decay = 1.0-1.0/decay
        self.value = 0.0
        self.spikes_record = []

    def update(self, now):
        self.value *= self.decay
        if random.random() < self.freq:  #spike
            self.value+=self.scale
        self.spikes_record.append(self.value)
        

        

class Current_Poisson_Pool(Neuron):
    def __init__(self, domain, index, scale, decay, pool_settings):
        Neuron.__init__(self, domain, index)
        self.type = 'current'
        self.freq = 0.0
        self.scale = scale
        self.decay = 1.0-1.0/decay
        self.alpha = pool_settings['alpha']
        self.k = pool_settings['k']
        self.a = pool_settings['a']
        self.b = pool_settings['b']
        self.c = pool_settings['c']
        self.d = pool_settings['d']
        
        self.pre_spike_time = []
        self.value = 0.0

        self.spikes_record = []
        self.freq_record = []
    
    def receive(self, source, pre_spike_time):
        self.pre_spike_time.append(pre_spike_time)
        #print(pre_spike_time)
    
    def update(self, now):
        P_neg = 0.0
        for spike in self.pre_spike_time:
            if spike <= now:
                temp = (now - spike) / self.alpha
                mi = (spike - now) / self.alpha
                temp = temp * (2.7172**mi)
                P_neg += temp
        P_neg *= self.k
        P_conv = 2.0 * self.b * P_neg + self.d
        P_conv = math.tanh(P_conv) + 1.0
        P_conv *= self.alpha/2.0
        self.freq = P_conv * self.c
        self.freq_record.append(self.freq)
        self.value *= self.decay
        if random.random() < self.freq:   #spike
            self.value = self.scale
        self.spikes_record.append(self.value)




