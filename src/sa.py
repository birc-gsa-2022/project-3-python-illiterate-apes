import argparse


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix array")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    print(f"Find every reads in {args.reads.name} " +
          f"in genome {args.genome.name}")


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
    #main()
