#!/usr/bin/python
import sys
import datetime

# Calculates death probabilities based on Social Security
# actuarial tables for a given group of people.

# Run with a list of ages/genders and
# an optional timespan (or year in the future):

# python actuary.py 63m 80m 75f 73m 10

# or:

# python actuary.py 63m 80m 75f 73m 2022

# This will give statistics for that group, including
# various probabilities over 10 years. Years can be
# ommitted and it will still give some statistics.
# If "Years" exceeds the current calendar year,
# it will be interpreted as a date.


# replaced with Japanese one
# http://www.mhlw.go.jp/toukei/saikin/hw/life/21th/index.html
bothtables = [[0.00037, 0.00026, 0.00018, 0.00013, 0.00011, 0.00010, 0.00009,
               0.00008, 0.00008, 0.00008, 0.00010, 0.00011, 0.00013, 0.00015,
               0.00019, 0.00024, 0.00030, 0.00038, 0.00045, 0.00051, 0.00057,
               0.00061, 0.00064, 0.00064, 0.00064, 0.00065, 0.00066, 0.00067,
               0.00068, 0.00069, 0.00071, 0.00074, 0.00077, 0.00081, 0.00085,
               0.00090, 0.00098, 0.00108, 0.00118, 0.00128, 0.00140, 0.00152,
               0.00166, 0.00181, 0.00198, 0.00216, 0.00238, 0.00263, 0.00289,
               0.00317, 0.00347, 0.00381, 0.00419, 0.00461, 0.00507, 0.00558,
               0.00612, 0.00669, 0.00732, 0.00810, 0.00888, 0.00961, 0.01037,
               0.01121, 0.01214, 0.01319, 0.01434, 0.01553, 0.01685, 0.01842,
               0.02023, 0.02227, 0.02466, 0.02753, 0.03087, 0.03478, 0.03919,
               0.04420, 0.04974, 0.05568, 0.06208, 0.06937, 0.07793, 0.08752,
               0.09785, 0.10827, 0.11926, 0.13135, 0.14503, 0.16041, 0.17569,
               0.19195, 0.20922, 0.22755, 0.24695, 0.26744, 0.28905, 0.31177,
               0.33560, 0.36051, 0.38649, 0.41348, 0.44142, 0.47023, 0.49980,
               0.53002, 0.56075, 0.59182, 0.62304, 0.65422],
              [0.00033, 0.00023, 0.00015, 0.00011, 0.00009, 0.00008, 0.00008,
               0.00007, 0.00006, 0.00006, 0.00006, 0.00007, 0.00008, 0.00010,
               0.00012, 0.00014, 0.00016, 0.00019, 0.00021, 0.00024, 0.00025,
               0.00026, 0.00026, 0.00026, 0.00026, 0.00027, 0.00028, 0.00031,
               0.00034, 0.00036, 0.00038, 0.00040, 0.00042, 0.00045, 0.00048,
               0.00052, 0.00056, 0.00061, 0.00066, 0.00071, 0.00076, 0.00082,
               0.00091, 0.00100, 0.00108, 0.00115, 0.00124, 0.00138, 0.00153,
               0.00167, 0.00179, 0.00191, 0.00204, 0.00219, 0.00236, 0.00254,
               0.00273, 0.00292, 0.00313, 0.00340, 0.00370, 0.00401, 0.00434,
               0.00465, 0.00498, 0.00537, 0.00584, 0.00634, 0.00692, 0.00767,
               0.00856, 0.00961, 0.01083, 0.01224, 0.01381, 0.01558, 0.01763,
               0.02006, 0.02284, 0.02600, 0.02956, 0.03371, 0.03867, 0.04458,
               0.05155, 0.05937, 0.06837, 0.07843, 0.08949, 0.10160, 0.11490,
               0.12964, 0.14628, 0.16458, 0.18367, 0.20330, 0.22398, 0.24573,
               0.26854, 0.29242, 0.31734, 0.34328, 0.37021, 0.39806, 0.42678,
               0.45627, 0.48643, 0.51715, 0.54827, 0.57965, 0.61112, 0.64247,
               0.67352, 0.70404]]


def deathprob(age, years):
    # negative ages = female
    act = []
    if age < 0:
        act = bothtables[1]
        age = -1 * age
    else:
        act = bothtables[0]
    while(len(act) < int(age+years+2)):
        # slower/bloaiter but keeps things clean
        act.append(act[-1]**0.5)
    liveprob = 1
    i = 0
    iage = int(age)
    fage = age % 1
    while i <= years-1:
        thisyear = (1-fage)*act[iage+i]+fage*act[iage+i+1]
        liveprob *= 1-thisyear
        i += 1
    if years % 1:  # Amortizes risk of dying over a partial year, which is
                # 1-P(living last full year)^(year fraction)
        lastyear = (1-fage)*act[iage+i]+fage*act[iage+i+1]
        lastyearlive = 1-lastyear
        lastyearlive = lastyearlive**((years % 1))
        liveprob *= lastyearlive
    return 1-liveprob


def proballdie(ages, years):
    probsliving = []
    for i in ages:
        probsliving.append(1-deathprob(i, years))
    prod = 1
    for i in probsliving:
        prod *= (1-i)
    return prod


def probanydie(ages, years):
    probsliving = []
    for i in ages:
        probsliving.append(1-deathprob(i, years))
    prod = 1
    for i in probsliving:
        prod *= i
    return 1-prod


def calcexp(ages, prob, flag):
    i = 0
    for interval in (10, 1, 0.1, 0.01):
        probs = 0
        while(probs < prob):
            i += interval
            if flag == 0:
                probs = proballdie(ages, i)
            else:
                probs = probanydie(ages, i)
        i -= interval
    return i

ages = []
# print sys.argv[1:]
for arg in sys.argv[1:]:
    gender = 1
    years = 1.0
    if arg[-1] == 'm' or arg[-1] == 'M':
        try:
            ages.append(1*float(arg[:-1]))
        except:
            print "Error parsing argument", arg
    elif arg[-1] == 'f' or arg[-1] == 'F':
        try:
            ages.append(-1*float(arg[:-1]))
        except:
            print "Error parsing argument", arg
    else:
        try:
            years = float(arg)
            break
        except:
            print "Error parsing argument", arg

if not sys.argv[1:]:
    print "The format is 'actuary.py 15m 80f 23', with a list of ages and a number\
           of years to run the projections."
    raise SystemExit
if not ages:
    print "No ages specified.  Format is 12m, 17f, etc."
    raise SystemExit

# print "Ages:", ages
# print "Years:", years

(datetime.date.today()+datetime.timedelta(days=365.242191*1)).year
someone_years = [calcexp(ages, 0.05, 1),
                 calcexp(ages, 0.5, 1),
                 calcexp(ages, 0.95, 1)]
someone_dates = [(datetime.date.today()+datetime.timedelta(
                    days=365.242191*someone_years[0])).year,
                 (datetime.date.today()+datetime.timedelta(
                    days=365.242191*someone_years[1])).year,
                 (datetime.date.today()+datetime.timedelta(
                    days=365.242191*someone_years[2])).year]
print("There is a 5%  chance of someone dying within", someone_years[0],
      "years (by", str(someone_dates[0])+").")
print("There is a 50% chance of someone dying within", someone_years[1],
      "years (by", str(someone_dates[1])+").")
print("There is a 95% chance of someone dying within", someone_years[2],
      "years (by", str(someone_dates[2])+").")
print("")

if len(ages) > 1:
    everyone_years = [calcexp(ages, 0.05, 0),
                      calcexp(ages, 0.5, 0),
                      calcexp(ages, 0.95, 0)]
    everyone_dates = [(datetime.date.today()+datetime.timedelta(
                        days=365.242191*everyone_years[0])).year,
                      (datetime.date.today()+datetime.timedelta(
                        days=365.242191*everyone_years[1])).year,
                      (datetime.date.today()+datetime.timedelta(
                        days=365.242191*everyone_years[2])).year]
    print("There is a 5%  chance of everyone dying within", everyone_years[0],
          "years (by", str(everyone_dates[0])+").")
    print("There is a 50% chance of everyone dying within", everyone_years[1],
          "years (by", str(everyone_dates[1])+").")
    print("There is a 95% chance of everyone dying within", everyone_years[2],
          "years (by", str(everyone_dates[2])+").")


if years:
    yearword = "years"
    if years == 1:
        yearword = "year"

    print ""
    if years > datetime.date.today().year:
        years = years-datetime.date.today().year
    if len(ages) > 1:
        p = 100*proballdie(ages, years)
        printable = ""
        if p < 0.001:
            printable = "<0.001"
        elif p > 99.99:
            printable = ">99.99"
        else:
            printable = str(p)[:5]
        print("Probability of all dying in",
              years, yearword+":  ", printable+"%")
    p = 100*probanydie(ages, years)
    printable = ""
    if p < 0.001:
        printable = "<0.001"
    elif p > 99.99:
        printable = ">99.99"
        print(p)
    else:
        printable = str(p)[:5]
    print("Probability of a death within", years, yearword+":", printable+"%")
raise SystemExit
