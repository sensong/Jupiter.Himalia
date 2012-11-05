from __future__ import division
import math
import SimPy.Simulation as simpy

from Jupiter.Ecliptic.Neuron import Neuron

class LIF_STDP_Neuron(Neuron):
    def __init__(self, domain, index, settings, STDP='on', initial_membrane_potential=0.0):
        #settings['reset_potential'] = -70
        #settings['spike_potential'] = 0
        #settings['threshold'] = -54
        #settings['refactory_period'] = 5.0 ms
        #settings['left_window_constant'] = (t+)
        #settings['right_window_constant'] = (t-)
        #settings['learning_rate'] = learning_rate (A+)
        #settings['stability'] = stability (B)
        #settings['weight_ceiling'] = weight_ceiling
        #settings['type'] = 'current' or 'voltage'
        #settings['output_current_decay'] = 3.0 (only need if type is current)
        #settings['output_current_peak'] = 2.2 (only need if type is current)

        Neuron.__init__(self, domain, index)
        self.STDP = STDP
        self.reset_potential = settings['reset_potential'] 
        self.spike_potential = settings['spike_potential']
        self.threshold = settings['threshold']
        self.weight_ceiling = settings['weight_ceiling']

        self.type = settings['type']
        if self.type == 'current':
            self.output_current_peak = settings['output_current_peak']
            self.output_current_decay = 1.0-1.0/settings['output_current_decay']
            self.value = 0.0

        self.stability = settings["stability"]
        self.left_window_constant = settings["left_window_constant"]
        self.left_learning_rate = settings['learning_rate']
        self.left_window_width = abs(math.log(0.01) * self.left_window_constant)
        self.right_window_constant = settings["right_window_constant"]
        #self.right_window_width = abs(math.log(0.01) * self.right_window_constant)
        self.right_window_width = self.right_window_constant
        #self.right_learning_rate = self.left_learning_rate * self.left_window_width * self.stability / self.right_window_width
        self.right_learning_rate = self.left_learning_rate
        if initial_membrane_potential == 0.0:
            self.membrane_potential = self.reset_potential
        else:
            self.membrane_potential = initial_membrane_potential
        self.left_window = []
        self.right_window = []
        self.refactory_period = settings['refactory_period']
        self.refact = 'no'


        self.last_firing_time = -1
        self.spikes_number = 0
        self.spikes_record = []
        self.value_record = []
        self.weights_record = []

    def fire(self):
        #reset membrane potential
        self.membrane_potential = self.reset_potential 
        if self.type == 'current':
            self.value = self.output_current_peak
        self.refact = 'yes'
        event = Event(name = 'reactivate')
        simpy.activate(event, event.reactivate(self), delay = self.refactory_period, prior=True)
        
        #print(simpy.now(), ":", str(self), "fire")
        self.spikes_number += 1
        #self.spikes_record.append(simpy.now())
        current_time = simpy.now() 
        
        #strengthen each source in current left window
        for source in self.left_window: 
            self.adjust_weight(source[0], source[1] - current_time)
        
        #open a new right window
        #self.right_window.append(current_time) 

        #send action potential to each axon
        for target in self.axons.keys():
            event = Event(name = str(target)+" receive from "+str(self))
            simpy.activate(event, event.receive(target, self, current_time), delay = self.axons[target], prior = True)

        #close the right window when it's over
        #event = Event(name = str(self) + " close right window")
        #simpy.activate(event, event.close_a_right_window(self, current_time), delay = self.right_window_width)


    def receive(self, source, pre_spike_time):
        #print(simpy.now(), ":", str(self), "at", self.membrane_potential, "receive", self.dendrites[source])

        #increse membrane potential
        #membrane_potential_increment = self.dendrites[source]
        #self.membrane_potential += membrane_potential_increment
        
        #insert the source into the left window
        #left_window_item = [source, pre_spike_time, simpy.now()]
        #self.left_window.append(left_window_item)

        #check to weaken the dendrite by each action in the right window
        current_time = simpy.now()
        if source.domain == 'source':
            self.right_window.append(current_time) 
            event = Event(name = str(self) + " close right window")
            simpy.activate(event, event.close_a_right_window(self, current_time), delay = self.right_window_width)
        elif source.domain == 'gc':
            if len(self.right_window)>0:
                self.adjust_weight(source, pre_spike_time - self.right_window[-1])

        #for post_spike_time in self.right_window:
            #self.adjust_weight(source, pre_spike_time - post_spike_time)

        #check if it can fire
        #if self.membrane_potential >= self.threshold:
            #if simpy.now() > self.last_firing_time:
                #self.last_firing_time = simpy.now()
                #event = Event(name = str(self) + " fire")
                #simpy.activate(event, event.fire(self), delay = 0.0)

        #remove the source from the left window when it's over, and decrease the membrane potential
        #event = Event(name = str(self) + "remove an item from left window")
        #simpy.activate(event, event.remove_from_left_window(self, left_window_item, membrane_potential_increment), 
                #delay = self.left_window_width)


    def adjust_weight(self, source, time_difference): #time_difference = t_pre - t_post
        if time_difference < 0 and self.dendrites[source] < self.weight_ceiling and (self.STDP == "on" or self.STDP == "left_only"):
            delta = self.dendrites[source]
            self.dendrites[source] += self.weight_ceiling * self.left_learning_rate * math.exp( time_difference / self.left_window_constant)
            if self.dendrites[source] > self.weight_ceiling:
                self.dendrites[source] = self.weight_ceiling
            delta = self.dendrites[source] - delta
            self.weights_record.append([simpy.now(), source, delta])
            #print(simpy.now(), ":", "increse", str(source), "->", str(self), "to", self.dendrites[source])
        elif time_difference >= 0 and self.dendrites[source] > 0 and (self.STDP == "on" or self.STDP == "right_only") and self.dendrites[source] < 256:
            delta = self.dendrites[source]
            self.dendrites[source] += self.right_learning_rate
            if self.dendrites[source] > 1.0:
                self.dendrites[source] = 1.0

            #self.dendrites[source] -= self.weight_ceiling * self.right_learning_rate * math.exp( -time_difference / self.right_window_constant)
            #if self.dendrites[source] < 0:
                #self.dendrites[source] = 0
            #delta = self.dendrites[source] - delta
            #self.weights_record.append([simpy.now(), source, delta])
            #print(simpy.now(), ":", "increse", str(source), "->", str(self), "to", self.dendrites[source])

    def update(self, now):
        #print(self.membrane_potential)
        if self.type == 'current':
            self.value_record.append(self.value)
            self.value *= self.output_current_decay
        if self.refact == 'yes':
            self.spikes_record.append(self.membrane_potential)
            return
        self.membrane_potential -= (self.membrane_potential - self.reset_potential)*0.1  #leak
        input = 0.0
        for source in self.dendrites.keys():
            if source.type == 'current':
                input += source.value
            elif source.type == 'voltage':
                pass # Voltage type input, add code here
        self.membrane_potential += input * 0.1
        if self.membrane_potential < self.reset_potential:
            self.membrane_potential = self.reset_potential
        record = self.membrane_potential
        if self.membrane_potential >= self.threshold:
            if simpy.now() > self.last_firing_time:
                self.last_firing_time = simpy.now()
                event = Event(name = str(self) + " fire")
                simpy.activate(event, event.fire(self), delay = 0.0)
                record = self.spike_potential
        self.spikes_record.append(record)

        

    def weights_trend(self, dendrites_set, initial_sum_weight):
        accumulator = initial_sum_weight
        dendrites_number = len(dendrites_set)
        weights_trend = [[0, accumulator/dendrites_number]]
        for adjust in self.weights_record:
            if adjust[1] in dendrites_set:
                accumulator += adjust[2]
                weights_trend.append([adjust[0], accumulator/dendrites_number])
        return weights_trend


class Event(simpy.Process):
    def update(self, subject):
        subject.update(simpy.now())
        yield simpy.passivate, self

    def fire(self, subject):
        subject.fire()
        yield simpy.passivate, self

    def receive(self, target, source, time):
        target.receive(source, time)
        yield simpy.passivate, self
        
    def reactivate(self, target):
        target.refact = 'no'
        yield simpy.passivate, self

    def close_a_right_window(self, subject, window) :
        subject.right_window.remove(window)
        yield simpy.passivate, self

    def remove_from_left_window(self, subject, window_item, membrane_potential_increment):
        subject.left_window.remove(window_item)

        # if the subject have not fired at or after the spike arrived, then subtract it from the subject's membrane potential
        if subject.last_firing_time < window_item[2]:
            subject.membrane_potential -= membrane_potential_increment
        yield simpy.passivate, self


            



