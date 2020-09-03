# Scrapping data from Reddit for text classification
In this repository, we are trying to get some textual data from [reddit](https://www.reddit.com) to train a text classification model for predicting cybersecurity related posts in reddit. 
### Keyword List
Our system is looking for the following keywords in particular
+ 'vulnerability',
+ 'cybersecurity', 
+ 'cyber-crime', 
+ 'cybercrime', 
+ 'cyber crime', 
+ 'CVE', 
+ 'CVEs', 
+ 'CVE-', 
+ 'cyber attack'

## APIs
The system uses [PushShift](https://pushshift.io/) API for downloading historical reddit data. The API documentation can be found in [PushShift Github Repo](https://github.com/pushshift/api) 
