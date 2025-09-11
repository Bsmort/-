import pytest 
from lab import sum_of_two

def test_sum_of_two_ex1():
  nums = [2, 7, 11, 15]
  target = 9
  expected = [0, 1]
  assert sum_of_two(nums, target) == expected

def test_sum_of_two_ex2():
  nums = [3, 2, 4]
  target = 6
  expected = [1, 2]
  assert sum_of_two(nums, target) == expected

def test_sum_of_two_ex3():
  nums = [3, 3]
  target = 6
  expected = [0, 1]
  assert sum_of_two(nums, target) == expected