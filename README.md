<img src="https://github.com/mihirs16/Project-Darwin/blob/master/static/Assets/Logo-w%20Name.svg" width=250>

---
The project aims to develop a prototype of a platform which can help streamline and scale up the
hiring process by automating the steps of recruitment that involve accepting applications,
gathering data and insights into the candidate pool, comparing candidates, ranking and
shortlisting all applicants. Such a platform could prove to be useful in carrying out large scale
recruitment campaigns by narrowing down the candidate pool for any specific job posting.<br>
<br>
Project Demo Video: [Introducing - Project Darwin | By Team Blueprint](https://youtu.be/dAfU6YDgf8w)

## Built With
| Software | Version |
|----------|---------|
| Adobe XD | 24.0.22 |
| Zeplin   | 4.0.2 |
| Python 3 | 3.7.1 |
| Twitter API | 7.0 |
| IBM Watson | 2.0 |
| IBM Watson's Personality Insights | Service Update 12-12-2019 |
| IBM DB2 | 11.5 |
| IBM Cloud Object Storage | 2.0 |

## Pre-requisites
* Windows

| Name | Lowest Version Tested With |
|----------|----------------------------|
| Google Chrome | 83.0.4103.116 |
| Microsoft Chromium Edge | 84.0.522.35 |

* MacOS

| Name | Lowest Version Tested With |
|----------|----------------------------|
| Safari | 13.1.1 |
| Google Chrome | 83.0.4103 |

* Development Libraries

| Name | Last Version Tested With |
|----------|--------------------------|
| Python | 3.7.1 |
| Pandas | 0.25.1 |
| Flask | 1.1.1 |
| Flask-CORS | 3.0.8 |
| IBM-COS-SDK | 2.6.3 |
| IBM-DB | 3.0.2 |
| IBM-Watson | 4.5.0 |
| Python-Dotenv | 0.13.0 |
| Tweepy | 3.8.0 |

## Instructions

* Clone the repository.
```
git clone https://github.com/mihirs16/Project-Darwin
```
* Now install all required libraries through requirements.txt
```
pip install requirements.txt
```
* Now create a file with the name `.env`. Add all API Keys inside this file as text. Click [here](https://pypi.org/project/python-dotenv/) to know more about hidden API Keys as Environment Variables.
```
EXAMPLE_API_KEY=examplekeyvalue123
```
* You can find all required keys in the `k3y5.py`, as imported environment variables.
* Now run the Flask app `app.py`
```
python app.py
```
* In your browser open http://localhost:5000 (or `:{port-number}` as specified by the Flask's development server)

## Disclaimer
Aforementioned Project Darwin is still an experimental prototype. However instances fit for specific use cases can be spawned and developed for your use. In order to contact us for such an endeavor please check out the contributors for this project. 
