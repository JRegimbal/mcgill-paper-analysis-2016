import re
from subprocess import call

files = open('article-list.txt', 'w')
call(
        ["find", ".", "-regex",
            "./\(news\|opinion\|student\-living\|features\|sci\-tech\|a\-e\|sports\|cartoons\)/[a-zA-Z0-9\-]+/index\.html"],
        stdout=files
        )
files.close()

files = open('article-list.txt', 'r')
categories = dict({"uncategorized":0})
for line in files:
    if line[len(line)-1] is '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    article.close()

    m = re.search('article:published.+2016.+>', content)
    if m is not None:
        category = re.search('[a-z-]+', line).group()
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1
files.close()

total = 0
for key in categories:
    total += categories[key]
    print(str(key)+": "+str(categories[key]))
print("\nTotal: "+str(total))
