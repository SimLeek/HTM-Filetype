import randomSample
from operator import attrgetter

max_neurons = 1000000000

class HTMLayer:

    def __init__(self):
        self.name = None
        self.num_neurons = None
        self.neurons = []
        self.possible_connections_per_neuron = None
        self.active_connections_per_neuron = None
        self.connected_permanence = None
        self.neighbors_per_neuron = None
        self.permanence_inc = None
        self.permanence_dec = None
        self.min_overlap = None

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
        self.name = seed
        self.num_neurons = num_neurons
        neuron_names = randomSample.randomSample(xrange(max_neurons),num_neurons, seed)
        #choose neuron names from here for uniqueness
        for i in range(0,num_neurons):
            next_neuron= HTMColumnNeuron()
            next_neuron.initial_startup(neuron_names[i], self)
            self.neurons.append(next_neuron)

        self.possible_connections_per_neuron = possible_connections_per_neuron
        self.active_connections_per_neuron = active_connections_per_neuron
        self.connected_permanence=connected_permanence
        self.neighbors_per_neuron = neighbors_per_neuron
        self.permanence_inc = permanence_inc
        self.permanence_dec = permanence_dec
        self.min_overlap = min_overlap

        return self

    def input_layers_array(self):
        #dummy function
        return [x for x in range(1000)]


def kth_score(neighbors, desired_local_activity):
    #scan over neighbors list, putting 'desired_local_activity' number of neighbors
    # into a sorted hash tree. Then, for the next neighbors, place them in the
    # sorted list and knock off the lowest member

    n_list = []
    for i, n in enumerate(neighbors):
        if i<desired_local_activity:
            n_list.append(n)
        else:
            if n.active_duty_cycle > n_list[-1].active_duty_cycle:
                n_list.pop()
                n_list.append(n)
        n_list.sort(key=attrgetter('active_duty_cycle'))

    return n_list[-1].active_duty_cycle


def max_duty_cycle(neighbors):
    #go through all and find max duty cycle

    max_duty_cycle_val = 0.0

    for n in neighbors:
        if n.active_duty_cycle > max_duty_cycle_val:
            max_duty_cycle_val = n.active_duty_cycle

    return max_duty_cycle_val

def update_active_duty_cycle(neuron):

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


def boost_function(active_duty_cycle, min_duty_cycle):

    if active_duty_cycle >= min_duty_cycle:
        return 1.0
    else:
        #todo: test if I should just increase by a constant every time, or
        # multiply this by a constant
        return 1/(min_duty_cycle - active_duty_cycle)


def update_overlap_duty_cycle(neuron):
    if neuron.overlap > neuron.parent.min_overlap:
        overlap_duty_cycle = neuron.overlap_duty_cycle - \
                            ((neuron.overlap_duty_cycle - 1.0)
                             /neuron.parent.integral_average_timesteps)
    else:
        overlap_duty_cycle = neuron.overlap_duty_cycle - \
                        (neuron.overlap_duty_cycle/
                         neuron.parent.integral_average_timesteps)

    return overlap_duty_cycle

class HTMSynapse:
    def __init__(self, neuron, permanence):
        self.neuron = neuron
        self.permanence = permanence

class HTMColumnCell:
    def __init__(self, parent, segments_per_cell):
        self.segments = []
        self.parent = parent
        self.segments_per_cell = segments_per_cell

    def get_previous_active_segment(self):
        pass

class HTMSegment:
    def __init__(self, parent, synapses_per_segment):
        self.was_learning = False
        self.is_active = False
        self.synapses = []
        self.parent = parent
        self.max_synapses = synapses_per_segment

    def get_previous_active_synapses(self, boolean):
        pass

class HTMColumnNeuron:

    def __init__(self):
        pass

    def get_previous_best_matching_cell(self):
        pass

    def check_predicted_and_learn(self):
        buPredicted = False
        IcChosen = False
        for c in self.cells:
            if c.wasPredicting == True:
                s = c.get_previous_active_segment()
                buPredicted = True
                c.active_state = 1
                if s.was_learning:
                    IcChosen = True
                    c.learn_state = 1
        if buPredicted == False:
            for c in self.cells:
                c.active_state=1
        if IcChosen == False:
            c,s = self.get_previous_best_matching_cell()
            c.learn_state = 1
            sUpdate = s.get_previous_active_synapses(True)
            self.segmentUpdateList.append(sUpdate)

    def reinforce_predicted(self):
        for c in self.cells:
            for s in c.segments:
                if s.is_active:
                    c.predictive_state = 1
                    activeUpdate = s.active_synapses(False)
                    self.segmentUpdateList.append(activeUpdate)

    def reinforce_segments(self):
        for c in self.cells:
            if c.learn_state == 1:
                c.adapt_segments(self.segmentUpdateList, True)
                self.segmentUpdateList = []
            elif c.active_state == 0 and c.prior_predictive_state == 1:
                c.adapt_segments(self.segmentUpdateList, False)
                self.segmentUpdateList = []


    def generate_potential_synapses(self):
        '''neurons = randomSample.randomSample(self.parent.input_layers_array(),
                            self.parent.possible_connections_per_neuron,
                            self.name)'''
        neurons = randomSample.randomSample(xrange(10000),
                                            self.parent.possible_connections_per_neuron,
                                            self.name)
        synapses = [HTMSynapse(x,0.0) for x in neurons]
        return synapses

    def initial_startup(self, name, layer):
        #everything in here should be serialized unless otherwise noted
        # unique identifier in this layer to identify neuron (random >=0 <=max_int)
        self.name = name
        # class of what layer we're in (NOT SERIALIZED)
        self.parent = layer
        # name of what layer we're in
        self.layer_name = self.parent.name

        self.potential_synapses = self.generate_potential_synapses()

        self.active_synapses = randomSample.randomSample(self.potential_synapses,
                                                         self.parent.active_connections_per_neuron,
                                                         self.name)

        for s in self.active_synapses:
            s.permanence = 1.0

        self.neighbors = randomSample.randomSample(self.parent.neurons,
                                                   self.parent.neighbors_per_neuron,
                                                   self.name)

        self.activated = 0
        self.overlap = 0
        self.boost = 0
        self.min_duty_cycle = 0
        self.active_duty_cycle = 0
        self.overlap_duty_cycle = 0
        self.segmentUpdateList = []

        return self


    #put these functions in layers to increase speed/memory
    def calculate_overlap(self):
        self.overlap=0
        for s in self.active_synapses:
            self.overlap = self.overlap + s.neuron.activated
        if self.overlap < self.parent.min_overlap:
            self.overlap = 0
        else:
            self.overlap = self.overlap * self.boost

    def calculate_inhibition(self):
        self.min_local_activity = kth_score(self.neighbors, self.parent.desired_local_activity)

        if self.overlap > 0 and self.overlap >= self.min_local_activity:
            self.activated = 1.0
            #parent.active_neurons.insert_front(self)
            #this way, partial activation can be calculated via one value from the parent

    def recalculate_permanences(self):
        """
        If this neuron was activated, strengthen/weaken connections
        :return:
        """

        for i, s in enumerate(self.active_synapses):
            if s.activated:
                s.permanence += self.parent.permanence_inc
                s.permanence = min(1.0, s.permanence)
            else:
                s.permanence -= self.parent.permanence_dec
                s.permanence = max(0.0, s.permanence)
                if s.permanence < self.parent.connected_permanence:
                    self.active_synapses.pop(i)

    def increase_all_permanences(self, increment):
        for s in self.potential_synapses:
            s.permanence+= increment
            if s.permanence > self.parent.connected_permanence:
                self.active_synapses.append(s)

    def recalculate_duty_cycles(self):
        """
        After all neurons had chance to activate, recalc how often they actually did
        :return:
        """

        self.min_duty_cycle = 0.01 * max_duty_cycle(self.neighbors)
        self.active_duty_cycle = update_active_duty_cycle(self)
        self.boost = boost_function(self.active_duty_cycle, self.min_duty_cycle)

        self.overlap_duty_cycle = update_overlap_duty_cycle(self)
        if self.overlap_duty_cycle < self.min_duty_cycle:
            self.increase_all_permanences(0.1*self.parent.connected_permanence)


if __name__ == "__main__":

    import HTMVisualizations
    import math

    '''layer = HTMLayer()
    layer.initial_startup(583475683,
                          100,
                          10,
                          2,
                          2,
                          0.6,
                          0.4,
                          0.1,
                          2)
    '''
    point_displayer = HTMVisualizations.vtk_points()

    layer_sqrt = math.ceil(math.sqrt(10000))

    layer_z = 0

    for i in range(10000):
        point_displayer.add_point([i%layer_sqrt, math.floor(i/layer_sqrt), layer_z], [255,200,200])

    #point_displayer.add_line(0, 1, [255, 200, 200])
    point_displayer.set_poly_data()

    point_displayer.visualize()







