import re
import operator
from subprocess import call

files = open('article-list.txt', 'w')
call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9][0-9]/[a-zA-Z-]+/index\.html"],
        stdout=files
        )
files.close()
categories = dict({"uncategorized":(0,0)})
files = open('article-list.txt', 'r')

for line in files:
    if line[len(line)-1] == '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    article.close()
    m = re.search('<div class="sections intro subtitle">(.|\n)*?<a.+?>.+<\/a>(.|\n)*?<\/div>', content)
    if m is None:
        categories["uncategorized"] += 1
    else:
        category = re.search('>.+?<\/a>', m.group()).group()[1:-4]
    # try to establish word count
    entry = re.search('<div class="[a-z ]+?text"(.|\n)+?<div class="spacer">', content).group()
    articleList = re.split('<.+?>|&.+?;|\\xa0', entry)
    text = str()
    for s in articleList:
        if s is not '':
            text += s
    words = 0
    for s in re.split(' |\n', text):
        if s is not '':
            words += 1
    if category in categories:
        categories[category] = tuple(map(
            operator.add, categories[category], (1, words)))
    else:
        categories[category] = (1, words)
files.close()
total = 0
words = 0
for key in categories:
    total += categories[key][0]
    words += categories[key][1]
    if categories[key][0] is 0:
        avgwords = 0
    else:
        avgwords = int(categories[key][1]/categories[key][0])
    line = [str(key), str(categories[key][0]), str(avgwords)]
    print('{:>16} {:>8} {:>8}'.format(*line))
print("\nTotal: "+str(total)+"\t"+str(int(words/total)))
