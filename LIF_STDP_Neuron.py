import math
import SimPy.Simulation as simpy

from Jupiter.Ecliptic.Neuron import Neuron

class STDP_Neuron(Neuron):
    def __init__(self, domain, index, settings_dict, STDP = 'on'):
        #settings_dict['rest_potential'] = 0
        #settings_dict['action_potential'] = 1
        #settings_dict['threshold'] = 0.3
        #settings_dict['left_window_constant'] = (t+)
        #settings_dict['right_window_constant'] = (t-)
        #settings_dict['learning_rate'] = learning_rate(A+)
        #settings_dict['stability'] = stability(B)
        #settings_dict['max_weight'] = max_weight

        Neuron.__init__(self, domain, index)
        #simpy.Process.__init__(self, name = str(self))
        self.STDP = STDP
        self.rest_potential = settings_dict['rest_potential'] 
        self.spike_potential = settings_dict['action_potential']
        self.threshold = settings_dict['threshold']
        self.max_weight = settings_dict['max_weight']

        self.stability = settings_dict["stability"]
        self.left_window_constant = settings_dict["left_window_constant"]
        self.left_learning_rate = settings_dict['learning_rate']
        self.left_window_width = abs(math.log(0.01) * self.left_window_constant)
        self.right_window_constant = settings_dict["right_window_constant"]
        self.right_window_width = abs(math.log(0.01) * self.right_window_constant)
        self.right_learning_rate = self.left_learning_rate * self.left_window_width * self.stability / self.right_window_width

        self.membrane_potential = self.rest_potential
        self.left_window = []
        self.right_window = []
        
        self.last_firing_time = -1
        self.spikes_number = 0
        self.spikes_record = []
        self.weights_record = []

    def fire(self):
        #reset membrane potential
        self.membrane_potential = self.rest_potential 
        
        #print(simpy.now(), ":", str(self), "fire")
        self.spikes_number += 1
        self.spikes_record.append(simpy.now())
        current_time = simpy.now() 
        
        #strengthen each source in current left window
        for source in self.left_window: 
            self.adjust_weight(source[0], source[1] - current_time)
        
        #open a new right window
        self.right_window.append(current_time) 

        #send action potential to each axon
        for target in self.axons.keys():
            event = Event(name = str(target)+" receive from "+str(self))
            simpy.activate(event, event.receive(target, self, current_time), delay = self.axons[target], prior = True)

        #close the right window when it's over
        event = Event(name = str(self) + " close right window")
        simpy.activate(event, event.close_a_right_window(self, current_time), delay = self.right_window_width)


    def receive(self, source, pre_spike_time):
        #print(simpy.now(), ":", str(self), "at", self.membrane_potential, "receive", self.dendrites[source])

        #increse membrane potential
        membrane_potential_increment = self.dendrites[source]
        self.membrane_potential += membrane_potential_increment
        
        #insert the source into the left window
        left_window_item = [source, pre_spike_time, simpy.now()]
        self.left_window.append(left_window_item)

        #check to weaken the dendrite by each action in the right window
        for post_spike_time in self.right_window:
            self.adjust_weight(source, pre_spike_time - post_spike_time)

        #check if it can fire
        if self.membrane_potential >= self.threshold:
            if simpy.now() > self.last_firing_time:
                self.last_firing_time = simpy.now()
                event = Event(name = str(self) + " fire")
                simpy.activate(event, event.fire(self), delay = 0.0)

        #remove the source from the left window when it's over, and decrease the membrane potential
        event = Event(name = str(self) + "remove an item from left window")
        simpy.activate(event, event.remove_from_left_window(self, left_window_item, membrane_potential_increment), 
                delay = self.left_window_width)


    def adjust_weight(self, source, time_difference): #time_difference = t_pre - t_post
        if time_difference < 0 and self.dendrites[source] < self.max_weight and (self.STDP == "on" or self.STDP == "left_only"):
            delta = self.dendrites[source]
            self.dendrites[source] += self.max_weight * self.left_learning_rate * math.exp( time_difference / self.left_window_constant)
            if self.dendrites[source] > self.max_weight:
                self.dendrites[source] = self.max_weight
            delta = self.dendrites[source] - delta
            self.weights_record.append([simpy.now(), source, delta])
            #print(simpy.now(), ":", "increse", str(source), "->", str(self), "to", self.dendrites[source])
        elif time_difference >= 0 and self.dendrites[source] > 0 and (self.STDP == "on" or self.STDP == "right_only") and self.dendrites[source] < 256:
            delta = self.dendrites[source]
            self.dendrites[source] -= self.max_weight * self.right_learning_rate * math.exp( -time_difference / self.right_window_constant)
            if self.dendrites[source] < 0:
                self.dendrites[source] = 0
            delta = self.dendrites[source] - delta
            self.weights_record.append([simpy.now(), source, delta])
            #print(simpy.now(), ":", "increse", str(source), "->", str(self), "to", self.dendrites[source])

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
    def fire(self, subject):
        subject.fire()
        yield simpy.passivate, self

    def receive(self, target, source, time):
        target.receive(source, time)
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


            



