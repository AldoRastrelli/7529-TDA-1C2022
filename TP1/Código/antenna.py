class Antenna:
    def __init__(self, id = None, location = None, radius = None):
        """ Constructor. """

        self.id = id
        self.location = location
        self.radius = radius
        self.s_i = calculate_s_i(location, radius)
        self.t_i = location + radius

    def __str__(self):
        """ Returns a string with the object's id. """

        return str(self.id)

    def get_superposition_with(self, another_antenna):
        return self.t_i - another_antenna.s_i
    
    def s_i_is_equal_with(self, another_antenna):
        return self.s_i == another_antenna.s_i

    def is_inside_relevant_range_of(self, k):
        """ Returns true if the antenna starts its coverage inside the route given by k kilometers. If not, returns false. """
        return self.s_i < k

def calculate_s_i(location, radius):
    s_i = location - radius
    if s_i < 0:
        s_i = 0
    
    return s_i