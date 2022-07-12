# Simple crawler
> This helps to grasp and analyze information from search engine.


## Installation

```sh
git clone https://github.com/TANSixu/SimpleCrawler.git
conda create -n [&choose_your_own_name&] python=2.7
pip install -r requirements.txt
conda activate [&choose_your_own_name&]
```

## Usage example
1. Go into source code simplecrawler.py, set $kw$ at line 20 to the search keyword. (use this ugly way to support kanji search across all platform)
2. Run the following command:
```sh
python simple_crawler.py
```
3. Optional arguments:

  -h, --help            show this help message and exit
  
  -n NUM, --num NUM     number of pages to craw
  
  -d DIR_NAME, --dir_name DIR_NAME
                        directory name to save the crawled files
                      


