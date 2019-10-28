# 1. Keyword and Stock Price Analysis

### Motivation
Our hypothesis is that there should be some correlation between keyword search frequency and stock price.
For example, there could be a breaking new about a company (which often result in large volume of keyword search for that company)
and this would likely attract investors' attention. On the other hand, there could an abrupt change in stock price of a company and 
this could make the investors to search for the company in order to investigate on the ongoing situation.
However, it is also possible that the correlation might not be significant.

Therefore, we would like to investigate on the correlation between search frequency and stock price, 
and will try to find out the correlation between them. And if correlation exists, we will try to find out how these two factors
influence each other. For example, it could be possible that the sudden changes in keyword search frequency 
trigger changes in prices or vice versa.

### Methods
#### Data
1. Stock Price
We used stock price data crawled from Naver Finance webpage.

2. Keyword Search Frequency
We used keyword search frequency data provided by Naver Datalab API.

#### Analysis
1. Find correlation between search frequency and stock price
    - Are there significant correlation?
2. Find the order of influences and propagation delay
    - Search or price first?
    - How long does it take to influence one another?
3. Find duration of influence
    - How long does the effect lasts?
4. Compare KOSPI and KOSDAQ companies
    - To find out what kind of companies are more sensitive to issues.
5. Compare different sector companies
    - To find out what kind of companies are more sensitive to issues.
    
    
### Results
TBA



### Extras
#### - Files Structure
```
[analysis]
- files for analysis

[data]
- combined (keyword+price) data files for analysis

[keyword]
- keyword data files

[prepare-data]
- files for preparing data for analysis

[price]
- price data files
```