import re
import operator
from subprocess import call

files = open('article-list.txt', 'w')
call(
        ["find", ".", "-regex",
            "./\(news\|opinion\|student\-living\|features\|sci\-tech\|a\-e\|sports\|cartoons\)/[a-zA-Z0-9\-]+/index\.html"],
        stdout=files
        )
files.close()

files = open('article-list.txt', 'r')
categories = dict({"uncategorized":(0,0)})
for line in files:
    if line[len(line)-1] is '\n':
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()
    article.close()

    m = re.search('article:published.+2016.+>', content)
    if m is not None:   # article was published in 2016
        category = re.search('[a-z-]+', line).group()
        # try to establish work count
        entry = re.search('<div class="entry-content">(.|\n)+?<\/div>', content).group()
        articleList = re.split('<.+?>|&[a-zA-Z]+?;', entry)
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
