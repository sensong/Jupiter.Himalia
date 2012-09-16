import math
import random
#import SimPy.SimulationTrace as Simpy
import SimPy.Simulation as Simpy

from Motif import Motif
from STDP_Neuron import STDP_Neuron as Neuron
from STDP_Neuron import Event

class Single_Perceptron(Motif):
    def __init__(self, domain, index, dendrites_number, neuron_settings, initial_weights, STDP = 'on'):
        Motif.__init__(self, domain, index)
        
        self.target = Neuron(domain+".target", 0, neuron_settings, STDP)
        self.inputs = []
        self.initial_weights = initial_weights
        max_weight = neuron_settings["max_weight"]
        for i in range(0, dendrites_number):
            self.inputs.append(Neuron("input", i, neuron_settings, STDP))
            self.inputs[i].connect(self.target, weight = initial_weights[i], distance = 1.0)


    def stimulate(self, stimu_range, start_time, duration, mean_rate, stddev = 0, init_phase = 0):
        deviation_gain = mean_rate / 10 * 3 * math.sqrt(2)
        stimu_rate = mean_rate + deviation_gain * random.gauss(0, stddev)
        if stimu_rate < 1:
            stimu_rate = 1
        elif stimu_rate > mean_rate * 2 - 1:
            stimu_rate = mean_rate * 2 - 1
        for input in [self.inputs[i] for i in stimu_range]:
            stimu_period = 1000 / stimu_rate
            if init_phase == "random":
                current_time = start_time + random.random() * stimu_period + random.random()
            else:
                current_time = start_time + init_phase + random.random()
            while current_time < start_time+duration:
                event = Event(name = "simulate " + str(input))
                Simpy.activate(event, event.fire(input), at = current_time)
                current_time += stimu_period


    def report_weights_trend(self, from_dendrite, to_dendrite):
        #output_rate = self.target.spikes_number
        #weights_list = [self.target.dendrites[input] for input in self.inputs]
        initial_sum_weights = math.fsum(self.initial_weights[from_dendrite:to_dendrite])
        dendrites_set = self.inputs[from_dendrite:to_dendrite]
        return self.target.weights_trend(dendrites_set, initial_sum_weights)

    def report_spikes_timeline(self, from_time, to_time):
        result = []
        offset = 1
        for neuron in self.inputs:
            result_piece = [[from_time, offset]]
            for record in neuron.spikes_record:
                if from_time <= record < to_time:
                    #print(record)
                    result_piece.append([record - 0.0001, offset])
                    result_piece.append([record, offset + 0.9])
                    result_piece.append([record + 0.0001, offset])
                elif record >= to_time:
                    break
            result_piece.append([to_time, offset])
            result.append(result_piece)
            offset += 1
        result_piece = [[from_time, 0]]
        for record in self.target.spikes_record:
            if from_time <= record <to_time:
                result_piece.append([record - 0.0001, 0])
                result_piece.append([record, offset])
                result_piece.append([record + 0.0001, 0])
            elif record >= to_time:
                break
        result_piece.append([to_time, 0])
        result.append(result_piece)
        return result





