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

