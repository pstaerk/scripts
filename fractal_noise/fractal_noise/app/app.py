from fractal_noise.generator import generator
import matplotlib.pyplot as plt

def app():
    """Main app.

    """
    gen = generator.Generator()
    amps = [(20, .4), (12, .4), (7, .7), (1, .05), (.1, .01)]
    l = 100
    xs, frac, noise = gen.generate_noise(l, amps)

    # Plot the noise and the noise values
    fig, axes = plt.subplots(len(amps))

    for i, (freq, amp) in enumerate(amps):
        axes[i].set_title(freq)
        axes[i].plot(xs, noise[i])
        
    plt.show()

    plt.plot(frac)
    plt.show()
