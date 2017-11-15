import re
import operator
from subprocess import call

files = open('article-list.txt', 'w')
ret = call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9a-zA-Z\-]+/index\.html"],
        stdout=files
        )
files.close()

files = open('article-list.txt', 'r')
categories = dict({"uncategorized":(0,0)})
for line in files:
    if line[len(line)-1] == '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    article.close()
    m = re.search('<h1><a.+?>(<span.+?>)?.+?(<\/span.+?>)?<\/a>', content)
    if m is None:
        category = "uncategorized"
    else:
        category = re.search('">[a-zA-Z]+?<\/', m.group())
        if category is None:
            category = "uncategorized"
        else:
            category = category.group()[2:-2]
    #try to determine word count
    if category is not "uncategorized":
        entry = re.search('<section class="tmd-post-content">(.|\n)+?<\/section>', content).group()
        articleList = re.split('<.+?>|&[#a-zA-Z0-9]+?;', entry)
        text = str()
        for s in articleList:
            if s is not '':
                text += s
        words = 0
        for s in re.split(' |\n', text):
            if s is not '':
                words += 1
    else:
        words = 0
    if category in categories:
        categories[category] = tuple(map(
            operator.add, categories[category], (1, words)))
    else:
        categories[category] = (1, words)
files.close()

total = 0
words = 0
for category in categories:
    total += categories[category][0]
    words += categories[category][1]
    if categories[category][0] is 0:
        avgwords = 0
    else:
        avgwords = int(categories[category][1]/categories[category][0])
    line = [str(category), str(categories[category][0]), str(avgwords)]
    print('{:>16} {:>8} {:>8}'.format(*line))
print("\nTotal: "+str(total)+"\t"+str(int(words/(total-categories["uncategorized"][0]))))
