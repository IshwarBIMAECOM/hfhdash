import numpy as np

class array:

	def __init__(self, *array_power):

		for i in array_power:
			self.array = np.array(array_power)
			self.display = str(i)
	# def __repr__(self):
	# 	return f"the array powers are {self.display}"
