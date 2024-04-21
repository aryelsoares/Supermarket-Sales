# Supermarket-Sales
 Analysis of supermarket branch sales from a database. The objective is to pass all the data from the source to a MySQL database and perform general analysis of the data.

#### Source
https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales

The dataset is one of the historical sales of supermarket company which has recorded in 3 different branches for 3 months data.

#### Attribute information
Invoice id: Computer generated sales slip invoice identification number.

Branch: Branch of supercenter (3 branches are available identified by A, B and C).

City: Location of supercenters.

Customer type: Type of customers, recorded by Members for customers using member card and Normal for without member card.

Gender: Gender type of customer.

Product line: General item categorization groups - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle, Sports and travel.

Unit price: Price of each product in $.

Quantity: Number of products purchased by customer.

Tax: 5% tax fee for customer buying.

Total: Total price including tax.

Date: Date of purchase (Record available from January 2019 to March 2019).

Time: Purchase time (10am to 9pm).

Payment: Payment used by customer for purchase (3 methods are available - Cash, Credit card and Ewallet).

COGS: Cost of goods sold.

Gross margin percentage: Gross margin percentage.

Gross income: Gross income.

Rating: Customer stratification rating on their overall shopping experience (On a scale of 1 to 10).

### Data modeling
To pass data from the csv file to a MySQL database, it's important to properly model the data. Data modeling is done up to fifth normal form (5NF). By using MySQL workbench the following schema was assigned and made a python script to automate data insertion.

![schema](https://github.com/aryelsoares/Bitcoin-Prediction/assets/165218194/4647f700-a5e2-465c-981f-b1e58b7008aa)

Branch and City are directly correlated, so just use the second one, which is less generic.

Customer Type and Gender are both related to customer that doesn't present data.

Tax and Total are redundant information for the database.

Date and Time are merged into datetime.

COGS and Gross Margin Percentage are directly correlated to Gross Income.

### Analysis
The data is taken from the MySQL database called 'supermarket' and analyzed in general. In addition, total price is grouped by rating (k-means clustering) and also checked the trend of gross income per branch using time series and linear regression.

### Note
This project is for educational proposals.