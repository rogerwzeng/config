## Harvard CSCI E-116 Dynamic Modeling and Prediction in Big Data
### Prof. William Yu
### Fall/Winter 2022

### Linear Regression Model 
__Interaction terms are often effective in modeling (increase $R^2$) between related variables__
```
library(olsrr) 
ols_step_all_possible(lm(y~ (x_1 + x_2 + ...)^2))
```
"^2" is for interaction terms to the second order (2 variable combos)

### Three Predictive Models
#### Strucutural/Static Model

$$ Y_t = F_t(x_1, x_2, ..., x_n) $$

__problem:__ need to model all independent variables in current period, high model complexity

#### Reduced form model (a.k.a. time series model in lay man terms)

$$ Y_t = F(Y_{t-1}, Y_{t-2}, ..., Y_{t-n})$$
$$Y_{t+1} = F(Y_t, Y_{t-1}, ..., Y_{t-n+1})$$

__advantage:__ only deal with one variable and its history
__problem:__ do not know why , can't predict turning points

#### Mixed Model

$$ Y_t = F(Y_{t-1}, x^1_t, x^2_t, ..., x^m_t) $$
$$ Y_{t+1} = F(Y_t, x^1_{t+1}, x^2_{t+1}, ..., x^m_{t+1}) $$

__advantage:__ reduced model complexity with some degrees of explanatary power

__Be ware of spurious (coincidental) correlation between time series data sets with similar trends__


### Useful libraries

__US Census__ 
```
library(tidycensus)
```
__API key:__ 46fa81f52b62758f6d0e7067d9c0aa7ef151553c

__Fed St. Louis US Economic Data__
```
library(quantmod)
getSymbols(symbol, src=source)
```

__Time Series__
```
library(tseries)
```

__olsrr__:  R OLS Regression library
```
# a grid search of all variable combo to the 2nd degree
gs_result <- set_all_possible(y ~ (x1 + x2 + x3)^2)
gs_result[which.max(gs_result$adjr),]

```

### T.A. (Hannah Grace Smith: hgmsmith@ucla.edu)

__Making predictions:__ Use as.matrix() to turn coef(model) into __n x 1__ matrix then use __%*%__ for matrix multiplication
```
pred = c(1, val1, val2, ...) %*% as.matrix(coef(model))
```
__Test Accuracy and Confusion Matrix__

## Assignment #02
#### quantile() in base
#### paste() in base: str+(sep)+str
#### cut() in base, convert numeric to categorical with breaks and labels

### log model: linear trend means constant growth rate

## Modeling Long term trends

### 1. Linear Trend
$$ Y_t = \beta_0 + \beta_1*Trend_t$$

### 2. Quadratic trend
$$ Y_t = \beta_0 + \beta_1*Trend_t + \beta_2*Trend_t^2 $$

### 3. Log Linear trend
$$ ln(Y_t) = \beta_0 + \beta_1*Trend_t$$

### 4. Exponential Smoothing (Holt's linear trend)
- Really it is weighted moving average to predict future
- Simple moving average: $L_t = \frac{1}{3}*Y_t + \frac{1}{3}*Y_{t-1} + \frac{1}{3}*Y_{t-2}$
- Exponential smoothing: $L_t^2 = \alpha*Y_t^2 + (1-\alpha)*L_{t-1}^2$ 
- with backsubstitution $\Longrightarrow$ $L_t^2 = \Sigma_{j=0}^t \alpha*(1-\alpha)^j*Y_{t-j}^2$

### Seasonal Model
useful funtions:
ts(), ggseasonplot(), ggsubseriesplot()
#### basic time serial analysis functions in R
- differencing: diff()
- frequency resampling: apply.xxx() (monthly, quarterly, yearly)
- simple decomposition: decompose()
- simulation: arima.sim
- other useful functions: seq_along(), tslm(), autoplot()
- coef test: coeftest()
- ACF functions: ggAcf(), acf()
- par() function to control layout
- checkresiduals()

### Are the model error residuals i.i.d.? 
Use Ljung-box test 
$$Q=n(n+2)\Sigma_{k=1}^h \frac{P_k^2}{n-k}$$
- n:sample size
- $P_k$:sample autocorrelation at lag k
- h: number of lag being tested
```
Box.test() in R
```
If not, there is likely ommitted variables. Solution:
- increase lag
- instrumental variables
- detect Heteroscedasdicity

### ARMA model
- a type of reduced form  model
- AR: use past series data to predict future data value
- MA: use past forecast error to predict future, also called "shock" (deviation from prediction)
- ARMA(p,q): AR with lag p + MA with lag q
- ARIMA: AR+MA+I(integration)

### How to find ARIMA model paramters
#### Dickey-Fuller test
```
library(tseries)
adf.test(data)
```
##### auto ARIMA to find the best p, q values
- auto.arima()
- accuracy()

#### stationarity $\rightarrow$ predicatable time series
Way to improve stationarity of data:
1. log transmformation of data (Box-Cox transformation)
2. Detrend data for deterministic trend
3. Take first difference for stochastic data: $(Y_t - Y_{t-1})$ i.e. I(1)
4. Growth rate: ln($Y_t$)-ln($Y_{t-1}$)
5. NB: signal/noise ratio: time sampling intervals affects model quality greatly, short term data have more noise

e.g. ARIMA(3,1,2)
- AR(3): $\beta_1Y_{t-1}+\beta_2Y_{t-2}+\beta_3Y_{t-3}$
- I(1): $\beta_4(Y_t-Y_{t-1})$
- MA(2): $\beta_5\epsilon_t+\beta_6\epsilon_{t-1}$
- ARIMA models are good at capturing momentum for short term forecast, not seasonality and turning points
- exogenous variables are better for turning points
- Mixed model:
$$Y_t = \alpha + \beta_1 Y_{t-1} + \beta_2 X_t + \beta_3 X_{t-1} + \epsilon_t , \epsilon_t \sim N(0, \sigma^2)$$

#### Types of the ARIMA models
- Pure Ramdom Walk: ARIMA(0,1,0)
- Radom Walk: ARIMA(p,0,q)
- Random Walk with Drift: ARIMA(0,1,0) + drift

### Wold Decomposition
- Generalized form of ARMA and ARIMA model
$$y_t = B (L) \epsilon_t = \Sigma_{i=0}^\infty b_i \epsilon_{t-1}$$
where $\epsilon_t \sim N(0, \sigma^2)$ and $\Epsilon(y_t) = \Sigma_{i=0}^\infty b_i \Epsilon(\epsilon_{t-1}) = 0$
- AR can be decomposed into MA with $\infty$ series, both are approximation of Wold Decomposition

### Dynamic Linear Model
- where coefficients are not static, but evolves with time
- DLM in state space model written in MARSS (multivariate autoregressive state space) form
$$ y_t = \mathbf{F}^{\top}_t \boldsymbol{\theta}_t + e_t \\
\boldsymbol{\theta}_t = \mathbf{G} \boldsymbol{\theta}_{t-1} + \mathbf{w}_t \\
\Downarrow \\
y_t = \mathbf{Z}_t \mathbf{x}_t + v_t (observation)\\
\mathbf{x}_t = \mathbf{B} \mathbf{x}_{t-1} + \mathbf{w}_t (process)$$
```
dynlm() in dynlm, MARSS() in MARSS library in R
dlm() in pyDLM , DynLin() in pyFlux package in Python
```
- Mixed model: time series reduced form model + structured model
- exogenous variables can have different model structures


