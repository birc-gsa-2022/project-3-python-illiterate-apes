from cmath import log10
from math import log2
import matplotlib.pyplot as plt
import numpy as np
import sa
import timeit



 


def main():
    
    
    #Construction

    #Worst Case
    string = "a"*10
    runtimes = runtimeConstruction(string)
    x = np.array([i[0] for i in runtimes])
    y = np.array([i[1] for i in runtimes])
    plt.title("Suffix Array construction algorithm - Radix Sort")
    plt.xlabel("string length")
    plt.ylabel("Runtime divided by x^2")
    y = [pair[1]/(pair[0]*pair[0]) for pair in zip(x,y)]
    plt.plot(x,y)
    plt.show()
    plt.title("Suffix Array construction algorithm - Radix Sort")
    plt.xlabel("string length")
    plt.ylabel("Runtime divided by x^3")
    y = [pair[1]/(pair[0]*pair[0]*pair[0]) for pair in zip(x,y)]
    plt.plot(x,y)
    plt.show()

    #Search

    #Worst Case

    string = "a"*10
    pattern = "a"*10
    runtimes = runtimeSearch(string, pattern)
    x = np.array([i[0] for i in runtimes])
    y = np.array([i[1] for i in runtimes])
    plt.title("Suffix Array binary search algorithmn")
    plt.xlabel("string and pattern length (They're the same)")
    plt.ylabel("Runtime")
    #y = [pair[1]/(pair[0]) for pair in zip(x,y)]
    plt.plot(x,y)
    plt.show()
    
def runtimeConstruction(string: str):
    """
    measures runtimes for suffix array construction
    """
    runtimes = []
    

    for i in range(1,30):
        start = timeit.default_timer()
        sa.radix_sort(sa.getSuffixes(string*i))
        stop = timeit.default_timer()
        runtimes.append([len(string*i), stop - start])

    
    return runtimes

def runtimeSearch(string: str, pattern: str):
    """
    measures runtimes for suffix array binary search
    """
    runtimes = []
    suffixArray = sa.radix_sort(sa.getSuffixes(string))

    for i in range(1,100):
        start = timeit.default_timer()
        sa.search(suffixArray*i,pattern*i,string)
        stop = timeit.default_timer()
        runtimes.append([len(string)*i, stop - start])

    
    return runtimes

if __name__ == "__main__":
    main()