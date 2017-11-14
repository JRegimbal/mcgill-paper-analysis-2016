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

## Totals and Breakdown by Category

### The Daily

| Category | Articles | Percentage |
| --- | --- | --- |
| News | 174 | |
| Culture | 91 | |
| Commentary | 122 | |
| Compendium | 22 | |
| Sci-Tech | 39 | |
| Sports | 1 | |
| Features | 22 | |
| Editorials | 3 | |
| Uncategorized | 52 | |
| --- | --- | --- |
| Total | 526 | 100% |

### Le Délit

| Category | Articles | Percentage |
| --- | --- | --- |
| Actualités | 154 | |
| Culture | 131 | |
| Société | 64 | |
| Innovations | 31 | |
| Éditorial | 19 | |
| Chroniques | 17 | |
| Entrevues | 14 | |
| --- | --- | --- |
| Total | 430 | 100% |


