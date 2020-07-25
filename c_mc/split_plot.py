import matplotlib.pyplot as plt
fig = np.empty(4, object)
ax = np.empty(4, object)

for season in range(4):
    fig[season] = plt.figure()
    ax[season] = plt.axes()
    for year in range(6):
        ax[season].plot(split_pv.seasons[season][year,:], label=f"{year}")
        ax[season].set_title(f"Season Number {season}")
        ax[season].legend()

plt.show()
