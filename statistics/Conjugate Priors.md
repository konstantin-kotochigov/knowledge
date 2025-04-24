# Conjugate priors

Решается задача статистики = оценить параметр распределения $\theta$ по наблюдаемым данным $X$.

В рамках Байесовского подхода это делается итеративно - приходят новые наблюдения, обновляем вероятности параметра

$$P(\theta|x) = \frac{P(x|\theta) P(\theta)}{P(x)} = \frac{\text{Likelihood} \times \text{Prior}}{\text{Marginal}}$$

$P(\theta)$ = bayesian prior, aka текущее накопленное знание

Форму прайора можно выбритать любой, НО если моделировать его распределением похожим по форме на Likelihood, то оно<br> 1) не будет терять форму после обновления<br> 2) довольно легко обновляется

Для многих популярных распределений (в основном потому что они похожи) есть такой формат prior-а. Если мы согласовали Prior, тогда такое распрделеение называется Conjugate distribution (или сопряженным).

Это свойство легко проиллюстрировать<br>
1.Берем Likelihood распределения Бернулли:
$$P(x|p) = p^{S}(1-p)^{N-S}$$
2.Берем Prior в виде Beta распределения:
$$P(p) = p^{\alpha-1}(1-p)^{\beta-1}$$

Перемножаем, получаем Beta распредeление
$$P(p|x) = \frac{p^{[S + \alpha - 1]}(1-p)^{[\beta + N - S - 1]}}{P(x)}$$

Список сопряженных распределений
1. Beta for modeling frequencies (Bernoulli, Binomial, Negative Binomial, Geometric)
2. Gamma for modeling rates (Poisson, Exponential)
3. Dirichlet for modeling Probability vectors that sum to one (Categorical, Multinomial)
4. Normal for modeling normal means
