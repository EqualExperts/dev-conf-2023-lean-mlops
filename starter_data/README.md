## Datasets

### Summary 
| DataSet                                                                                      | # Observations | Dimensions | Description                                                               | Prediction Problem Type |
|----------------------------------------------------------------------------------------------|----------------|------------|---------------------------------------------------------------------------|-------------------------|
| [German Credit](https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)) (1994) | 1000           | 9          | Each row/record                                                           | Classification          |
| [California Housing](https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html) (1997)    | 20640          | 8          | Each row/record represents a residential area for circa ~1400 inhabitants | Regression              |
 

### 1. German Credit Data

Preview of the data.  The **_response variable_**, the value we need to predict, is italicised 

| Age | Sex | Job | Housing | Saving accounts | Checking account | Credit amount | Duration | Purpose | _Risk_ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |:-------|
| 67 | male | 2 | own | NaN | little | 1169 | 6 | radio/TV | _good_ |
| 22 | female | 2 | own | little | moderate | 5951 | 48 | radio/TV | _bad_  |
| 49 | male | 1 | own | little | NaN | 2096 | 12 | education | _good_ |
| 45 | male | 2 | free | little | little | 7882 | 42 | furniture/equipment | _good_ |
| 53 | male | 2 | free | little | little | 4870 | 24 | car | _bad_  |


**Dataset Summary**

| column\_name     | data\_type | completeness | description                          |
|:-----------------| :--- | :--- |--------------------------------------|
| Age              | BIGINT | 1.000 | age in years                         |
| Sex              | VARCHAR | 1.000 |                                      |
| Job              | BIGINT | 1.000 | enumeration of employment categories |
| Housing          | VARCHAR | 1.000 |                                      |
| Checking account | VARCHAR | 0.606 |                                      |
| Credit amount    | BIGINT | 1.000 |                                      |
| Duration         | BIGINT | 1.000 |                                      |
| Purpose          | VARCHAR | 1.000 |                                      |
| Saving accounts  | VARCHAR | 0.817 |                                      |
| Risk             | VARCHAR | 1.000 |                                      |



### 2. California House Data

**Preview** 

| MedInc | HouseAge | AveRooms | AveBedrms | Population | AveOccup | Latitude | Longitude | _median\_house\_value_ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |:-----------------------|
| 8.3252 | 41.0 | 6.984127 | 1.023810 | 322.0 | 2.555556 | 37.88 | -122.23 | _4.526_                |
| 8.3014 | 21.0 | 6.238137 | 0.971880 | 2401.0 | 2.109842 | 37.86 | -122.22 | _3.585_                |
| 7.2574 | 52.0 | 8.288136 | 1.073446 | 496.0 | 2.802260 | 37.85 | -122.24 | _3.521_                |
| 5.6431 | 52.0 | 5.817352 | 1.073059 | 558.0 | 2.547945 | 37.85 | -122.25 | _3.413_                |
| 3.8462 | 52.0 | 6.281853 | 1.081081 | 565.0 | 2.181467 | 37.85 | -122.25 | _3.422_                |

**Schema**

| attribute            | data\_type | completeness | description                                                                                                                     |
|:---------------------| :--- | :--- |:--------------------------------------------------------------------------------------------------------------------------------|
| MedInc               | DOUBLE | 1.0 | median income                                                                                                                   |
| HouseAge             | DOUBLE | 1.0 | median house age                                                                                                                |
| AveRooms             | DOUBLE | 1.0 | average number of rooms                                                                                                         |
| AveBedrms            | DOUBLE | 1.0 | average number of bedrooms                                                                                                      |
| Population           | DOUBLE | 1.0 | population for block                                                                                                            |
| AveOccup             | DOUBLE | 1.0 | average number of household members                                                                                             |
| Latitude             | DOUBLE | 1.0 | block group latitude                                                                                                            |
| Longitude            | DOUBLE | 1.0 | block group longitude                                                                                                           |
| median\_house\_value | DOUBLE | 1.0 | The target variable is the median house value for California districts, epressed in hundreds of thousands of dollars ($100,000) |


