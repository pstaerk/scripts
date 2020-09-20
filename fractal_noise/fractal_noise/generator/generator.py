import numpy as np
from scipy import interpolate

class Generator:
    """Generator class for fractal noise"""
    def __init__(self, method='default'):
        self._method = method

    def generate_noise(self, l, amplitudes=[(1,1.), (.5, .5)]):
        """Generate 1d noise on length 1.

        :l: length that noise is generated for
        :amplitudes: array of amplitudes and frequencies pairs as tuples.

        :returns: noise array with noise values
        """
        if self._method == 'default':
            total_xs, frac_noise, noises = generate_def_noise(l, amplitudes)
        else:
            print('Feature not supported!!')

        return total_xs, frac_noise, noises


def generate_def_noise(l, amplitudes):
    """Generate noise with a interpolated random walk of different 
    frequencies and amplitudes.

    :l: length that noise is generated for
    :amplitudes: array of amplitudes and frequencies pairs as tuples.

    :returns: noise array with noise values
    """
    min_freq = min([a[0] for a in amplitudes])
    interpolate_steps = int(l / min_freq)
    noises = np.empty((len(amplitudes), interpolate_steps))
    total_xs = np.linspace(0, l, interpolate_steps)

    for i, (freq, amp) in enumerate(amplitudes):
        nr_of_samples = int(l/freq)
        # If there are less than 4 sample points quadratic interpolation won't work
        if nr_of_samples < 4:
            print(f'Warning: Less than 4 points of interpolation!!, skipping freq: {freq}')
            continue

        # Generate random noise at specified frequency, scaled with amplitude
        noise = amp * np.random.rand(nr_of_samples)

        # Generate interpolation
        xs = np.linspace(0, l, nr_of_samples)
        interp_func = interpolate.interp1d(xs, noise, kind='quadratic')
        noises[i, :] = interp_func(total_xs)

    frac_noise = np.sum(noises, axis=0)
    return total_xs, frac_noise, noises
