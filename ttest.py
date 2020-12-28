
import datetime
now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S.%f .')
print(now)

a=[1,2,3,4,5,6,7,8,9]
b=[[] for i in range(3)]
b[0].extend(a[0:1])
b[1].extend(a[3:4])
b[2].extend(a[5:6])
print(b)
# a=[]
# a[20]=0