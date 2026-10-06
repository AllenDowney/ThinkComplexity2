import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2.0


def three_frame(world, n_seq, seed=17):
    """Draw three timesteps.
    
    world: object with step, loop, and draw
    n_seq: 3-tuple, number of steps before each draw
    seed: random see for NumPy
    """
    np.random.seed(seed)
    plt.figure(figsize=(10, 4))

    for i, n in enumerate(n_seq):
        plt.subplot(1, 3, i+1)
        world.loop(n)
        world.draw()

    plt.tight_layout()
    

def savefig(filename, **options):
    """Save the current figure.

    Keyword arguments are passed along to plt.savefig

    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html

    filename: string
    """
    print("Saving figure to file", filename)
    plt.savefig(filename, **options)


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d


def decorate(**options):
    """Decorate the current axes.

    Call decorate with keyword arguments like

    decorate(title='Title',
             xlabel='x',
             ylabel='y')

    The keyword arguments can be any of the axis properties

    https://matplotlib.org/api/axes_api.html

    In addition, you can use `legend=False` to suppress the legend.

    And you can use `loc` to indicate the location of the legend
    (the default value is 'best')
    """
    loc = options.pop("loc", "best")
    if options.pop("legend", True):
        legend(loc=loc)

    plt.gca().set(**options)
    plt.tight_layout()


def legend(**options):
    """Draws a legend only if there is at least one labeled item.

    options are passed to plt.legend()
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html

    """
    underride(options, loc="best", frameon=False)

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, **options)


def set_palette(*args, **kwds):
    """Set the matplotlib color cycler.

    args, kwds: same as for sns.color_palette

    Also takes a boolean kwd, `reverse`, to indicate
    whether the order of the palette should be reversed.

    returns: list of colors
    """
    reverse = kwds.pop('reverse', False)
    palette = sns.color_palette(*args, **kwds)

    palette = list(palette)
    if reverse:
        palette.reverse()

    cycler = plt.cycler(color=palette)
    plt.gca().set_prop_cycle(cycler)
    return palette




# Cell magic for adding a method to a class that was defined in an earlier
# cell, so a class can be presented one method at a time.  From ThinkPython.
#
#     %%add_method_to ClassName
#
#         def method(self):
#             ...

import re


def extract_function_name(text):
    """Find a function definition and return its name.

    text: String

    returns: String or None
    """
    pattern = r"def\s+(\w+)\s*\("
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


# the magic is only defined if we're running in Jupyter
try:
    from IPython.core.magic import register_cell_magic

    @register_cell_magic
    def add_method_to(args, cell):

        # get the name of the function defined in this cell
        func_name = extract_function_name(cell)
        if func_name is None:
            return "This cell doesn't define any new functions."

        # get the class we're adding it to
        namespace = get_ipython().user_ns
        class_name = args.strip()
        cls = namespace.get(class_name, None)
        if cls is None:
            return f"Class '{class_name}' not found."

        # save the old version of the function if it was already defined
        old_func = namespace.get(func_name, None)
        if old_func is not None:
            del namespace[func_name]

        # execute the cell to define the function
        get_ipython().run_cell(cell)

        # get the newly defined function
        new_func = namespace.get(func_name, None)
        if new_func is None:
            return f"This cell didn't define {func_name}."

        # add the function to the class and remove it from the namespace
        setattr(cls, func_name, new_func)
        del namespace[func_name]

        # restore the old function to the namespace
        if old_func is not None:
            namespace[func_name] = old_func

except (ImportError, NameError):
    pass
