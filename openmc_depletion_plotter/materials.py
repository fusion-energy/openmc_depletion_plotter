import openmc


class Materials(openmc.Materials):

    def mymethod(self):
        pass

openmc.Materials = Materials
