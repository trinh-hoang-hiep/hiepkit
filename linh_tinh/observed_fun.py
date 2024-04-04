# nhóm 3
#####tuple (value, [])
def observedfunction1(txt):
    print(txt)

def observedfunction2needcall(txt):
    print(txt)
is_change=False
a=("excel1", is_change, [observedfunction1, observedfunction2needcall])

is_change=True
a=("excel2", is_change, [observedfunction1, observedfunction2needcall])
if a[1]:
    [i(a[0]) for i in a[2]] ##### ko alway, cần flag is_change