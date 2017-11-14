import re
from subprocess import call

files = open('list', 'w')
ret = call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9a-zA-Z\-]+/index\.html"],
        stdout=files
        )
files.close()

files = open('list', 'r')
categories = dict({"uncategorized":0})
uncat = open('uncategorized.txt', 'w')
for line in files:
    if line[len(line)-1] == '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    m = re.search('<h1><a.+?>(<span.+?>)?.+?(<\/span.+?>)?<\/a>', content)
    if m is None:
        categories["uncategorized"] += 1
        uncat.write(line+"\n")
    else:
        category = re.search('">[a-zA-Z]+?<\/', m.group())
        if category is None:
            categories["uncategorized"] += 1
            uncat.write(line+"\n")
        else:
            category = category.group()[2:-2]
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
    article.close()
uncat.close()
files.close()

total = 0
for category in categories:
    total += categories[category]
    print(str(category)+": "+str(categories[category]))
print("\nTotal: "+str(total))
