"""
===============
Defuzzification
===============
Fuzzy logic calculations are excellent tools, but to use them the fuzzy result
must be converted back into a single number. This is known as defuzzification.
There are several possible methods for defuzzification, exposed via
`skfuzzy.defuzz`.
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from Level import Level

driving = {
    "bad": Level("bad", 0, 30, 0, 20),
    "average": Level("average", 50, 50, 20, 20),
    "good": Level("good", 80, 100, 20, 0)
}

# Generate trapezoidal membership function on range [0, 1]
x = np.arange(0, 100, 1)

mfx_bad = fuzz.trapmf(x, driving["bad"].get_abcd())
mfx_average = fuzz.trapmf(x, driving["average"].get_abcd())
mfx_good = fuzz.trapmf(x, driving["good"].get_abcd())

# Collect info for vertical lines
labels = ['bad', 'average', 'good']
xvals = [mfx_good, mfx_average, mfx_bad]
colors = ['r', 'y', 'g']
ymax = [fuzz.interp_membership(x, mfx_bad, i) for i in xvals]

# Display and compare defuzzification results against membership function
plt.figure(figsize=(8, 5))

bad, = plt.plot(x, mfx_bad, 'k', label=driving["bad"].get_name(), color="red")
average, = plt.plot(x, mfx_average, 'k', label=driving["average"].get_name(), color="yellow")
good, = plt.plot(x, mfx_good, 'k', label=driving["good"].get_name(), color="green")

plt.ylabel('Membership')
plt.xlabel('Driving quality')
plt.ylim(0, 1)
plt.legend(handles=[bad, average, good])

plt.show()
