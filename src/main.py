import preprocessing

# Part 1: Preprocess the data
ev_in = 'data/in/parking_lot.mat'
ev_out = 'data/preprocessing/ev.npy'

my_ev = preprocessing.EV(ev_in)
my_ev.run()
my_ev.save(ev_out)


pv_in = 'data/in/solar_wind.mat'
pv_out = 'data/preprocessing/pv.npy'

my_pv = preprocessing.PV(pv_in)
my_pv.run()
my_pv.save(pv_out)


wt_in = 'data/in/solar_wind.mat'
wt_out = 'data/preprocessing/wt.npy'

my_wt = preprocessing.WT(wt_in)
my_wt.run()
my_wt.save(wt_out)
