import re
from subprocess import call

files = open('list', 'w')
call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9][0-9]/[a-zA-Z-]+/index\.html"],
        stdout=files
        )
files.close()
categories = dict({"uncategorized":0})
files = open('list', 'r')

for line in files:
    if line[len(line)-1] == '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    m = re.search('<div class="sections intro subtitle">(.|\n)*?<a.+?>.+<\/a>(.|\n)*?<\/div>', content)
    if m is None:
        categories["uncategorized"] += 1
    else:
        category = re.search('>.+?<\/a>', m.group()).group()[1:-4]
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
    article.close()
files.close()
total = 0
for key in categories:
    total += categories[key]
    print(str(key)+": "+str(categories[key]))
print("\nTotal: "+str(total))
