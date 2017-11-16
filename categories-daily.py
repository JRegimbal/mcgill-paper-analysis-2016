import re
import operator
from subprocess import call

# open file to store paths of articles
files = open('article-list.txt', 'w')
# system call to generate the list
ret = call(
        ["find", ".", "-regex", "./2016/[0-9][0-9]/[0-9a-zA-Z\-]+/index\.html"],
        stdout=files
        )
files.close()

files = open('article-list.txt', 'r')
categories = dict({"uncategorized":(0,0)})
for line in files:      # process file by file
    if line[len(line)-1] == '\n':   # remove trailing newline character
        line = line[:-1]
    article = open(line, 'r')
    content = article.read()        # copy raw HTML/javscript/CSS from article
    article.close()
    # look for the header section that usually contains category info
    # not all articles have this
    m = re.search('<h1><a.+?>(<span.+?>)?.+?(<\/span.+?>)?<\/a>', content)
    if m is None:
        category = "uncategorized"
    else:
        #filter out most of HTML so the category has a set buffer on each end
        category = re.search('">[a-zA-Z]+?<\/', m.group())
        if category is None:
            category = "uncategorized"
        else:
            category = category.group()[2:-2] # remove the buffers
    #try to determine word count
    if category is not "uncategorized": # uncategorized is excluded
        entry = re.search('<section class="tmd-post-content">(.|\n)+?<\/section>', content).group()
        # try to remove HTML, non-text special characters
        articleList = re.split('<.+?>|&[#a-zA-Z0-9]+?;', entry)
        text = str()
        for s in articleList:
            if s is not '':     # don't bother adding empty strings
                text += s
        words = 0
        for s in re.split(' |\n', text): # split into words by space or newline
            if s is not '':
                words += 1
    else:
        words = 0
    if category in categories:  # add to overall category data
        categories[category] = tuple(map(
            operator.add, categories[category], (1, words)))
    else:
        categories[category] = (1, words)   # new category added
files.close()

total = 0
words = 0
for category in categories:
    total += categories[category][0]
    words += categories[category][1]
    if categories[category][0] is 0:    # avoid division by zero error
        avgwords = 0
    else:
        avgwords = int(categories[category][1]/categories[category][0])
    line = [str(category), str(categories[category][0]), str(avgwords)]
    print('{:>16} {:>8} {:>8}'.format(*line))   # keeps the output pretty
print("\nTotal: "+str(total)+"\t"+str(int(words/(total-categories["uncategorized"][0]))))
