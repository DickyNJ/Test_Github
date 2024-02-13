from errorAnalyzer import ErrorAnalyzer

list1 = [240, 216, 224, 224, 224, 224, 216, 224, 224, 224, 224, 224, 224, 224, 224]
width = [40, 48, 40, 40, 48, 24, 48, 48, 48, 48, 48, 48, 48, 48, 48]

result,flag = -1, None

ceshi = ErrorAnalyzer(12, 4, 8) # error_range, error_range_width数据都从yaml文件中读取
for i in range(len(list1)):
    result,flag = ceshi.analyze_new(list1[i],width[i])
    if flag:
        print(i)
        break
print("result:",result)
print("flag:",flag)
#123
