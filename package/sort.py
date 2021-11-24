def quick(list, begin, end) -> None:
    middle = list[(begin + end) // 2]
    i = begin
    j = end
    if begin < end:
        while True:
            while list[i]['age'] < middle['age']:
                i += 1
            while list[j]['age'] > middle['age']:
                j -= 1
            if i >= j:
                middle_index = j
                break
            list[i], list[j] = list[j], list[i]
            i += 1
            j -= 1
        quick(list, begin, middle_index)
        quick(list, middle_index + 1, end)


def quick_sort(list) -> None:
    quick(list, 0, len(list) - 1)
