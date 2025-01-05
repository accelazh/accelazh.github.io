import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np


consider_power_price = True


hdd_price_capacity = 0.02
ssd_price_capacity = 0.2

hdd_price_bandwidth = 2000
ssd_price_bandwidth = 0.2/0.00065

hdd_power_bandwidth = 65
ssd_power_bandwidth = 10
power_price = 0.1

def calc_hdd_price(capacity, bandwidth):
  cost_capacity = hdd_price_capacity * capacity
  cost_bandwidth = hdd_price_bandwidth * bandwidth
  cost = max(cost_capacity, cost_bandwidth)
  if consider_power_price:
    purchase_cost = cost
    cost = purchase_cost / 60 \
      + bandwidth * hdd_power_bandwidth / 1000 \
        * 30 * 24 * power_price
  return cost

def calc_ssd_price(capacity, bandwidth):
  cost_capacity = ssd_price_capacity * capacity
  cost_bandwidth = ssd_price_bandwidth * bandwidth
  cost = max(cost_capacity, cost_bandwidth)
  if consider_power_price:
    purchase_cost = cost
    cost = purchase_cost / 60 \
      + bandwidth * ssd_power_bandwidth / 1000 \
        * 30 * 24 * power_price
  return cost

def calc_price(capacity, bandwidth):
  cost_hdd = calc_hdd_price(capacity, bandwidth)
  cost_ssd = calc_ssd_price(capacity, bandwidth)
  return min(cost_hdd, cost_ssd)

def sel_hdd_ssd(capacity, bandwidth):
  cost_hdd = calc_hdd_price(capacity, bandwidth)
  cost_ssd = calc_ssd_price(capacity, bandwidth)
  if (cost_hdd < cost_ssd):
    return {
      "sel": "hdd",
      "cost": cost_hdd
    }
  else:
    return {
      "sel": "ssd",
      "cost": cost_ssd
    }


fig = plt.figure()
ax = plt.axes(projection='3d')

step = 100
x = np.logspace(math.log10(1), math.log10(1000 * 1000), step)
y = np.logspace(math.log10(0.00001), math.log10(800), step)

X, Y = np.meshgrid(x, y)

assert len(X) == len(Y)
Z = []
for row in range(0, len(X)):
  assert len(X[row]) == len(Y[row])
  Z.append([sel_hdd_ssd(X[row][col], Y[row][col])["cost"] 
    for col in range(0, len(X[row]))])

Z = np.array(Z)

ax.plot_surface(X, Y, Z, 
  cmap='viridis', 
  edgecolor='green')

ax.set_xlabel('Capacity (GB)')
ax.set_ylabel('Bandwidth (GBps)')
ax.set_zlabel('Cost monthly $' if consider_power_price else 'Cost $')

ax.set_xlim(1, 1000 * 1000)
ax.set_ylim(0.00001, 1000)
#ax.set_zlim(0, 250 * 1000)

def number_formatter(value, tick_number):
  if value % 1000 == 0:
    return f"{int(value / 1000)}k"
  else:
    return f"{int(value):,}"

ax.zaxis.set_major_formatter(FuncFormatter(number_formatter))

ax.set_title('Choosing HDD/SSD by capacity, bandwidth')
plt.show()



