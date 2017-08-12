# class auc2(metric_base):
#     def __init__(self, k=999999, s_score='score'):
#         self.k = k
#         self.s_score = s_score
#
#     def __call__(self, df):


def auc2(metric_base):
    # metric_base = [old position, new position, product ID, Query, Query Length]
    k = 99999999

    # tp0 = 0.0
    # fp0 = 0.0
    # tp1 = 1.0
    # fp1 = 1.0
    # P = 0
    # N = 0
    # k0 = 0
    # k1 = 0

    # for name, row in df[:self.k].iterrows():
    #     act = row[s_label]
    #     if act>1e-9:
    #         P += 1.0
    #     else:
    #         N += 1.0
    P = 1
    N = metric_base[4]

    # if P==0:
    #     return 0.0
    # if N==0:
    #     return 1.0

    # for name, row in df[:self.k].iterrows():
    # metric_base = [old position, new position, product ID, Query, Query Length]
    testlist = [1, 2, 3, 4, 5, 6, 10, 20, 40, metric_base[4]]
    # if metric_base[4] > 40:
    #     testlist = [1, 2, 3, 4, 5, 6, 10, 20, 40, metric_base[4]]
    # elif metric_base[4] > 20:
    #     testlist = [1, 2, 3, 4, 5, 6, 10, 20, metric_base[4]]
    # elif metric_base[4] > 10:
    #     testlist = [1, 2, 3, 4, 5, 6, 10, metric_base[4]]
    # elif metric_base[4] > 6:
    #     testlist = [1, 2, 3, 4, 5, 6, metric_base[4]]
    # elif metric_base[4] > 5:
    #     testlist = [1, 2, 3, 4, 5, metric_base[4]]
    # elif metric_base[4] > 4:
    #     testlist = [1, 2, 3, 4, metric_base[4]]
    # elif metric_base[4] > 3:
    #     testlist = [1, 2, 3, metric_base[4]]
    # elif metric_base[4] > 2:
    #     testlist = [1, 2,  metric_base[4]]
    # else:
    #     testlist = [1,  metric_base[4]]

    oldAUC2 = [0.0] * len(testlist)
    newAUC2 = [0.0] * len(testlist)

    for y in xrange(len(testlist)):
        # reset
        tp0 = 0.0
        fp0 = 0.0
        # tp1 = 1.0
        fp1 = 1.0
        k0 = 0
        k1 = 0
        # for oldAUC2
        for x in xrange(testlist[y]):

            if x == metric_base[0] - 1:
                act = 1.0
            else:
                act = 0.0

            if act > 1e-9:
                k1 += 1
                tp1 = float(k1)/P
                fp1 = float(k0)/N
                oldAUC2[y] += (fp1-fp0)*(tp1+tp0)/2
                # print("kk", (fp1-fp0)*(tp1+tp0)/2, fp1, fp0, tp1, tp0, k1, k0)
                tp0 = tp1
                fp0 = fp1
            else:
                k0 += 1

        oldAUC2[y] += 1.0 - fp1

    for y in xrange(len(testlist)):
        # reset
        tp0 = 0.0
        fp0 = 0.0
        # tp1 = 1.0
        fp1 = 1.0
        k0 = 0
        k1 = 0

        # for newAUC2
        for x in xrange(testlist[y]):

            if x == metric_base[1] - 1:
                act = 1.0
            else:
                act = 0.0

            if act > 1e-9:
                k1 += 1
                tp1 = float(k1) / P
                fp1 = float(k0) / N
                newAUC2[y] += (fp1 - fp0) * (tp1 + tp0) / 2
                # print("kk", (fp1-fp0)*(tp1+tp0)/2, fp1, fp0, tp1, tp0, k1, k0)
                tp0 = tp1
                fp0 = fp1
            else:
                k0 += 1
        newAUC2[y] += 1.0 - fp1

    return [oldAUC2, newAUC2]
