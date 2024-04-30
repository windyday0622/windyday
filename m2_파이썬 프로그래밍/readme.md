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
파이썬 깔기
우분투, 리눅스 깔기
======================================================================================================================================================
# Q. 다른 타입의 숫자 2개를 입력받아 큰 수를 출력하세요.
num1 = int(input("첫번째 숫자"))
num2 = int(input("두번째 숫자"))
if num1>num2:
  print(num1)
elif num1<num2:
  print(num2)
else:
  print("큰 수가 없습니다.")
---------------------------------------------------------------------------------------------------------------------------------------------------------
클래스? 객체?


<오답노트>
Q. 입력받은 문자열의 각 문자를 그 다음 문자로 변경하여 출력하세요.

def shift_characters(input_str):
    shifted_str = ""
    for i in range(len(input_str)):
        # 현재 문자를 다음 문자로 변경하여 추가합니다.
        shifted_str += chr(ord(input_str[i]) + 1)
        # 마지막 문자인 경우, 첫 번째 문자로 이동합니다.
        if shifted_str[-1] > 'z':
            shifted_str = chr(ord(shifted_str[-1]) - 26)
    return shifted_str

# 문자열 입력 받기
input_str = input("문자열을 입력하세요: ")

# 문자열 각 문자를 다음 문자로 변경하여 출력
print("결과:", shift_characters(input_str))
