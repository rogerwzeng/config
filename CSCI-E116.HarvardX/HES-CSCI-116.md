### Harvard CSCI E-116 Dynamic Modeling and Prediction in Big Data
#### Prof. William Yu
#### Fall/Winter 2022

[toc]
### Linear Regression Model 
__Interaction terms are often effective in modeling (increase $R^2$) between related variables__
```
lm()
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


### Useful libraries and functions

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

T.A. (Hannah Grace Smith: hgmsmith@ucla.edu)

__Making predictions:__ Use as.matrix() to turn coef(model) into __n x 1__ matrix then use __%*%__ for matrix multiplication
```
pred = c(1, val1, val2, ...) %*% as.matrix(coef(model))
```
__Test Accuracy and Confusion Matrix__

```
quantile() in base
paste() in base: str+(sep)+str
cut() in base, convert numeric to categorical with breaks and labels
```

__INSIGHT__: linear trend in log model means constant growth rate

### Modeling Long term trends
Key components in time series modeling:
- Level
- Trend
- Seasonality
- Noise

#### 1. Linear Trend
$$Y_t = \beta_0 + \beta_1 Trend_t$$

#### 2. Quadratic trend
$$Y_t = \beta_0 + \beta_1 Trend_t + \beta_2 Trend_t^2$$

#### 3. Log Linear trend
$$ ln(Y_t) = \beta_0 + \beta_1 Trend_t$$

#### 4. Exponential Smoothing (simple exponential smoothing)
- __INSIGHT:__ Really it is using weighted moving average to predict future
- $\alpha$ is the hyperparameter for level data 
- Simple moving average: 
$$L_t = \frac{1}{3}Y_t + \frac{1}{3}Y_{t-1} + \frac{1}{3}Y_{t-2}$$
- Simple exponential smoothing: 
$$L_t^2 = \alpha Y_t^2 + (1-\alpha)L_{t-1}^2$$ 
- with backsubstitution:
$$\Rightarrow L_t^2 = \Sigma_{j=0}^t \,\, \alpha(1-\alpha)^jY_{t-j}^2$$
#### 5. Trend model Holt's model
- Adds hyperparameter $\beta$ to model trend in the data
- Additive model: linear trend 
- Multiplicative model: exponential trend 
#### 6. Seasonal Model (Holt-Winters model)
- Adds hyperparameter $\gamma$ to add control for seasonality to Holt's model
#### 7. Trend damping
- No trend last forever! Need to damp trend over time for better forecasting
- Adds hyperparameter $\varphi$ (additive or multiplicative) to damp trend

#### Useful funtions:
ts(), ggseasonplot(), ggsubseriesplot()
#### Basic time serial analysis functions in R
- differencing: diff()
- frequency resampling: apply.xxx() (monthly, quarterly, yearly)
- simple decomposition: decompose()
- simulation: arima.sim
- other useful functions: seq_along(), tslm(), autoplot()
- coef test: coeftest()
- ACF functions: ggAcf(), acf()
- par() function to control layout
- checkresiduals()

#### Ljung-box test 
$$Q=n(n+2)\Sigma_{k=1}^h \frac{P_k^2}{n-k}$$
- n:sample size
- $P_k$:sample autocorrelation at lag k
- h: number of lag being tested
```
Box.test() in R
```
#### Augmented Dickey-Fuller (ADF) test
```
adf.test() in R
```
If not, there is likely ommitted variables. Solution:
- increase lag
- instrumental variables
- detect Heteroscedasdicity

### ARMA model
- a type of reduced form  model
- AR: use past series data to predict future data value
- MA: use past forecast error to predict future
- ARMA(p,q): AR with lag p + MA with lag q
- ARIMA: AR+MA+I(integration)
#### INSIGHT: Forecast errors $\epsilon_t$ are shocks to the system (deviation from prediction)

### How to find ARIMA model paramters
#### Dickey-Fuller test
```
library(tseries)
adf.test(data)
```
#### auto ARIMA to find the best p, q values
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
- assumes $x$ impacts $y$ but NOT the other way around

### VAR
- More general other dynamic linear model, assume $x$ and $y$ impact each other.
- Simple two variable VAR
$$
\begin{bmatrix}
y_{1,t}\\
y_{2,t}
\end{bmatrix}
=
\begin{bmatrix}
\phi_{11}&\phi_{12}\\
\phi_{21}&\phi_{22}\\
\end{bmatrix}
\cdot
\begin{bmatrix}
x_{1,t}\\
x_{2,t}\\
\end{bmatrix}
+
\begin{bmatrix}
\epsilon_{1,t}\\
\epsilon_{2,t}\\
\end{bmatrix}
$$
- Shocks affects $\epsilon_{1,t}$ and $\epsilon_{2,t}$ and are (somehow) also called "innovation"!
- Also, $\epsilon_{1,t}$ and $\epsilon_{2,t}$ can be correlated so the innovations on one affects the other
- $\epsilon_{1,t} \sim WN(0, \sigma_1^2)$ , $\epsilon_{2,t} \sim WN(0, \sigma_2^2)$ and $cov(\epsilon_{1,t}, \epsilon_{2,t}) = \sigma_{12}=\sigma_{21}$ 
- Solve for the NxN $\phi$ linear equation (easy!)
```
VARselect()
VAR()
```
#### Granger Causality Test 
But $y_2$ may not really cause $y_1$ even if $\phi_{12}>0$
```
grangertest()
```
$H_0$: $x$ does not Granger cause (affect) $y$ <br>
$H_1$: $x$ does Granger cause (affect) $y$

#### Impact Response Functions (IRF)
- response to system shock over time
```
irf()
```
Protocol: 
- Use Granger test to determine the causality arrow of the $y$s
- Set up the VAR model and compute $\phi$ coefficient matrix
- Use IRF on non-stationary $\epsilon$s to analyze impact of one-time events (e.g. Covid, Ukraine War)

### Dynamic Factor Model
#### How to handle big data? Some common approaches:
- Remove highly correlated variables (>0.95)
- Variance Inflation Factor (VIF)
- Shrinkage/Regularization e.g. lasso, ridge regression
- Model selection e.g. Regsubset in R, stepwise selection
- Principle Component Analysis (trim # of variables)

#### DFM = VAR + PCA
$$ y_t = \Lambda \mathbf{F}_t + e_t $$
$$ \mathbf{F}_t = \Phi \mathbf{F}_{t-1} + \epsilon_t $$
for $lag=1$, where:
- $\mathbf{F}_t$ is the principle component vector at time $t$
- $\Lambda$ is the loading factor matrix
- $\Phi$ is the VAR coefficient matrix

#### INSIGHT: PCA is a type of unsupervised learning
- Clustering methods in ML group observations (rows)
- PCA is clustering/grouping of variables (columns)!
- DFM steps:
    * Use PCA to find $m$ best composite variables
    * Use Multiple Linear Regression to get $m+1$ coefficients and intercept vector
    * Use VAR to predict loading factor ahead by $n$ steps
    * Multiply $n$X$(m+1)$ matrix with $m+1$ vector to get $n$X$1$ vector of predicted values
- BUT, Why can't add add dependent variable to VAR to get prediction using VAR?
In the case of Assignment 7, the results of these two approaches were very close.

#### PCA math
$$ \mathbf{A}\cdot F = \lambda F $$
where:
- Loading factor / orientation: $\mathbf{A}$ is the proportion of variables in each principle component
- Eigenvectors $F$ are orthogonal to each other 
- Eigenvalues: $\lambda$ squared sum of distances of all observations to the origin
- __SVD (singular value decomposition)__ singular value = $\sqrt\lambda$
- scree plot: distribution of principle components weights in explaining data variation (add up to 100%)

Try to tell a story with each principle component chosen (look for high abs(coefficients) in PC matrix)

#### Advantage of DFM:
- Over PCA: capture lag causality in time series
- Over VAR: using composite variables for better accuracy
- Over ARIMA: more explainable
### State Space Model
$\alpha$ and $\beta$ are $\alpha_t$ and $\beta_t$, i.e. time varying
#### Structural Time Series
- Limited # of changes of $\alpha$ and $\beta$
- Null hypothesis: coefficients do not vary with time
    * Use __F Test__ to determine 

__INSIGHT:__ intercept of linear model also called __unconditional mean__
```
StructTS()  # structural time series
- level
- trend
- BSM (Baysian Sessonal Model: trend + seasonal)

breakpoints()
```

### Multivariate Gaussian

| Type | Univariate| Multivariate|
|:--|:----|----|
|Mean| $\mu$ | $[\mu_1, \mu_2, \cdots , \mu_n]^\mathsf T$|
|Covariance| $\sigma^2$|$\Sigma = \begin{bmatrix} \sigma_1^2 & \sigma_{12} & \cdots & \sigma_{1n} \\ \sigma_{21} &\sigma_2^2 & \cdots & \sigma_{2n} \\ \vdots  & \vdots  & \ddots & \vdots  \\ \sigma_{n1} & \sigma_{n2} & \cdots & \sigma_n^2 \end{bmatrix}$|
|PDF| $f(x, \mu, \sigma) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp \Big [{-\frac{1}{2}}{(x-\mu)^2}/\sigma^2 \Big ]$ | $f(\mathbf{x},\, \mu,\,\Sigma) = \frac{1}{\sqrt{(2\pi)^n\|\Sigma\|}}\, \exp  \Big [{ -\frac{1}{2}(\mathbf{x}-\mu)^\mathsf{T}\Sigma^{-1}(\mathbf{x}-\mu) \Big ]}$ 
| Multiplication | $\begin{aligned} \mu &=\frac{\sigma_1^2 \mu_2 + \sigma_2^2 \mu_1} {\sigma_1^2 + \sigma_2^2} \\ \sigma^2 &= \frac{\sigma_1^2\sigma_2^2}{\sigma_1^2+\sigma_2^2} \end{aligned}$ | $\begin{aligned} \mu &= \Sigma^{(2)}(\Sigma^{(s)})^{-1}\mu^{(1)} + \Sigma^{(1)}(\Sigma^{(s)})^{-1}\mu^{(2)} \\ \Sigma &= \Sigma^{(1)}(\Sigma^{(s)})^{-1}\Sigma^{(2)} \\ \Sigma^{(s)} &=\Sigma^{(1)}+\Sigma^{(2)} \end{aligned}$|



- Multiplying Gaussians increase mean and reduces variance (more certainty)
- The more correlated the two Guassians, the smaller the covariance of their product

### Kalman Filter
__Kalman filter is the generalized version of Structural Time Series, and the most optimal solution for state space model.__

__state variable__ $x_t \in \mathbb{R^n}$ ;
__measurement variable__ $y_t \in \mathbb{R^m}$

__State Transition Equation__
$$x_t = \mathbf{A}x_{t-1} + \mathbf{B} u_{t-1}+ \epsilon_t$$ 

__Measurement Equation__
$$ z_t = \mathbf{H} x_t + \nu_t$$
with process noise $\epsilon_t \sim \mathbf{N}(0, \mathbf{Q})$ and measurement noise $\nu_t \sim \mathbf{N}(0, \mathbf{R})$

_a prior_ state estimate: $\hat x^-_t =\mathbf{A}x_{t-1} + \mathbf{B} u_{t-1}$ <br>
_a prior_ predicted measurement: $\hat z_t = \mathbf{H}x^-_t$<br>
_a posteriori_ state estimate: $\hat x_t = \mathbf{E}[x_t] = \hat x^-_t + \mathbf{K}(z_t - \hat y_t) = \mathbf{A}x_{t-1} + \mathbf{B} u_{t-1} + \mathbf{K}(z_t - \mathbf{H} \hat x^-_t)$<br>
$y_t = z_t - \mathbf{H}\hat x^-_t$ is the descrepancy between prediction and measurement and often called _innovation_ or _residual_.

_a prior_ estimate error and its covariance matrix: $e^-_t = (x_t - \hat x^-_t)$ and $\mathbf{P}^-_t = \mathbb{E}[e^-_t e_t^{-\mathsf T}]$<br>
_a posteriori_ estimate error and its covariance matrix: $e_t = (x_t - \hat x_t)$ and $\mathbf{P}_t = \mathbb{E}[e_t e_t^\mathsf T]$<br>

The __Kalman Gain__ $\mathbf{K}$ is the value $argmin_\mathbf{K} \mathbf{P}_t$, i.e. one that minimizes posteriori estimate covariance:
$$\mathbf{K_t} = \mathbf{P^-_t}\mathbf{H^T}(\mathbf{H}\mathbf{P^-_t}\mathbf{H^T} + \mathbf{R})^{-1}$$

__INSIGHT:__ Good estimate is a __blend__ of measurement and prediction!

__INSIGHT:__ State is the __true value__ of what we are trying to estimate through measurements.

__INSIGHT:__ Measurment variance affect final precision much more than process variance!


#### The Kalman Filter algorithm
<u>**Initiation**</u><br>
estimates of initial states $\hat x_0$ and covariance $\mathbf{P}_0$<br>
<u>**Predict**</u>

$\begin{array}{|l|l|l|}
\hline
\text{Univariate} & \text{Univariate} & \text{Multivariate}\\
& \text{(Kalman form)} & \\
\hline
\hat \mu = \mu + \mu_{f_x} & \hat x = x + dx & \hat {\mathbf x} = \mathbf{Ax} + \mathbf{Bu}\\
\hat\sigma^2 = \sigma_x^2 + \sigma_{f_x}^2 & \hat P = P + Q & \hat{\mathbf P} = \mathbf{APA}^\mathsf T + \mathbf Q \\
\hline
\end{array}$

<u>**Measurment**</u><br>
Take measurement $z$<br>
<u>**Update**</u>

$\begin{array}{|l|l|l|}
\hline
\text{Univariate} & \text{Univariate} & \text{Multivariate}\\
& \text{(Kalman form)} & \\
\hline
& y = z - \hat x & \mathbf y = \mathbf z - \mathbf{H\hat x} \\
& K = \frac{\hat P}{\hat P+R}&
\mathbf K = \mathbf{\hat{P}H}^\mathsf T (\mathbf{H\hat{P}H}^\mathsf T + \mathbf R)^{-1} \\
\mu=\frac{\hat\sigma^2\, \mu_z + \sigma_z^2 \, \hat\mu} {\hat\sigma^2 + \sigma_z^2} & x = \hat x + Ky & \mathbf x = \hat{\mathbf x} + \mathbf{Ky} \\
\sigma^2 = \frac{\sigma_1^2\sigma_2^2}{\sigma_1^2+\sigma_2^2} & P = (1-K)\hat P &
\mathbf P = (\mathbf I - \mathbf{KH})\mathbf{\hat{P}} \\
\hline
\end{array}$ 

<u>**Predict next step**</u><br>

__The TASK:__ To design the state $\left(\hat \mathbf x, \mathbf P\right)$, the process $\left(\mathbf A, \mathbf Q\right)$, the measurement $\left(\mathbf x, \mathbf R\right)$, and the  measurement function $\mathbf H$. If the system has control inputs, such as a robot, also design $\mathbf B$ and $\mathbf u$.

__Practical Considerations:__
- $\mathbf{Q}$ (how sure we are about state values) and $\mathbf{R}$ (precision of measurement) are often assumed to be constant and determined beforehand, esp. $\mathbf{R}$ b/o ease.
- With constant $\mathbf{Q}$ and $\mathbf{R}$, $\mathbf{K}$ and $\mathbf{P}$ converge quickly, so they are often computed beforehand.
- Optional control input $u_t \in \mathbb{R^l}$ and other parameters $\mathbf{R}$ $\mathbf{A} \in \mathbb{R^{nxn}}$, $\mathbf{B} \in \mathbb{R^{nxl}}$ and $\mathbf{H} \in \mathbb{R^{mxn}}$ are calculated with EM algorithm using training data!
    * E-Step: find expectations with Kalman Filter and smoother
    * M-Step: calculate close-form solution of the paramaters
    * MARSS package in R
- KF can also go backwards in time by using measurements at later time to get earlier state by back substitution (smoothing).

#### Extended Kalman Filter (EKF)  _obsoleted by UKF_
- When functions are not linear globally
- Use taylor expansion and Jacobian to make function locally linear (many segements of linear functions)

#### Unscented Kalman Filter (UKF)
- Special Sigma $\chi$ points to estimate mean and covariance

#### Particle Filter
- Monte-Carlo method for non-linear filters 
- Easy to set up, high computation costs
- Does not need mean and covariance info

#### When to use State Space Model? 
Answer: reasonable to assume coefficients change a lot

### VECM (Vector Error Correction Model)
- Cointegration: two time series $\mathbf X$ and $\mathbf Y$ share common stochastic trend, i.e. 
    * $\mathbf X$ and $\mathbf Y$ are both $\mathbf I(1)$, i.e. first order differences are stationary ($\mathbf I(0)$)
    * $\exist \,  \theta  \,\, s.t. \,\, (\mathbf Y - \mathbf\theta \mathbf X$) is $\mathbf I(0)$
- Long run model: $\mathbf Y_t = \alpha + \beta \mathbf X_t$
- Short run model: $\Delta \mathbf Y_t = \alpha + \beta \Delta \mathbf X_t$ 
- VAR(1): $\Delta \mathbf Y_t = \alpha + \beta_1 \Delta \mathbf Y_{t-1} + \beta_2 \Delta \mathbf X_{t-1} + e_t$ 
- VECM(1): $\Delta \mathbf Y_t = \alpha + \beta_1 \Delta \mathbf Y_{t-1} + \beta_2 \Delta \mathbf X_{t-1} + \beta_3 \mathbf Y_{t-1} + \beta_4 \mathbf X_{t-1} + e_t$
- VECM(1): $\Delta \mathbf Y_t = \alpha + \beta_1 \Delta \mathbf Y_{t-1} + \beta_2 \Delta \mathbf X_{t-1} - \nu (\mathbf Y_{t-1} - \theta \mathbf X_{t-1}) + e_t$ (alternate form)
    * first two terms are _growth_ data, the next two are _level_ data.
    * Coefficients ( $\alpha$s, $\beta$s, $\theta$ and $\nu$) can change over time in a dynamic model!
    * 0 < $\nu$ < 1 is used to correct eratic fluactuation in data (damping) 
    * Use regression to get $\theta$ and get residual before applying VECM model

### Bayesian / Dynamic Model Averaging

#### Bayesian Model Averaging
- Start with a prior, use data to assign model probability over time
- Model parameter does not change over time

__INSIGHT:__ Posterior = Prior X Likelihood
$$ \mathbb P_{post} = \mathbb P_{prior} \times \ell_{like} $$

Q: How did we get this from Baye's Theorem?

#### Dynamic Model Averaging
- When BOTH model and parameters are uncertain
- BOTH parameters value and weght can change over time (hence dynamic)
- The Shrinkage variant (DMS) zeros params with small probability for economy and performance
- The importance of __forget factor $\lambda$__ 
- $\Sigma_{t|t-1} = \Sigma_{t-1|t-1} + W$\,, where $\Sigma_{t|t-1}$ is the covariance of $\theta_{t|t-1}$ 

__INSIGHT:__ Sum of coefficients close to 1 means consistent trend, otherwise possible bad model specification (ref. _H11b_bma.R_)

```
library(eDMA)
fit <- DMA(formula, data, vDelta=, vKeep=, dBeta=, dAlpha=)
```
- vDelta: which $\lambda$s to try
- vKeep: how many models are certain to include
- dBeta:
- dAlpha:

__INSIGHT:__ BMA is a special case of DMA where $\alpha = \lambda = 1$

### LSTM
- Forget gate similar to Forget Factor $\lambda$ in DMA
- Construct of LSTM closely resembles Kalman Filter!

