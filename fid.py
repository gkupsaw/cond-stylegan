import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow import image

import tensorflow_gan as tfgan
import tensorflow_hub as hub

# For evaluating the quality of generated images
# Frechet Inception Distance measures how similar the generated images are to the real ones
# https://nealjean.com/ml/frechet-inception-distance/
# Lower is better
module = tf.keras.Sequential([hub.KerasLayer("https://tfhub.dev/google/tf2-preview/inception_v3/classification/4", output_shape=[1001])])
def fid_function(real_image_batch, generated_image_batch):
	"""
	Given a batch of real images and a batch of generated images, this function pulls down a pre-trained inception 
	v3 network and then uses it to extract the activations for both the real and generated images. The distance of 
	these activations is then computed. The distance is a measure of how "realistic" the generated images are.

	:param real_image_batch: a batch of real images from the dataset, shape=[batch_size, height, width, channels]
	:param generated_image_batch: a batch of images generated by the generator network, shape=[batch_size, height, width, channels]

	:return: the inception distance between the real and generated images, scalar
	"""
	INCEPTION_IMAGE_SIZE = (299, 299)
	real_resized = image.resize(real_image_batch, INCEPTION_IMAGE_SIZE)
	fake_resized = image.resize(generated_image_batch, INCEPTION_IMAGE_SIZE)
	module.build([None, 299, 299, 3])
	real_features = module(real_resized)
	fake_features = module(fake_resized)
	return tfgan.eval.frechet_classifier_distance_from_activations(real_features, fake_features)
