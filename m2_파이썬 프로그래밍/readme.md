<테스트 오답노트>
Q6. 주어진 정수 리스트에서 가장 자주 등장하는 숫자(최빈값)를 찾아 반환하는 함수를 작성하세요. 만약 최빈값이 여러 개라면, 그 중 가장 작은 숫자를 반환하세요.
numbers = [1, 3, 2, 3, 4, 1, 3, 3]

def find_mode(numbers):
  from collections import Counter
  count =Counter(numbers)
  max_freq = max(count.values())
  frequent_numbers = [num for num, freq in count.items() if freq == max_freq]
  return min(frequent_numbers)

  numbers = [1, 3, 2, 3, 4, 1, 3, 3]
  print(find_mode(numbers))
----------------------------------------------------------------------------------------------------------------------------------------------------

  Q10. 숫자를 0으로 나누려 할 때 발생하는 예외를 처리하는 코드를 작성하세요.

  try:
  reslt = 10/0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
-----------------------------------------------------------------------------------------------------------------------------------------------------

hugging space 오픈소스 제공하는 곳!!
궁금한 건 논문 찾아보기!!
