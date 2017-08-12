class auc2(metric_base):
    def __init__(self, k=999999, s_score='score'):
        self.k = k
        self.s_score = s_score

    def __call__(self, df):
        auc = 0.0

        tp0 = 0.0
        fp0 = 0.0
        tp1 = 1.0
        fp1 = 1.0
        P = 0
        N = 0
        k0 = 0
        k1 = 0

        for name, row in df[:self.k].iterrows():
            act = row[s_label]
            if act>1e-9:
                P += 1.0
            else:
                N += 1.0

        if P==0:
            return 0.0
        if N==0:
            return 1.0

        for name, row in df[:self.k].iterrows():
            act = row[s_label]
            if act > 1e-9:
                k1 += 1
                tp1 = float(k1)/P
                fp1 = float(k0)/N
                auc += (fp1-fp0)*(tp1+tp0)/2
                #print("kk", (fp1-fp0)*(tp1+tp0)/2, fp1, fp0, tp1, tp0, k1, k0)
                tp0 = tp1
                fp0 = fp1
            else:
                k0 += 1

        auc += 1.0 - fp1
        return auc
