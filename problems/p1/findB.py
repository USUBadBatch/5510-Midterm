from math import sqrt
import math


def sqr(num):
    return num ** 2

def ln(num):
    return math.log(num)


def thetaToArcLength(theta, spiralParams, start=0):
    (a, b) = spiralParams
    c = start
    d = theta

    aPlusBj = a + b * d

    return (
        b *
        (((a + b * d) * sqrt(sqr(b) + sqr(a + b * d))) / (2 * sqr(b)) -
         ((a + b * c) * sqrt(sqr(b) + sqr(a + b * c))) / (2 * sqr(b)) +
            .5 *
         (ln(abs(a + b * d + sqrt(sqr(b) + sqr(a + b * d))) / abs(b)) -
          ln(abs(a + b * c + sqrt(sqr(b) + sqr(a + b * c))) / abs(b))))
    )



def theta(b):
    return 5 / b

def main():
    for i in range(0, 501):
        b = 5.6
        b = b + .001 * i
        t = theta(b)
        l = thetaToArcLength(t, (0, b))
        print(f"b: {b:8.5} Theta: {t:5.5}, Arc Length: {l:5.5}, Arc Length / .8: {l / .8}")















main()
