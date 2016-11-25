from bisect import bisect_left

def binSearch(arr, val):
  """ function for running binary search on a sorted list.
  @param arr (list) a sorted list of integers to search
  @param val (int)  a integer to search for in the sorted array
  @return (int) the index of the element if it is found and -1 otherwise.
  """
  i = bisect_left(arr, val)
  if i != len(arr) and arr[i] == val:
    return i
  return -1

