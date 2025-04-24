# Distribution Moments

Moment of a function is a measure of the function shape 

In probability theory it is a statistic over the variable distribution - see definitions below

__Raw moment__ is a weighted by PDF power of the argument

<img src="img/moments1.svg" width=400 style="float: left;"><div style="clear: both;"></div><br>

__Moment about c__ is a moment with shifted argument

<img src="img/moments2.svg" width=250 style="float: left;"><div style="clear: both;"></div><br>



__Central moment__ is a moment around its mean

<img src="img/central1.png" width=250 style="float: left;"><div style="clear: both;"></div><br>

__Standardized moment__ is a moment divided by the power of its second moment

<img src="img/moments3.svg" width=300 style="float: left;"><div style="clear: both;"></div><br>


## Etimology



## Main Moments

|N|Moment|Measures what|
|---|---|---|
|1st Raw|Mean|Center of Mass|
|2nd Central|Variance|Distribution|
|3rd Central|Skewness|Assymetry|
|4th Central|Kurtosis|Tail-heaviness/peakedness|


### Skewness

Skewness measures an expected deviation around the mean (raised to 3rd power)<br> It is normalized by the same power of standard deviation to make it scale-invariant.
<img src="img/skewness.png" width=250>
- Since there is a third (odd) power any assymetry in the distribution contributes to the final measure. This is what Skewness supposed to measure<br>
- Skewness can be negative depending on the assymetry direction


### Kurtosis

Kurtosis measures an expected deviation around the mean (raised to 4rd power)<br> It is normalized by the same power of standard deviation to make it scale-invariant.
<img src="img/kurtosis.png" width=250>
- Since there is a fourth (even) power heavy tails from both sides contribute the most to the final output<br>

Comparison of shapes with respect to distribution moments
<img src="img/moments5.png" width=600>


### Higher order moments


In theory there are much more momemnts that exist

<img src="img/moments4.png" width=400>



## Usage

Method of moments = equalize analytic and sample expressions for the moments and solve this system oif equations

Alternative to Maximum Likelihood estimation




