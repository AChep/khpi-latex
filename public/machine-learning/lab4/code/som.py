from matplotlib import pyplot as plt
from matplotlib import patches as patches
import numpy as np


class SOM:
	def __init__(self, net_x_dim, net_y_dim, num_features):
		self.network_dimensions = np.array([net_x_dim, net_y_dim])
		self.init_radius = min(self.network_dimensions[0],
		self.network_dimensions[1])
		# initialize weight vectors
		self.num_features = num_features
		self.initialize()
	
	def initialize(self):
		self.net = np.random.random((self.network_dimensions[0],
		self.network_dimensions[1], self.num_features))
	
	def train(self, data, num_epochs=100, init_learning_rate=0.01,
		resetWeights=False):
		if resetWeights:
			self.initialize()
		num_rows = data.shape[0]
		indices = np.arange(num_rows)
		self.time_constant = num_epochs / np.log(self.init_radius)
		
		# visualization
		if self.num_features == 3:
			fig = plt.figure()
		else:
			fig = None
		
		for i in range(1, num_epochs + 1):
			# interpolate new values for α(t) and σ (t)
			radius = self.decay_radius(i)
			learning_rate = self.decay_learning_rate(init_learning_rate, i, num_epochs)
			# visualization
			vis_interval = int(num_epochs/10)
			if i % vis_interval == 0:
				if fig is not None:
					self.show_plot(fig, i/vis_interval, i)
				print("SOM training epoches %d" % i)
				print("neighborhood radius ", radius)
				print("learning rate ", learning_rate)
				print("-------------------------------------")
			
			# shuffling data
			np.random.shuffle(indices)
			for record in indices:
				row_t = data[record, :]
				# find its Best Matching Unit
				bmu, bmu_idx = self.find_bmu(row_t)
				for x in range(self.network_dimensions[0]):
					for y in range(self.network_dimensions[1]):
						weight = self.net[x, y, :].reshape(1, self.num_features)
						w_dist = np.sum((np.array([x, y]) - bmu_idx) ** 2)
						# if the distance is within the current neighbourhood radius
						if w_dist <= radius ** 2:
							# update weight vectors wk using Eq. (3)
							influence = SOM.calculate_influence(w_dist, radius)
							new_w = weight + (learning_rate * influence * (row_t - weight))
							self.net[x, y, :] = new_w.reshape(1, self.num_features)
		if fig is not None:
			plt.show()

	@staticmethod
	def calculate_influence(distance, radius):
		return np.exp(-distance / (2 * (radius ** 2)))

	def find_bmu(self, row_t):
		bmu_idx = np.array([0, 0])
		# set the initial minimum distance to a huge number
		min_dist = np.iinfo(np.int).max
		# calculate the high-dimensional distance between each neuron and the input
		for x in range(self.network_dimensions[0]):
			for y in range(self.network_dimensions[1]):
				weight_k = self.net[x, y, :].reshape(1, self.num_features)
				# compute distances dk using Eq. (1)
				sq_dist = np.sum((weight_k - row_t) ** 2)
				# compute winning node c using Eq. (2)
				if sq_dist < min_dist:
					min_dist = sq_dist
					bmu_idx = np.array([x, y])
		# get vector corresponding to bmu_idx
		bmu = self.net[bmu_idx[0], bmu_idx[1], :].reshape(1, self.num_features)
		return bmu, bmu_idx

	def predict(self, data):
		# find its Best Matching Unit
		bmu, bmu_idx = self.find_bmu(data)
		return bmu, bmu_idx

	def decay_radius(self, iteration):
		return self.init_radius * np.exp(-iteration / self.time_constant)

	def decay_learning_rate(self, initial_learning_rate, iteration, num_iterations):
		return initial_learning_rate * np.exp(-iteration / num_iterations)

	def show_plot(self, fig, position, epoch):
		# setup axes
		ax = fig.add_subplot(2, 5, position, aspect="equal")
		ax.set_xlim((0, self.net.shape[0] + 1))
		ax.set_ylim((0, self.net.shape[1] + 1))
		ax.set_title('Ep: %d' % epoch)
		# plot the rectangles
		for x in range(1, self.net.shape[0] + 1):
			for y in range(1, self.net.shape[1] + 1):
				print(self.net[x - 1, y - 1, :])
				ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1,
					facecolor=self.net[x - 1, y - 1, :],
					edgecolor='none'))