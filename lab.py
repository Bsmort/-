def sum_of_two(nums: list, target: int) -> list:
    step = 0
    result = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] + nums[j] == target:
                result = [i, j]
                step = 1
                break
        if step == 1:
            break
    return result 
#print(sum_of_two([2, 7, 11, 15], 9)) 
#print(sum_of_two([3, 2, 4], 6))
#print(sum_of_two([3, 3], 6))

    
