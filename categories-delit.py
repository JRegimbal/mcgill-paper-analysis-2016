import re
import operator
from subprocess import call

# open file to store paths of articles
files = open('article-list.txt', 'w')
# system call to generate the list
call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9][0-9]/[a-zA-Z-]+/index\.html"],
        stdout=files
        )
files.close()
categories = dict({"uncategorized":(0,0)})
files = open('article-list.txt', 'r')

for line in files:  # each line is path to article
    if line[len(line)-1] == '\n':   # remove trailing newline character (if any)
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()        # get raw content
    article.close()
    # search for section that contains category info
    m = re.search('<div class="sections intro subtitle">(.|\n)*?<a.+?>.+<\/a>(.|\n)*?<\/div>', content)
    if m is None:
        categories["uncategorized"] += 1
    else:
        # refine to category and trim unneeded characters
        category = re.search('>.+?<\/a>', m.group()).group()[1:-4]
    # try to establish word count
    entry = re.search('<div class="[a-z ]+?text"(.|\n)+?<div class="spacer">', content).group()
    # remove HTML and non-text characters
    articleList = re.split('<.+?>|&.+?;|\\xa0', entry)
    text = str()
    for s in articleList:
        if s is not '':
            text += s
    words = 0
    for s in re.split(' |\n', text):    # split into words and count
        if s is not '':
            words += 1
    # record category data
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
    if categories[key][0] is 0: # avoid division by 0 error
        avgwords = 0
    else:
        avgwords = int(categories[key][1]/categories[key][0])
    line = [str(key), str(categories[key][0]), str(avgwords)]
    print('{:>16} {:>8} {:>8}'.format(*line))
print("\nTotal: "+str(total)+"\t"+str(int(words/total)))
