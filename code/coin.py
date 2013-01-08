""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Solution to a problem from
Abelson and Sussman, Structure and Interpretation of Computer Programs, pg 37:

"How many different ways can we make change of $1.00, given half-dollars,
quarters, dimes, nickels and pennies?"

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

cache = {}
#coins = (50, 25, 10, 5, 1)
coins = (1, 5, 10, 25, 50)

def combinations(amount, num_coins):
    try:
        return cache[amount, num_coins]
    except KeyError:
        pass

    if amount < 0 or num_coins == 0:
        return 0
    if amount == 0:
        return 1

    coin = coins[num_coins-1]
    total = (combinations(amount-coin, num_coins) + 
             combinations(amount, num_coins-1))

    cache[amount, num_coins] = total
    return total
          

def summarize_cache():
    d = {}
    for num_coins in range(1, 6):
        d[num_coins] = []
        for amount in range(1, 100):
            if (amount, num_coins) in cache:
                d[num_coins].append(amount)

    for num_coins in range(1, 6):
        t = d[num_coins]
        t.sort()
        print num_coins, t
            

def main(script):
    print combinations(100, 5)
    summarize_cache()

if __name__ == '__main__':
    import sys
    main(*sys.argv)
