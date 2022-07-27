# Harvard Extension School - Summer 2022
## CSCI-101 Foundations of Data Science and Engineering

### Stats Refresher
#### types of data
1. Nominal Data: labels, can be grouped
2. Ordinal Data: can be ranked
3. Interval: numberical values
4. Ratio

#### central tendencies
mean, median, mode

#### stats concepts
- sample vs population standard deviation $\sigma$ (Bessell correction)
- z-score
$$Z=\frac{x-\mu}{\sigma}$$

#### Covariance
$$ sample: Cov = \frac{\Sigma(X-\overline{X})(Y-\overline{Y})}{n-1}$$
$$ population: Cov = \frac{\Sigma(X-\overline{X})(Y-\overline{Y})}{N}$$

#### Correlation coefficient Cor(X, Y)
$$\rho_{XY} = \frac{Cov(X,Y)}{\sigma_X\sigma_Y}$$
$$r=\frac{\Sigma_i(x_i-\overline{x})(y_i-\overline{y})}{\sqrt{\Sigma_i(x_i-\overline{x})^2(y_i-\overline{y})^2}}$$
- $r$ and $\rho$ are equivalent
- $r \in$ [-1,1], with |$r$|>0.5 indicates strong correlation
#### Pearson's $R^2$
$$R^2=1-\frac{\Sigma_{i=1}^N (x_i-y_i)^2}{\Sigma_{i=1}^N (x_i-\overline{x})^2}$$
- $R^2$ measures much of the data is explained by the model
- How's $r$ and $R^2$ related?
    - in univariable linear regression: $R^2 = Cor(X,Y)^2 = r^2$
    - in multivariable linear regression: $R^2 = Cor(\hat Y, Y)^2$
logical expressiuon short-circuit evaluation: stop if the first expression is false in an "AND" evaluation

### SQL 
the "group by" error trap?

#### file I/O
Infile & Outfile fields termninated by line terminated by

### Python Error Handling

```
try:
    # run these code
except [error type]:
    # what to do when error occurs
    # can have multiple "excepts" for different error types
    # OSError, ValueError, RuntimeError, CustomError etc.
else:
    # run these code when there is no exception
finally:
    # run these regardless, useful for clean up code
```

### Pandas dataframe filtering
```
df_filtered = df[(df['col_name'] == value) & (df['col_2'] == val2)]
```

Note the difference between the logical 'and' 'or' and bitwise '&' '|'

Pandas load data as String by default to convert, use sth like:

```
df['col_1'] = pd.to_numeric(df['col_1'], errors='coerce')
```

### Pandas pivot table

```
df.pivot_table(index='', columns=[], values=[], aggfunc='')
```

there is also a df.pivot() function, a subset of pivot_table()

### String functions
```
str.lower/upper/title
str.replace(' ', '')
```

### Pandas dataframe merge, dedupe, insert
```
pd.merge()
df.drop_duplicates()
df.insert(col_#, 'col_name', fill_in_value)
```

### Storytelling with Data

#### Data -> Information -> Knowledge -> Action or Decision
#### pre-attentive attributes: Color, size, orientation, texture

### Object Oriented Programming with Python

class v.s. Name Space

```
class bank_account:
pass

acct1 = bank_account   #  Name space

acct2 = bank_account()  # object class

# default constructor method
__main__   

# custom constructor method
def __init__(self, account_number, balance)  # 1st argument always 'self'
    self.aNum = account_number  # public instance variable 
    self.__aBal = balance   # private instance variable  with '__'

class_variable1
class_variable2

def class_method_1:

```

NOTE: Python does NOT reserve class instance after it's instantiated, CRAZY!

```
acct1 = bank_account()
acct1.some_faulty_variable = 1000

print(acct.some_faulty_variable)

Output: 1000
```

#### Class inheretance with super()

```
# Child class
class CD_account(bank_account):
    def __init__(self, account_number, balance, CD_maturity):
        super.__init__(self. account_number, balance)  # calls parent class init
        self.CD_maturity = mat
```
    
### T-Test
#### Independent sample t-test
```
scipy.stats.ttest_ind()
```
degree of freedom: 
$$ df = n_a + n_b -2 $$

Common variance of two samples:

#### Paired sample t-test
Q: do the two sample sets belong to the same population? 
$$ t = \frac{m}{s/\sqrt n} $$
where: 
- m: mean of difference
- n: # of samples, i.e. # of pairs
- s: standard deviation of difference
Null hypothesis: m = 0
```
scipy.stats.ttest_rel()
```

#### t-test set-up steps
1. 1-tail or 2-tail?
2. paired or unpaired?
3. equal variance? for this course, False if var_big/var_small > 2 

### ANOVA
Analysis of variability (signal to noise ratio):
1. among the sample means (signal)
2. within the distributions (noise)

Assumptiongs that must be met:
1. i.d.d.
2. normal distribution
3. homoscedasticity
```
# One-way ANOVA test
from scipy.stats import f_oneway
```

#### Post Hoc Analysis
```
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
```
mc = MultiComparison
tu = pairwise_tukeyhsd(mc)


#### Linear Regression Analysis
Two ways to do it: ols or LinearRegression

```
import statsmodels.api as sm
from statsmodels.formula.api import ols

result = ols("y ~ X", data=df).fit()
```

```
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
model = LinearRegression()
model.fit(x_tran, y_train)  # train the model

y_pred = model.predict(x_test)  # validate model w/ test data set

model.score(x_test, y_test)
```

#### Confounding variables

Variance Inflation Factor(VIF)
$$ VIF = \frac{1}{1-R^2}$$

```
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

df = add_constant(df)
vif = variance_inflation_factor(df.values, i)

# if vif > 5, then there is a collinearity problem
```

