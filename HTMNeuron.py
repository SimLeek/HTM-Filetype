import randomSample
import math
from operator import itemgetter, attrgetter, methodcaller

max_neurons = 1000000000

class HTMLayer:

    def initial_startup(self,
                        seed,
                        num_neurons,
                        possible_connections_per_neuron,
                        active_connections_per_neuron,
                        neighbors_per_neuron,
                        connected_permanence,
                        permanence_inc,
                        permanence_dec,
                        min_overlap=20
                        ):
        # unique identifier in this group to identify layer
        self.name = randomSample.randomSample(xrange(max_neurons),1)
        self.num_neurons = num_neurons
        neuron_names = randomSample.randomSample(xrange(max_neurons),num_neurons)
        #choose neuron names from here for uniqueness
        self.neurons=[]
        for i in range(0,num_neurons):
            next_neuron= HTMColumnNeuron.initial_startup(neuron_names[i], self)
            self.neurons.append(next_neuron)

        self.possible_connections_per_neuron = possible_connections_per_neuron
        self.active_connections_per_neuron = active_connections_per_neuron
        self.connected_permanence=connected_permanence
        self.neighbors_per_neuron = neighbors_per_neuron
        self.permanence_inc = permanence_inc
        self.permanence_dec = permanence_dec
        self.min_overlap = min_overlap

def kthScore(neighbors, desired_local_activity):
    #scan over neighbors list, putting 'desired_local_activity' number of neighbors
    # into a sorted hash tree. Then, for the next neighbors, place them in the
    # sorted list and knock off the lowest member

    nList = []
    for i, n in enumerate(neighbors):
        if i<desired_local_activity:
            nList.append(n)
        else:
            if n.active_duty_cycle > nList[-1].active_duty_cycle:
                nList.pop()
                nList.append(n)
        nList.sort(key=attrgetter('active_duty_cycle'))

    return nList[-1].active_duty_cycle


def maxDutyCycle(neighbors):
    #go through all and find max duty cycle

    max_duty_cycle = 0.0

    for n in neighbors:
        if n.active_duty_cycle > max_duty_cycle:
            max_duty_cycle = n.active_duty_cycle

    return max_duty_cycle

def updateActiveDutyCycle(neuron):

    if neuron.activated:
        #subtract average out but add 1.
        active_duty_cycle = neuron.active_duty_cycle - \
                            ((neuron.active_duty_cycle - 1.0)
                             /neuron.parent.integral_average_timesteps)
    else:
        #subtract average out. Never equals 0.
        # Accurate at high value, may need to add floor function for low values.
        active_duty_cycle = neuron.active_duty_cycle - \
                        (neuron.active_duty_cycle/
                         neuron.parent.integral_average_timesteps)

    return active_duty_cycle


def boostFunction(active_duty_cycle, min_duty_cycle):

    if active_duty_cycle >= min_duty_cycle:
        return 1.0
    else:
        #todo: test if I should just increase by a constant every time, or
        # multiply this by a constant
        return 1/(min_duty_cycle - active_duty_cycle)


def updateOverlapDutyCycle(neuron):
    if neuron.overlap > neuron.parent.min_overlap:
        overlap_duty_cycle = neuron.overlap_duty_cycle - \
                            ((neuron.overlap_duty_cycle - 1.0)
                             /neuron.parent.integral_average_timesteps)
    else:
        overlap_duty_cycle = neuron.overlap_duty_cycle - \
                        (neuron.overlap_duty_cycle/
                         neuron.parent.integral_average_timesteps)

    return overlap_duty_cycle


class HTMColumnNeuron:
    def potential_synapses(self):
        return randomSample.randomSample(self.parent.input_layers_array(),
                            self.parent.possible_connections_per_neuron,
                            self.name)



    def initial_startup(self, name, layer):
        # unique identifier in this layer to identify neuron (random >=0 <=max_int)
        self.name = name
        # class of what layer we're in (NOT SERIALIZED)
        self.parent = layer
        # name of what layer we're in
        self.layer_name = self.parent.name

        self.active_synapses = randomSample.randomSample(self.potential_synapses(),
                                                         self.parent.active_connections_per_neuron,
                                                         self.name)

        self.neighbors = randomSample.randomSample(self.parent.neurons,
                                                   self.parent.neighbors_per_neuron,
                                                   self.name)

        self.activated = 0

    #put these functions in layers to increase speed/memory
    def calculate_overlap(self):
        self.overlap=0
        for s in self.potential_synapses():
            self.overlap = self.overlap + s.neuron.activated
            if s == self.last_connected_synapse:
                break
        if self.overlap < self.parent.min_overlap:
            self.overlap = 0
        else:
            self.overlap = self.overlap * self.boost

    def calculate_inhibition(self):
        self.min_local_activity = kthScore(self.neighbors, self.parent.desired_local_activity)

        if self.overlap > 0 and self.overlap >= self.min_local_activity:
            self.activated = 1.0
            #parent.active_neurons.insert_front(self)
            #this way, partial activation can be calculated via one value from the parent

    def recalculate_permanences(self):
        """
        If this neuron was activated, strengthen/weaken connections
        :return:
        """

        for s in self.potential_synapses:
            if s.activated:
                s.permanence += self.parent.permanence_inc
                s.permanence = min(1.0, s.permanence)
            else:
                s.permanence -= self.parent.permanence_dec
                s.permanence = max(0.0, s.permanence)
            if s == self.last_connected_synapse:
                break

    def recalculate_duty_cycles(self):
        """
        After all neurons had chance to activate, recalc how often they actually did
        :return:
        """

        self.min_duty_cycle = 0.01* maxDutyCycle(self.neighbors)
        self.active_duty_cycle = updateActiveDutyCycle(self)
        self.boost = boostFunction(self.active_duty_cycle, self.min_duty_cycle)

        self.overlap_duty_cycle = updateOverlapDutyCycle(self)
        if self.overlap_duty_cycle < self.min_duty_cycle:
            self.increase_all_permanences(0.1*self.parent.connected_permanence)










