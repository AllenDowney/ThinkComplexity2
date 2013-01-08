"""Solution to a brain teaser.

Author: Allen B. Downey
Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""


def recurse_levels(width, height):
    """Finds arrangements of bricks that make a wall with width and height,
    with no overlapping seams.

    Returns a dictionary that maps from a top-row configuration to the
    number of combinations that have that top row.

    A configuration is a tuple of seam locations.
    """
    # base case: if there's only one row, just enumerate the combos
    if height == 1:
        return bundle_combos(start=0, width=width, avoid=tuple())

    # otherwise make a recursive call
    d = recurse_levels(width, height-1)

    # for each top-row configuration, enumerate the combos for the next row
    res = {}
    for avoid, factor in d.iteritems():
        accumulate_combos(res, bundle_combos(0, width, avoid, factor))

    return res


def accumulate_combos(acc, new_d):
    """Updates acc with entries from new_d."""
    for combo, count in new_d.iteritems():
        acc[combo] = acc.get(combo, 0) + count


def bundle_combos(start, width, avoid, factor=1):
    """Makes a map from a top-row configuration to the
    number of combinations that have that top row.

    start: integer index of the end of the last brick placed
    width: integer width of the row
    avoid: tuple of locations where you can't put a seam
    factor: multiplier for the number of combinations
    """
    combos = enumerate_combos(start, width, avoid)
    d = {}
    for combo in combos:
        d[combo] = d.get(combo, 0) + factor
    return d


cache = {}

def enumerate_combos(start, width, avoid):
    """Enumerates top-row configurations and returns a list.

    start: integer index of the end of the last brick placed
    width: integer width of the row
    avoid: tuple of locations where you can't put a seam    
    """
    # see if we've already computed this
    try:
        return cache[start, width, avoid]
    except KeyError:
        pass

    # if we get to the end of the row, return an empty configuration 
    if start == width:
        return [tuple()]

    # enumerate the bricks
    bricks = [2, 3]
    combos = []
    for brick in bricks:

        # if we go past the end or hit a seam, skip it
        end = start+brick
        if end > width or end in avoid:
            continue
        
        # enumerate the rest of the row
        new_combos = enumerate_combos(end, width, avoid)

        # add this brick to the results
        if end < width:
            new_combos = add_brick(end, new_combos)

        # accumulate the combinations
        combos.extend(new_combos)

    cache[start, width, avoid] = combos
    return combos


def add_brick(end, combos):
    """Add the new brick to each combination in combos.

    Returns a new list.
    """
    return [combo + (end,) for combo in combos]


def how_many_combinations(width, height):
    """Returns the number of combinations with the given width and height.

    Converts from inches to 1.5 inch fundamental units.

    width: integer width in inches
    height: integer height in brick heights
    """
    d = recurse_levels(width*2 / 3, height)
    return sum(d.itervalues())


print how_many_combinations(12, 3)
print how_many_combinations(27, 5)
print how_many_combinations(48, 10)
