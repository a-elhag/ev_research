## Part 0: Importing
import numpy as np
import matplotlib.pyplot as plt

class GenerateDG():
    def __init__(self):
        self.characteristics()

    def mat2num(self, s):
        return np.array(np.matrix(s.strip('[]')))

    def characteristics(self):
        """
        There are three DG characteristics we are concered with:

        1) Cap (Capacity)
           This is the maximum generating capacity of generator (i) in MW
        2) MTTF(Mean Time to Fail)
           As the name suggests, for generator (i) this is the mean time that it
           will take to fail.
           For example, generator 6 has a MTTF of 450 hours. Meaning on average, we
           expect it to fail every 450 hours.
        3) MTTR(Mean Time to Repair)
           Evident from name. For example, that same generator 6 has a MTTR of 50
           hours. Meaning that when it fails, it will take on average 50 hours to
           bring it back online
        """
        # Initializing DG Characteristics
        self.Cap = '[12 12 12 12 12 20 20 20 20 50 50 50 50 50 50 76 76 76 76 100 100 100 \
            155 155 155 155 197 197 197 350 400 400]'
        self.MTTF = '[2940 2940 2940 2940 2940 450 450 450 450 1980 1980 1980 1980 1980 \
            1980 1960 1960 1960 1960 1200 1200 1200 960 960 960 960 950 950 950 1150 \
            1100 1100]'
        self.MTTR = '[60 60 60 60 60 50 50 50 50 20 20 20 20 20 20 40 40 40 40 50 50 50 40 \
            40 40 40 50 50 50 100 150 150]'
        self.Cap = self.mat2num(self.Cap)
        self.MTTF = self.mat2num(self.MTTF)
        self.MTTR = self.mat2num(self.MTTR)
        # Shape should be (x,1)
        self.Cap = self.Cap.reshape(-1, 1)
        self.MTTF = self.MTTF.reshape(-1, 1)
        self.MTTR = self.MTTR.reshape(-1, 1)

    def monte(self, years):
        # Variables
        years_simu = 0
        xtra_mul = 1.1
        """
        This is making sure we generate enough years. Since we are not exactly
        sure how much years we are generating, this code will initially generate
        iter with an extra multiplier. If more is indeed needed, then the
        multiplier is mulitplied by 1.1. Until the condition is satisified
        """
        while years>=years_simu:
            """
            This while loop generates our VS for DG. It is through the following steps:

            1) Generate the minimum number of failures we wish to simulate
               (if it is not enough, xtra_mul will increase the number of years to
                simulate and try again. The variable `years_simu` is the one that will
                check)

               The formulae is really easy, you convert the years you want to
               simulate into hours (x8760). Then divide it by the minimum MTTF
               of all the generators. It will give you a minimum number of failures
               to simulate for.
            """
            # How many fails to generate
            fails = np.ceil(xtra_mul*years*8760/self.MTTF.min())
            fails = fails.astype(int)

            # Generating fails + repairs
            R1 = np.random.rand(32,fails)
            R2 = np.random.rand(32,fails)

            # Shape (32,1) ==> (32,fails) 
            MTTF_Rep = np.tile(self.MTTF,(1,fails))
            MTTR_Rep = np.tile(self.MTTR,(1,fails))

            TTF = np.round(-MTTF_Rep*np.log(R1))
            TTR = np.round(-MTTR_Rep*np.log(R2))

            hours_sim = TTF.sum(1)+TTR.sum(1)
            hours_sim = hours_sim.min()
            years_simu = np.floor(hours_sim/8760)

            xtra_mul = xtra_mul*1.1

        cap_rep = np.tile(self.Cap.astype('i2'), (1, years*8760))
        total_time = TTF.sum(axis=1) + TTR.sum(axis=1)
        total_time = total_time.astype('i4')
        self.data_out = np.ones((32, total_time.max()), dtype=int)

        for DG in range(32):
            idx_tot = 0
            for idx in range(TTF.shape[1]):
                idx1 = idx_tot + TTF[DG, idx]
                idx2 = idx1 + TTR[DG, idx]
                idx1 = idx1.astype('i4')
                idx2 = idx2.astype('i4')
                self.data_out[DG, idx1:idx2] = 0
                idx_tot += TTF[DG, idx] + TTR[DG, idx]

        hours_simu = 8760 * years_simu
        hours_simu = hours_simu.astype('i')
        self.data_out = self.data_out[:, :hours_simu]



dg_gen = GenerateDG()
dg_gen.monte(10)


