# Python program for implementation of Quicksort Sort

# This implementation utilizes pivot as the last element in the nums list
# It has a pointer to keep track of the elements smaller than the pivot
# At the very end of partition() function, the pointer is swapped with the pivot
# to come up with a "sorted" nums relative to the pivot


def partition(l, r, nums):
  # Last element will be the pivot and the first element the pointer
  pivot, ptr = nums[r], l
  for i in range(l, r):
    if nums[i] <= pivot:
      # Swapping values smaller than the pivot to the front
      nums[i], nums[ptr] = nums[ptr], nums[i]
      ptr += 1
  # Finally swapping the last element with the pointer indexed number
  nums[ptr], nums[r] = nums[r], nums[ptr]
  return ptr

# With quicksort() function, we will be utilizing the above code to obtain the pointer
# at which the left values are all smaller than the number at pointer index and vice versa
# for the right values.


def quicksort(l, r, nums):
  if len(nums) == 1: # Terminating Condition for recursion. VERY IMPORTANT!
    return nums
  if l < r:
    pi = partition(l, r, nums)
    quicksort(l, pi-1, nums) # Recursively sorting the left values
    quicksort(pi+1, r, nums) # Recursively sorting the right values
  return nums



# Python program to merge
# two sorted arrays

# Merge ar1[] and ar2[]
def merge(ar1, ar2):
    merged = []
    n = len(ar1)
    m = len(ar2)
    i = 0
    j = 0
    while i < n and j < m:
        #print(f"i: {i} j: {j} ar1: {ar1[i]} ar2:{ar2[j]} ")
        #print(f"{merged}")
        if(ar1[i] < ar2[j]):
            merged.append(ar1[i])
            i +=1
        else:
            merged.append(ar2[j])
            j +=1
    if (i == n):
        for k in range(j,m):
            merged.append(ar2[k])    
    if (j == m):
        for k in range(i,n):
            merged.append(ar1[k])        
    return merged

#quicksort merge is probably overkill for this thing but heres a template
#in case we want to go down this route.
ar1 = [1, 5, 9, 10, 15, 20]
ar2 = [2, 3, 8, 13]
m = len(ar1)
n = len(ar2)


a1 = [4, 5, 1, 2, 3]
a2 = [10,8,0,9]
sorted1 = quicksort(0, len(a1)-1, a1)
sorted2 = quicksort(0, len(a2)-1, a2)

for i in range(len(sorted1)):
   print(f"sorted1 {sorted1[i]}")

for i in range(len(sorted2)):
   print(f"sorted2 {sorted2[i]}")

merged = merge(sorted1, sorted2)


for i in range(len(merged)):
   print(f"merged {merged[i]}", "")

# print("before Merging \nFirst Array:", end="")
# for i in range(m):
#   print(ar1[i])

# print("\nSecond Array: ", end="")
# for i in range(n):
#   print(ar2[i])

# merged = merge(ar1, ar2)

# print("After Merging \nFirst Array:", end="")
# for i in range(len(merged)):
#     print(merged[i])

# This code is contributed
# by Anant Agarwal.
