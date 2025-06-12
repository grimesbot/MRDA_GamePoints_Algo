import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import pandas as pd
from scipy.interpolate import make_interp_spline
import matplotlib.dates as mdates
from datetime import datetime

# # x = np.arange(5)
# # y = np.random.random(5)


# # plt.plot(x2, y2, color='b')
# # plt.plot(x, y, ls='', marker='o', color='r')

# # plt.show()


# x = ['2024-01-01','2024-03-10','2024-05-10','2024-06-01','2024-10-15']
# gpfs = [1,1,3,6,3]
# fun = interp1d(x=x, y=gpfs, kind=2)
# x2 = np.linspace(start=x[0], stop=x[-1], num=1000)
# y2 = fun(x2)

# # # Smooth GPF values using Savitzky-Golay filter
# # if len(gpfs) > 2:  # Smoothing requires at least a few points
# #     smoothed_gpfs = savgol_filter(gpfs, window_length=3, polyorder=2)
# # else:
# #     print("smoothing didn't work")
# #     smoothed_gpfs = gpfs  # Use raw values if not enough points for smoothing


# smoothed = savgol_filter(gpfs, window_length=5, polyorder=2)
# plt.plot(x, smoothed)
    
# # plt.plot(x2, y2, color='b')
# # plt.plot(x, gpfs, ls='', marker='o', color='r')

# plt.show()

# Input data
x = ['2024-01-01', '2024-03-10', '2024-05-10', '2024-06-01', '2024-10-15']
y = [1, 1, 3, 6, 3]

# Convert dates to datetime objects and numerical format for interpolation
dates = [datetime.strptime(date, '%Y-%m-%d') for date in x]
x_numeric = mdates.date2num(dates)

# Create a smoothed spline
x_smooth = np.linspace(x_numeric.min(), x_numeric.max(), 300)
spline = make_interp_spline(x_numeric, y, k=3)
y_smooth = spline(x_smooth)

# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot_date(dates, y, 'o', label='Original Data', color='blue')  # Original points
ax.plot(mdates.num2date(x_smooth), y_smooth, '-', label='Smoothed Curve', color='red')  # Smoothed curve

# Format the x-axis with date labels
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
ax.set_title("Smoothed Plot of Unequally Distributed Dates")
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.legend()
plt.tight_layout()
plt.show()
