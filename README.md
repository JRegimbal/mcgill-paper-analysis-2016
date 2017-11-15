# McGill Independent Student Newspaper Analysis for 2016

Note that this is still a work in progress. If any errors have been made, please notify me either by creating an issue or using the email address listed on my profile.

## Papers Examined

The Daily, Le Délit, and the Tribune were all analyzed. Only text-based articles posted online were subject to review. Other articles, including specials, were not examined. Articles were collected en masse and filtered based on year of publication and category. Articles were collected using GNU wget 1.19.2 as follows.

### The Daily

The Daily publishes articles online organized by year and month of publication. Articles were downloaded using `wget -r -np www.mcgilldaily.com/2016/ --accept=html,htm`. Only HTML files were accepted to avoid downloading media files.

### Le Délit

Le Délit uses a similar organization as the Daily. Articles are organized by year, month, and day of publication. However there is no simple way to list out all of the articles published in 2016 as there is with the Daily. Attempting to use the same command and substituting the URL misses most of the articles. Instead the entire plaintext website needed to be downloaded using `wget -r www.delitfrancais.com/ --accept=html,htm`. This downloaded the 2016 subfolder which was used as the source for analysis.

### The Tribune

The Tribune does provide a list of pages published by year, however articles are organized by category and title making the method used with the Daily unusable. Like le Délit, the entire plaintext site needed to be downloaded using `wget -r www.mcgilltribune.com/ --accept=html,htm`.

## Article Count and Categorization

### The Daily

The list of articles published in 2016 was generated using GNU find 4.7.0 and a regex run in the root directory for the website. Categories were found by using another regex to search for the `<h1>` tag and filter out text to find the category the article was published under. Some articles do not have a category defined in this way for some reason, and are listed as uncategorized. Some may truly lack a category, but others may be formatted in a way that fails with this automation.

The regex for the file list was `find . -regex './2016/[0-9][0-9]/[0-9a-zA-Z\-]+/index\.html'`.

The regex for the categorization was done in two parts and using Python's `re` module. The first, `<h1><a.+?>(<span.+?>)?.+?(<\/span.+?>)?<\/a>`, broadly finds the first link in the header which typically is to the general category. The second, `">[a-zA-Z]+?<\/`, yields a string with known buffers around the actual title. The first and last two characters are removed here to yield the category name.

[Python Script for the Daily](categories-daily.py)

### Le Délit

The list of files was generated similarly to the method used with the Daily. The regex used for the file list was `find . -regex './2016/[0-9][0-9]/[0-9][0-9]/[a-zA-Z-]+/index\.html'`.

The category system is also similar to that used by the Daily. Within the `<div class="sections intro subtitle">` tag are links to the main category and subcategories of the article. Subcategories were ignored here for simplicity. Again, a two part method was used using Python's `re` module. The first broadly selects the contents of this `<div>` tag using `<div class="sections intro subtitle">(.|\n)*?<a.+?>.+<\/a>(.|\n)*?<\/div>`. The second refines it down so that the category title has a buffer of one character before and 4 characters behind. This one is `>.+?<\/a>`.

[Python Script for le Délit](categories-delit.py)

### The Tribune

The list of articles was formed by first making a list of all articles in each category and then filtering by publication date. Category was extracted from the paths of articles published in 2016.

The subfolders examined, which correspond to categories, were news, opinion, student-living, features, sci-tech, sports, student living, cartoons, and arts and entertainment (a-e). 
The list was generated using `find . -regex './\(news\|opinion\|student\-living\|features\|sci\-tech\|a\-e\|sports\|cartoons\)/[a-zA-Z0-9\-]+/index\.html'`.

Article tags were used to determine if a certain article was published in 2016. Specifically the regex was `article:published.+2016.+>`. For articles meeting this, the category was determined by passing the following regex on its path: `[a-z-]+`.

[Python Script for the Tribune](categories-tribune.py)

## Totals and Breakdown by Category

### The Daily

| Category | Articles | Percentage | Average Length (words) |
| --- | --- | --- | --- |
| News | 174 | 33.08% | 922 |
| Culture | 91 | 17.30% | 958 |
| Commentary | 122 | 23.19% | 977 |
| Compendium | 22 | 4.18% | 505 |
| Sci-Tech | 39 | 7.41% | 1039 |
| Sports | 1 | 0.19% | 953 |
| Features | 22 | 4.18% | 2984 |
| Editorials | 3 | 0.57% | 492 |
| Uncategorized | 52 | 9.89% | N/A |
| Total | 526 | 100% | 1002 |

### Le Délit

| Category | Articles | Percentage | Average Length (words) |
| --- | --- | --- | --- |
| Actualités | 154 | 35.81% | 649 |
| Culture | 131 | 30.47% | 630 |
| Société | 64 | 14.9% | 833 |
| Innovations | 31 | 7.21% | 672 |
| Éditorial | 19 | 4.42% | 617 |
| Chroniques | 17 | 3.95% | 455 |
| Entrevues | 14 | 3.26% | 1141 |
| Total | 430 | 100% | 679 |

### The Tribune

| Category | Articles | Percentage | Average Length (words) |
| --- | --- | --- | --- |
| News | 145 | 18.61% | 714 |
| Opinion | 140 | 17.97% | 436 |
| Sports | 140 | 17.97% | 569 |
| Sci-Tech | 92 | 11.81% | 651 |
| Student Living | 103 | 13.22% | 592 |
| Arts and Entertainment | 159 | 20.41% | 659 |
| Total | 779 | 100% | 603 |

### Note About Word Counts

Word counts were determined by trying to identify the part of the HTML contained the article entry, filtering out HTML tags, special characters, etc. and then finding breaking up the resulting string by whitespace characters. Because of this, contractions like "it'll" or "l'article" are counted as one word and not two. This is probably has the most impact on le Délit.

Uncategorized articles often couldn't have their word counts checked using the same method as categorized articles. These were simply omitted from the count, and the total average length was calculated using the number of *categorized* articles. The assumption is made that uncategorized articles have roughly the same length as uncategorized.

## Notes

The regular expression syntax differs between GNU's find and Python's `re` module. `re` largely follows Perl regex syntax, while find uses emacs regex syntax. This is the reason for differences in escape characters.

This project isn't meant to be definitive in any way, but give a general idea of what each of the newspapers produces. It is not intended for anything more.

This is written in English so it can reach the entire McGill community. Ideally a French translation will be made once the content is mostly finalized.
