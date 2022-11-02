import argparse
import fasta, fastq
import re

def getSuffixes(x: memoryview):
    """
    Gets all suffixes from a string
    """
    suffixes = [x[i:] for i in range(0, len(x))] 
    return suffixes

def getTrailingNumber(s):
    m = re.search(r'\d+$', s)
    return (s[:m.start()], int(s[m.start():]))

def lower(a: str, x: str, sa: memoryview, lo: int, hi: int, offset: int) -> int:
    """Finds the lower bound of `a` at `offset` in the block defined by `lo:hi`."""
    while lo < hi:  # Search in sa[lo:hi]
        m = (lo + hi) // 2
        if x[sa[m] + offset % len(x)] < a: # compare at column offset in sa
            lo = m + 1
        else:
            hi = m
    return lo

def upper(a: str, x: str, sa: memoryview, lo: int, hi: int, offset: int) -> int:
    """Finds the upper bound of `a` at `offset` in the block defined by `lo:hi`."""
    return lower(chr(ord(a) + 1), x, sa, lo, hi, offset)

def search(sa, pattern, genome):
    lo, hi = 0, len(sa)
    for offset, a in enumerate(pattern):
        lo = lower(a, genome, sa, lo, hi, offset)
        hi = upper(a, genome, sa, lo, hi, offset)
    for sol in sa[lo:hi]:
        yield sol+1
    return
    
def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix array")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()

    genomes = fasta.fasta_parse(args.genome)
    reads = fastq.fastq_parser(args.reads)

    out = []

    for g in genomes:
        gen = g[1]+"$"
        if len(g[1]) == 0:
            continue
        genView = memoryview(gen.encode())
        sa = radix_sort(getSuffixes(genView))
        # print("suffix array: ",sa)
        for r in reads:
            length = len(r[1])
            if length == 0:
                continue
            matches = search(sa, r[1], gen)
            for m in matches:
                out.append((getTrailingNumber(r[0]), getTrailingNumber(g[0]), m, length, r[1]))

    for t in sorted(out, key=lambda x: (x[0], x[1], x[2])):
        print(f"{t[0][0]}{t[0][1]}\t{t[1][0]}{t[1][1]}\t{t[2]}\t{t[3]}M\t{t[4]}")


def radix_sort(lst: list[memoryview]):
    # print("Radix sort", len(lst))
    maximum = max(lst, key = len)

    for place in range(len(maximum),0, -1):
        lst = counting_sort(lst, place - 1)
    
    lst = [len(maximum) - len(suffix) for suffix in lst]
    return lst
            

def counting_sort(lst: list[memoryview], place):
    maximum = max(lst, key = len)
    counts = dict.fromkeys(["$",*sorted(maximum)],[])
    for string_index in range(len(lst)):
        if place >= len(lst[string_index]):
            counts["$"] = [*counts["$"], lst[string_index]]
            
        else:
            counts[lst[string_index][place]] = [*counts[lst[string_index][place]], lst[string_index]]

    ordered = []
    for key in counts:
        ordered += counts[key]
    return ordered
    
    
if __name__ == '__main__':
    main()
