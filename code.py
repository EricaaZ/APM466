import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

class bond:
    def __init__(self, ISIN, close_prices, maturity_date, coupon_rate, period):
        self.ISIN = ISIN
        self.price = close_prices
        self.maturity = maturity_date
        self.coupon = coupon_rate
        self.period = period

bond_list = []

# close prices for ten days of each bond
close_price_202031 = [99.85, 99.86, 99.86, 99.86, 99.86, 99.86, 99.86, 99.86, 99.86, 99.86]
bond_1 = bond("CA135087D929", close_price_202031, datetime.date(2020,3,1), 0.75, 0)
bond_list.append(bond_1)

close_price_202061 = [100.70, 100.70, 100.69, 100.69, 100.68, 100.66, 100.65, 100.65, 100.64, 100.64]
bond_2 = bond("CA135087YZ11", close_price_202061, datetime.date(2020,6,1), 1.75, 0)

close_price_202091 = [99.26, 99.28, 99.28, 99.27, 99.28, 99.28, 99.28, 99.27, 99.28, 99.30]
bond_3 = bond("CA135087E596", close_price_202091, datetime.date(2020,9,1), 0.375, 1)
bond_list.append(bond_3)

close_price_202131 = [98.89, 98.93, 98.95, 98.94, 98.92, 98.92, 98.88, 98.90, 98.90, 98.93]
bond_4 = bond("CA135087F254", close_price_202131, datetime.date(2021,3,1), 0.375, 2)
bond_list.append(bond_4)

close_price_202191 = [98.41, 98.45, 98.49, 98.46, 98.46, 98.43, 98.43, 98.38, 98.41, 98.42]
bond_5 = bond("CA135087F585", close_price_202191, datetime.date(2021,9,1), 0.375, 3)
bond_list.append(bond_5)

close_price_202231 = [97.57, 97.63, 97.66, 97.65, 97.64, 97.60, 97.61, 97.57, 97.58, 97.61]
bond_6 = bond("CA135087G328", close_price_202231, datetime.date(2022,3,1), 0.25, 4)
bond_list.append(bond_6)

close_price_202331 = [100.31, 100.42, 100.48, 100.45, 100.44, 100.35, 100.31, 100.27, 100.31, 100.38]
bond_7 = bond("CA135087H490", close_price_202331, datetime.date(2023,3,1), 0.875, 5)
bond_list.append(bond_7)

close_price_202431 = [102.52, 102.65, 102.75, 102.58, 102.68, 102.53, 102.47, 102.46, 102.54, 102.64]
bond_8 = bond("CA135087J546", close_price_202431, datetime.date(2024,3,1), 1.125, 6)
bond_list.append(bond_8)

close_price_202491 = [98.72, 98.95, 99.29, 99.11, 99.25, 98.99, 99.03, 99.06, 98.99, 99.10]
bond_9 = bond("CA135087J967", close_price_202491, datetime.date(2024,9,1), 0.75, 7)
bond_list.append(bond_9)

close_price_202531 = [98.24, 98.43, 98.58, 98.48, 98.48, 98.30, 98.25, 98.24, 98.34, 98.47]
bond_10 = bond("CA135087K528", close_price_202531, datetime.date(2025,3,1), 0.625, 8)
bond_list.append(bond_10)

price_date = {}
price_date[0] = datetime.date(2020,1,2)
price_date[1] = datetime.date(2020,1,3)
for x in range(2,7):
    price_date[x] = datetime.date(2020,1,x+4)
price_date[7] = datetime.date(2020, 1, 13)
price_date[8] = datetime.date(2020, 1, 14)
price_date[9] = datetime.date(2020, 1, 15)

period_dict = {}
for x in range(0,5):
    period_dict[x] = x
period_dict[5] = 6
period_dict[6] = 8
period_dict[7] = 9
period_dict[8] = 10

def present_value(bond, date_day):
    d_price = ((123 + date_day)/183)*bond.coupon
    present_val = round(d_price + bond.price[date_day], 4)
    return present_val
 
def time_diff(first_d, second_d):
    diff = (second_d - first_d).total_seconds()
    res = round(divmod(diff, 86400)[0] / 365, 3)
    return res
    
def year_frac(price_date, year_frac_dict):
    loc = 0
    for i in range(0,8):
        year_frac = time_diff(price_date, bond_list[i].maturity)
        year_frac_dict[loc] = year_frac
        
        check = time_diff(bond_list[i].maturity, bond_list[i+1].maturity)
        
        if check > 0.6:
            next_year_frac = time_diff(price_date, bond_list[i+1].maturity)
            year_frac_dict[loc+1] = (year_frac + next_year_frac)/2
            loc += 1
        loc += 1
    year_frac_dict[loc] = time_diff(price_date, bond_list[-1].maturity)
    return year_frac_dict


def total_present_value(f_val, coupon, period, rate, year_frac_dict):
    result = 0
    total_period = period_dict[period]

    if (period == 0):
        result += f_val*math.exp(-year_frac_dict[0] * rate)
    else:
        for i in range(total_period):
            result += coupon * math.exp(-year_frac_dict[i] * rate)
        result += f_val * math.exp(-year_frac_dict[i+1] * rate)
    return result
 
def ytm(bond, date_day, year_frac_dict):
    pre_val = present_value(bond, date_day)
    f_val = bond.coupon + 100
    
    ytm_1= bond.coupon/100
    check_1 = True
    while check_1:
        if (pre_val < f_val):
            ytm_1 -= 0.000001
        else:
            ytm_1 += 0.000001
 
        pv_1 = total_present_value(f_val, bond.coupon, bond.period, ytm_1, year_frac_dict)
 
        if (pre_val < f_val):
            check_1 = pv_1 < pre_val
        else:
            check_1 = pv_1> pre_val
            
    ytm_2= bond.coupon/100
    check_2 = True
    while check_2:
        if (pre_val < f_val):
            ytm_2 += 0.000001
        else:
            ytm_2 -= 0.000001
 
        pv_2 = total_present_value(f_val, bond.coupon, bond.period, ytm_2, year_frac_dict)
 
        if (pre_val < f_val):
            check_2 = pv_2 > pre_val
        else:
            check_2 = pv_2 < pre_val
    return max(ytm_1 * 100, ytm_2 * 100)

def ytm_every_day(bond_list):
    day_true_ytm = {}
    day_est_ytm = {}
    day_year_frac = {}

    for i in range(10):
        true_ytm = []
        est_ytm = []
        input_dict = {}
        year_frac_dict = year_frac(price_date[i], input_dict)

        j = 0
        while(j < 8):
            ytm_val = ytm(bond_list[j], i, year_frac_dict)
            # print(ytm_val)
            true_ytm.append(ytm_val)
            est_ytm.append(ytm_val)
            
            if (time_diff(bond_list[j].maturity, bond_list[j+1].maturity) > 0.6):
                next_ytm = ytm(bond_list[j+1], i, year_frac_dict)
                avg_ytm = (next_ytm + ytm_val)/2
                est_ytm.append(avg_ytm)
            j += 1

        last_ytm = ytm(bond_list[-1], i, year_frac_dict)
        true_ytm.append(last_ytm)
        est_ytm.append(last_ytm)
        day_true_ytm[i] = true_ytm
        day_est_ytm[i] = est_ytm
        day_year_frac[i] = year_frac_dict

    return day_true_ytm, day_est_ytm, day_year_frac

day_true_ytm, day_est_ytm, day_year_frac_dict = ytm_every_day(bond_list)

date = ['Jan 2', 'Jan 3', 'Jan 6', 'Jan 7', 'Jan 8', 'Jan 9', 'Jan 10', 'Jan 13', 'Jan 14', 'Jan 15']
plt.xticks(ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],labels = ['20/3','20/9','21/3','21/9', '22/3', '22/9', '23/3', '23/9', '24/3', '24/9','25/3'])
for i in range(10):
    plt.plot(day_est_ytm[i], label = date[i])
plt.xlabel('time to maturity')
plt.ylabel('yield to maturity')
plt.title('five year yield curve')
plt.legend(loc=1, prop={'size': 6})
plt.show()

def total_spot_rate_pre_val(f_val, coupon, period, rate, year_frac_dict, spot_rate, gap):
    res = 0
    total_period = period_dict[period]

    if gap == False:
        for i in range(total_period):
            res += coupon * math.exp(-year_frac_dict[i] * (spot_rate[i]/100))
        res += f_val * math.exp(-year_frac_dict[i+1] * rate)
    else:
        for i in range(total_period - 1):
            res += coupon * math.exp(-year_frac_dict[i] * (spot_rate[i]/100))
        res += coupon * math.exp(-year_frac_dict[i+1] * ((spot_rate[-1]/100 + rate)/2))
        res += f_val * math.exp(-year_frac_dict[i+2] * rate)

    return res
 
 
def spot_rate(bond, date_day, bond_index, year_frac_dict, spot_rate, ytm_list, gap):
    pre_val = present_value(bond, date_day)
    f_val = bond.coupon + 100
    
    spot_rate_1 = ytm_list[bond_index]/100
    check_1 = True
    while check_1:
        if (pre_val < f_val):
            spot_rate_1 -= 0.000001
        else:
            spot_rate_1 += 0.000001
 
        pv_1 = total_spot_rate_pre_val(f_val, bond.coupon, bond.period, spot_rate_1, year_frac_dict, spot_rate, gap)

        if (pre_val < f_val):
            check_1 = pv_1 < pre_val
        else:
            check_1 = pv_1 > pre_val

    spot_rate_2 = ytm_list[bond_index]/100
    check_2 = True
    while check_2:
        if (pre_val < f_val):
            spot_rate_2 += 0.000001
        else:
            spot_rate_2 -= 0.000001

        pv_2 = total_spot_rate_pre_val(f_val, bond.coupon, bond.period, spot_rate_2, year_frac_dict, spot_rate, gap)
        
        if (pre_val < f_val):
            check_2 = pv_2 > pre_val
        else:
            check_2 = pv_2 < pre_val

    return max(spot_rate_1*100, spot_rate_2*100)
 
 
 
def spot_rate_every_day(bond_list, day_year_frac_dict):
    spot_rt_dict = {}
    for i in range(10):
        spot_rt_list = []
        for j in range(len(bond_list)):
            ytm_list = day_true_ytm[i]

            if j == 0:
                spot_rt_list.append(ytm_list[0])
            if j >= 1:
                bond = bond_list[j]
                if time_diff(bond_list[j-1].maturity, bond.maturity) > 0.6:
                    spot_rt = spot_rate(bond_list[j], i, j, day_year_frac_dict[i], spot_rt_list, ytm_list, True)
                    spot_rt_list.append((spot_rt_list[-1] + spot_rt)/2)
                    spot_rt_list.append(spot_rt)
                else:
                    spot_rt = spot_rate(bond_list[j], i, j, day_year_frac_dict[i], spot_rt_list, ytm_list, False)
                    spot_rt_list.append(spot_rt)
        spot_rt_dict[i] = spot_rt_list
    return spot_rt_dict

                    
spot_rate_dict = spot_rate_every_day(bond_list, day_year_frac_dict)

date = ['Jan 2', 'Jan 3', 'Jan 6', 'Jan 7', 'Jan 8', 'Jan 9', 'Jan 10', 'Jan 13', 'Jan 14', 'Jan 15']
plt.xlabel('time to maturity')
plt.ylabel('spot rate')
plt.title('five year spot rate curve')
axes = plt.gca()
axes.set_ylim([1.4, 2.8])
plt.xticks(ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],labels = ['20/3','20/9','21/3','21/9', '22/3', '22/9', '23/3', '23/9', '24/3', '24/9','25/3'])
for i in range(10):
    plt.plot(spot_rate_dict[i], label = date[i])
plt.legend(loc=1, prop={'size': 6})
plt.show()

def forward_rate(spot_r_dict):
    forward_rt_dict = {}
    for i in range(len(spot_r_dict)):
        forward_rt_list = []
        rate_used = spot_r_dict[i][2]

        j = 2
        l = 4
        while(l < len(spot_r_dict[0])):
            forw = (spot_r_dict[i][l] * j - rate_used)/(j-1)
            forward_rt_list.append(forw)        
            j += 1
            l += 2
        forward_rt_dict[i] = forward_rt_list
    return forward_rt_dict


forward_rate_dict = forward_rate(spot_rate_dict)

dates = ['Jan 2', 'Jan 3', 'Jan 6', 'Jan 7', 'Jan 8', 'Jan 9', 'Jan 10', 'Jan 13', 'Jan 14', 'Jan 15']
plt.xlabel('year')
plt.ylabel('forward rate')
plt.title('five year forward rate curve')
axes = plt.gca()
axes.set_ylim([1.4, 1.72])
plt.xticks(ticks = [0, 1, 2, 3],labels = ['1yr-1yr','1yr-2yr','1yr-3yr','1yr-4yr'])
for i in range(10):
    plt.plot(forward_rate_dict[i], label = dates[i])
plt.legend(loc=1, prop={'size': 6})
plt.show()

def ytm_cov(est_ytm):
    ytm_lst = []
    for i in range(10):
        n = 1
        res_list = []
        while (n < len(est_ytm[0])):
            res_list.append(est_ytm[i][n])
            n += 2
        ytm_lst.append(res_list)

    ytm_lst = np.array(ytm_lst).transpose()

    log_returns = np.zeros((5, 9))
    for i in range(len(ytm_lst)):
        for j in range(len(ytm_lst[i])-1):
            log_returns[i][j] = math.log(ytm_lst[i][j]/ytm_lst[i][j+1])

    return np.cov(log_returns)

ytm_cov_log_re = ytm_cov(day_est_ytm)


def forward_cov(for_r_dict):
    for_r_list = []
    for i in range(10):
        n = 0
        res_list = []
        while (n < len(for_r_dict[0])):
            res_list.append(for_r_dict[i][n])
            n += 1
        for_r_list.append(res_list)

    for_r_list = np.array(for_r_list).transpose()

    log_returns = np.zeros((4, 9))
    for i in range(len(for_r_list)):
        for j in range(len(for_r_list[i])-1):
            log_returns[i][j] = math.log(for_r_list[i][j]/for_r_list[i][j+1])
    return np.cov(log_returns)

forward_cov_log_re = forward_cov(forward_rate_dict)


ytm_val, ytm_vec = np.linalg.eig(ytm_cov_log_re)
forward_val, forward_vec = np.linalg.eig(forward_cov_log_re)
