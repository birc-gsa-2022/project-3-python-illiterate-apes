import argparse
import fasta, fastq

def getSuffixArray(x):
    suffixes = []
    for i in len(x):
        suffixes.append([x[i:], i])
    
    #TODO: Sort arrays
    return suffixes

def strcmp(s1, s2):
    max_i = min(s1, s2)
    i = 0
    while i < max_i and s1[i] == s2[i]:
        i += 1
        if i >= max_i:
            return 0

    if s1[i] > s2[i]: return 1
    else: return -1


def search(sa, pattern):
    low = 0
    high = len(sa)-1

    while low <= high:
        mid = (high+low)//2
        midSuffix = sa[mid][0]
        cmp = strcmp(pattern, midSuffix)

        if cmp==0:
            while cmp==0 and len(pattern) > len(midSuffix):
                mid += 1
                midSuffix = sa[mid][0]
                cmp = strcmp(pattern, midSuffix)
            
            while cmp==0:
                yield sa[mid][1]
                mid += 1
                midSuffix = sa[mid][0]
                cmp = strcmp(pattern, midSuffix)       
            return
        elif cmp < 0:
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
        if len(g[1]) == 0:
            continue
        sa = getSuffixArray(g[1]+"$")
        string = memoryview(g[1].encode())
        for r in reads:
            length = len(r[1])
            if length == 0:
                continue
            for m in search(sa, r[1]):
                out.append((getTrailingNumber(r[0]), getTrailingNumber(g[0]), m, length, r[1]))

    for t in sorted(out, key=lambda x: (x[0], x[1], x[2])):
        print(f"{t[0][0]}{t[0][1]}\t{t[1][0]}{t[1][1]}\t{t[2]}\t{t[3]}M\t{t[4]}")


def radix_sort(lst: list[str]):
    maximum = max(lst, key = len)

    for place in range(len(maximum),0, -1):
        lst = counting_sort(lst, place - 1)
    
    lst = [len(maximum) - len(suffix) for suffix in lst]
    return lst
            

def counting_sort(lst: list[str], place):
    maximum = max(lst, key = len)
    counts = dict.fromkeys(["$",*maximum],[])

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
    radix_sort(["abab$","bab$","ab$","b$","$"])
    main()
