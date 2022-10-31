import argparse
import fasta, fastq
import re

def getSuffixes(x):
    """
    Gets all suffixes from a string
    """
    suffixes = [x[i:] for i in range(0, len(x))] 
    # print("list of unordered suffixes: ",suffixes) 
    return suffixes

def getTrailingNumber(s):
    m = re.search(r'\d+$', s)
    return (s[:m.start()], int(s[m.start():]))

def strcmp(s1, index, x):
    max_i = min(len(s1), len(x)-index)
    i = 0
    while i < max_i and s1[i] == x[index+i]:
        i += 1
        if i >= max_i:
            return 0
    if s1[i] > x[index+i]: return 1
    else: return -1


def search(sa, pattern, genome):
    low = 0
    high = len(sa)-1

    while True:
        mid = (high+low)//2
        midSuffix = sa[mid]
        # print(high, low, mid)
        cmp = strcmp(pattern, midSuffix, genome)

        if cmp==0:
            while cmp==0 and len(pattern) > len(genome) - midSuffix:
                mid += 1
                if mid >= len(sa): return
                midSuffix = sa[mid]
                cmp = strcmp(pattern, midSuffix, genome)
            while cmp==0:
                yield genome[sa[mid]:]
                mid += 1
                if mid >= len(sa): return
                midSuffix = sa[mid]
                cmp = strcmp(pattern, midSuffix, genome)
            return
        else:
            if high-low <= 1:
                return
            if cmp < 0:
                high = mid
            else:
                low = mid

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
        sa = radix_sort(getSuffixes(gen))
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


def radix_sort(lst: list[str]):
    # print("Radix sort", len(lst))
    maximum = max(lst, key = len)

    for place in range(len(maximum),0, -1):
        lst = counting_sort(lst, place - 1)
    
    lst = [len(maximum) - len(suffix) for suffix in lst]
    return lst
            

def counting_sort(lst: list[str], place):
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
