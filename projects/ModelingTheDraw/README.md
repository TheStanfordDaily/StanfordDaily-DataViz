# Modeling The Stanford Housing Draw
Current functionality:
* Process single simple queries using last year's Housing Draw numbers (simple = True)
* Process single queries using previous years' Housing Draw numbers (simple = False)
* Clean housing data

Upcoming functionality:
* Let students assume a drawing number and see which houses they can get into
* Run Monte Carlo simulations on multiple simple queries to determine likeliest housing outcomes
## Process Single Queries (processQuery.py)
A simple query will allow a student to input a single housing draw scenario so they can see what chance they have to get certain housing given their gender, tier number, desired residence/room type, and amount of people in applicant group.
## Model Strategies
Different model strategies can be chosen by adjusting the following variables in the processSingleQuery.py function.
* simple
* linear
* logistic (coming soon)
### Simple/Naive
By setting *simple* to *True* (everything else *False*), the model takes The Draw cutoffs from 2018 as the ground truth, so it assumes 2019 will be no different.
### Linear
By setting l

Simply, this functionality will answer the following query with a probability: <br>
I am a *[gender]* applying as *[applyType]*. If I apply for a *[roomType]* in *[resName]* using tier *[tierNum]*, what are my chances of getting in?
## Clean Housing Data (cleanHousingData.py)
Take raw housing data from *[Stanford R&DE Historical Draw Numbers](https://rde.stanford.edu/studenthousing/historical-draw-statistics)* and clean and standardize the data.
