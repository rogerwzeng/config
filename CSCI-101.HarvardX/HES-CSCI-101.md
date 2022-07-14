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
- NB: correlation does no equal to causation

logical expressiuon short-circuit evaluation: stop if the first expression is false in an "AND" evaluation

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

