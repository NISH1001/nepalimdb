# nepalimdb
Nepali IMDB crawler to extract Nepali movies data and analyze

## Dependencies
The crawler uses **BeautifulSoup** and **requests** modules for **python3**.  
Install using *requirements.txt* as:  
```bash
pip install -r requirements.txt
```

## Crawler Usage
Run **nepalimdb.py** script using python:  
```bash
python nepalimdb.py
```

## Data
The data is dumped as JSON in `data/nepali-movies.json`.  
The data consists of list of json object with each object holding a single movie with information like:  
- imdb_url
- title
- year
- runtime
- genre
- rating
- plot
- votes

Here's the sample json object:
```json
{
    "imdb_url": "https://www.imdb.com/title/tt6944688/?ref_=adv_li_tt",
    "title": "A Mero Hajur 2",
    "year": 2017,
    "runtime": "138 min",
    "genre": "Drama, Romance",
    "rating": 8.2,
    "plot": "A Man stalks a girl, after while they fall in love, but their relative don't want the girl to be with that man.",
    "votes": 164
},
```

You can find the data so far: [here](https://github.com/NISH1001/nepalimdb/tree/master/data)

## Data Analysis
I have done basic analysis in [this jupyter notebook](https://github.com/NISH1001/nepalimdb/blob/master/nepali-movie-analyzer.ipynb).

## Contributions
Feel free to use the data and the crawler any way you like. But, if you feel like giving me a credit, mention and this repo.  
Pull requests are welcome. Feel free to tweak the code and optimize. You might send a pull request too.  

Cheers...
