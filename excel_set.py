from openpyxl import load_workbook

load_wb = load_workbook("./route.xlsx", data_only=True)

load_ws = load_wb.active

i = 0
sA = []
sB = []
sC = []

for r in load_ws.rows:
    i = i + 1
    sA.append(r[0].value)
    sB.append(r[1].value)
    sC.append(r[2].value)
    if i == 518:
        break

with open('d:/route.txt', 'w+') as f:
    for i in range(0, 518):
        txt = "list.add(new Road(\"" + sB[i] + "\",\"" + sA[i] + "\",\"default\",\"" + sC[i] + "\"));\n"
        print(txt)
        f.write(txt)
