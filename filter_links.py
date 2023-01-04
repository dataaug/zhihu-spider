with open('zhihu_valid_links.txt', 'r') as fr:
    lines = fr.readlines()
    lines = [line.strip() for line in lines]
    lines = [x for x in lines if x]
    lines = [x.split('|*|') for x in lines]

lines = [[x[0], x[1].replace(' - 知乎',''), int(x[2].replace(',',''))] for x in lines]

len(lines)

# 按照数量筛选
lines = [x for x in lines if x[2] > 5]
print(len(lines))

links_need = [x[0] for x in lines]

# texts =  [x[1] for x in lines]

# len(texts)

with open('need_links.txt', 'w') as fw:
    for item in links_need:
        fw.write(item + '\n')



