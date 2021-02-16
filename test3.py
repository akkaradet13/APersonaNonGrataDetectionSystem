# n = 0
# for i in range(100):
#     if i%10 == 1 :
#         n += 1
#         print(i)
# print(n)

# x = None
# 
# if x is not None:
    # print('x')
# else:
    # print('y')
x = 0
while True:
    print(f'{x},{x%10}')
    x += 1
    if x == 30 : x = 0