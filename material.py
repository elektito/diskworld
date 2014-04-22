class Material:
    def __init__(self, name, color, density):
        self.name = name
        self.color = color
        self.density = density

    def __repr__(self):
        return "<Material '{}'>".format(self.name)
