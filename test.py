import pandas as pd

l1 = [1, 2, 3, 4, 5]


for i in l1:
    try:
        if i == 3:
            pd.read_csv("oscar")
        print("----",i)
    except:
        print("error")
    else:
        print("if not fails")