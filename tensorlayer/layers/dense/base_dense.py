#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
from tensorlayer.layers.core import LayersConfig

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = [
    'Dense',
]


class Dense(Layer):
    """The :class:`Dense` class is a fully connected layer.

    Parameters
    ----------
    n_units : int
        The number of units of this layer.
    act : activation function
        The activation function of this layer.
    W_init : initializer
        The initializer for the weight matrix.
    b_init : initializer or None
        The initializer for the bias vector. If None, skip biases.
    W_init_args : dictionary
        The arguments for the weight matrix initializer.
    b_init_args : dictionary
        The arguments for the bias vector initializer.
    name : None or str
        A unique layer name.

    Examples
    --------
    With TensorLayer

    >>> net = tl.layers.Input(x, name='input')
    >>> net = tl.layers.Dense(net, 800, act=tf.nn.relu, name='relu')

    Without native TensorLayer APIs, you can do as follow.

    >>> W = tf.Variable(
    ...     tf.random_uniform([n_in, n_units], -1.0, 1.0), name='W')
    >>> b = tf.Variable(tf.zeros(shape=[n_units]), name='b')
    >>> y = tf.nn.relu(tf.matmul(inputs, W) + b)

    Notes
    -----
    If the layer input has more than two axes, it needs to be flatten by using :class:`Flatten`.

    """

    def __init__(
            self,
            n_units=100,
            act=None,
            W_init=tf.truncated_normal_initializer(stddev=0.1),
            b_init=tf.constant_initializer(value=0.0),
            W_init_args=None,
            b_init_args=None,
            name=None,  # 'dense',
    ):

        # super(Dense, self
        #      ).__init__(prev_layer=prev_layer, act=act, W_init_args=W_init_args, b_init_args=b_init_args, name=name)
        super().__init__(name)

        self.n_units = n_units
        self.act = act
        self.W_init = W_init
        self.b_init = b_init
        self.W_init_args = W_init_args
        self.b_init_args = b_init_args

        self.n_in = int(self.inputs.get_shape()[-1])
        # self.inputs_shape = self.inputs.shape.as_list() #
        # self.outputs_shape = [self.inputs_shape[0], n_units]

        logging.info(
            "Dense  %s: %d %s" %
            (self.name, self.n_units, self.act.__name__ if self.act is not None else 'No Activation')
        )

        if self.inputs.shape.ndims != 2:
            raise AssertionError("The input dimension must be rank 2, please reshape or flatten it")

    def build(self, inputs):
        # self._make_weight(name=self.name, name2="W", shape=(self.n_in, self.n_units), initializer=self.)
        # if self.b_init is not None:
        #     self._make_weight(name=self.name, name2="b", shape=(self.n_units))
        self.W = tf.get_variable(
            name='W', shape=(self.n_in, self.n_units), initializer=self.W_init, dtype=LayersConfig.tf_dtype,
            **self.W_init_args
        )
        if self.b_init is not None:
            try:
                self.b = tf.get_variable(
                    name='b', shape=(self.n_units), initializer=self.b_init, dtype=LayersConfig.tf_dtype,
                    **self.b_init_args
                )
            except Exception:  # If initializer is a constant, do not specify shape.
                self.b = tf.get_variable(
                    name='b', initializer=self.b_init, dtype=LayersConfig.tf_dtype, **self.b_init_args
                )
        self.add_weights(self.W, self.b)

    def forward(self, inputs, is_train):
        outputs = tf.matmul(inputs, self.W)
        if self.b_init is not None:
            outputs = tf.add(z, self.b)
        outputs = self.act(outputs)
        return outputs
