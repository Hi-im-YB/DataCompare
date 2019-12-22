import pandas as pd

#Company Specifier -> Company YrsExperience c [0-2, 3-5, 6-10, 11-15, 16+]
#Company -> Company YrsCompany
#Company YrsExperience = min -> max Company YrsExperience : YrsCompany = [0-2] && [3-5] && [6-10] && [11-15] && [16+]
#YrsCompany, Company are the same length - data with equal row numbers for each column

#group age slices [N group * M age set]
FIRST_GROUP = [0.0, 1.0, 2.0]
SECOND_GROUP = [3.0, 4.0, 5.0]
THIRD_GROUP = [6.0, 7.0, 8.0, 9.0, 10.0]
FOURTH_GROUP = [11.0, 12.0, 13.0, 14.0, 15.0]
SIXTH_GROUP = [16.0]

#group sets
YEARS_SLICE = {'FIRST_GROUP' : FIRST_GROUP,
               'SECOND_GROUP': SECOND_GROUP,
               'THIRD_GROUP' : THIRD_GROUP,
               'FOURTH_GROUP': FOURTH_GROUP,
               'SIXTH_GROUP' : SIXTH_GROUP}

#exist data file
INPUT_DATA_PATH = '../common/data.csv'
input_file = pd.read_csv(INPUT_DATA_PATH)

def is_year_in_years_slice(company_age):
    #by default return 1 st group if None age bound/...
    actual_group = 'FIRST_GROUP'
    for group_data in YEARS_SLICE.items():
        #print('current year = ', group_data, ' for group: ', group_data[0], company_age)
        for group_age in group_data[1]:
            if company_age == group_age:
                #print('In bounds, minimum age for group: ', group_data[0])
                actual_group = group_data[0]
    return actual_group

def pdf(_input_file):
    return pd.DataFrame(_input_file)

def column_index(file, _column):
    df = pd.DataFrame(file)
    return df.columns.get_loc(_column)

def column_data_by_index(file, _index):
    df = pd.DataFrame(file)
    return df.iloc[:, _index]

def column_data_by_name(input_file, column_name):
    return column_data_by_index(input_file,
                                    column_index(input_file, column_name))

def column_value_by_row(df, column_value, row_value):
    return df.loc[df[column_value] == row_value]


#filter by unique rows
def filter_by_unique_rows(company_profile):
    print("Unfiltered companies & ages length: ", len(company_profile['YrsExperience']))
    company_profile_filtered = list()
    for company_info in zip(company_profile['Company'], company_profile['YrsExperience']):
        company_profile_filtered.append(company_info)
    return list(set(company_profile_filtered))


#make list of tuples with [(Company, Age1, Age2, ..., AgeN)]
def filter_by_age_and_name(company_profile_filtered):
    company_ages_by_names_raw = {}
    print("Filtered companies & ages length: ", len(company_profile_filtered))
    company_ages_by_names_raw = {}
    for c_name, c_age in company_profile_filtered:
        company_ages_by_names_raw.setdefault(c_name, [c_name]).append(c_age)
    return list(map(tuple, company_ages_by_names_raw.values()))


#find minimum company age and search if that value in group ages slice
def company_min_age_subset(company_ages_by_names):
    print("Filtered companies by ages length: ", len(company_ages_by_names))
    result = list()
    for c_info in company_ages_by_names:
        #print('company name', company_info[0], 'ages: ', company_info[1:-1])
        min_company_age = 0.0
        try:
            min_company_age = min(c_info[1:-1])
        except ValueError:
            #print('Company have not age bounds, suppose that necessary experience is 0 years')
            pass
        result.append((c_info[0], c_info[1:-1], is_year_in_years_slice(min_company_age)))
        #print('minimum age: ', min_company_age)
        #print('ages slice: ', is_year_in_years_slice(min_company_age))
    return result


#check if company
#years experience factor in all groups (shift minimum age)
def company_get_all_age_subsets(company_data_result):
    result = list()
    for c_info in company_data_result:
        # print('company name', c_info[0])
        ages_slice = c_info[1:-1]
        company_ages = list(map(list, (ages_slice)))[0]
        # print('company ages: ', company_ages)
        ages_entries = list()
        for c_age in company_ages:
            # print("current company age for comparing: ", c_age)
            ages_group = is_year_in_years_slice(c_age)
            # print(ages_group)
            ages_entries.append(is_year_in_years_slice(c_age))
        # stay only unique entries of companies age entries
        ages_entries = list(set(ages_entries))
        # save results of searching
        result.append((c_info[0], ages_slice, ages_entries))
    return result


#for each Company find years experience factor
#that by we have all age groups etries
def company_get_all_age_etries(company_ages):
    result_entries = list()
    for c_info in company_ages:
        ages_entries = 0
        for c_group in c_info[2]:
            for g_group in YEARS_SLICE.keys():
                #print('company = ', c_info[0], ' company group = ', c_group, ' bound group age = ', g_group)
                if c_group == g_group:
                    ages_entries += 1
            if ages_entries == len(YEARS_SLICE.keys()):
                #print('company age entries: ', ages_entries)
                result_entries.append((c_info[0], c_info[1:-1][0][0], c_info[2]))
    return result_entries


# get actual company info from data source
company_name = column_data_by_name(input_file, 'Company')
company_experience = column_data_by_name(input_file, 'YrsExperience')
company_profile = {}
company_profile['Company'] = company_name
company_profile['YrsExperience'] = company_experience
company_total = column_data_by_name(input_file, 'TotalValue')
company_profile['TotalValue'] = company_total

# filter and process data by steps
company_profile_filtered = filter_by_unique_rows(company_profile)
company_ages_by_names = filter_by_age_and_name(company_profile_filtered)
company_data_result = company_min_age_subset(company_ages_by_names)
company_ages = company_get_all_age_subsets(company_data_result)
company_all_entries = company_get_all_age_etries(company_ages)

#companies with age bounds entries
print('\nCOMPANIES WITH BOUND AGES ENTRIES:\n')
for company_info in company_ages:
    print(company_info)

print('\nCOMPANIES WITH ALL AGES ENTRIES:\n')
for company_info in company_all_entries:
    print(company_info)


#calculate product factors for each Company
#to "establish" maximum equality of all years of experience subsets for each Company

#1. 1 find totalvalues for all companies rows and calculate local average
df_company_data = list()
for c_info in zip(company_profile['Company'], company_profile['TotalValue']):
    #print(c_info)
    try:
        df_company_data.append([c_info[0], float(c_info[1].replace(',', '.'))])
    except:
        #lose some data because of str totalvalue to float
        pass

#1. 2 find mean TotalValue for each Company
dfc = pd.DataFrame(df_company_data, columns = ['Company', 'TotalValue'])
dfc_total_means = dfc.groupby('Company', as_index=False)['TotalValue'].mean()

company_all = list()
for c_info in company_all_entries:
    #print(c_info)
    try:
        mean_total = column_value_by_row(dfc_total_means, 'Company', c_info[0]).iloc[0, 1]
        #print(mean_total)
        company_all.append((c_info[0], c_info[1:-1][0], c_info[2], mean_total))
    except:
        # lose some data if no mean value of TotalValue for current company
        pass

print('\nCOMPANIES WITH ALL AGES ENTRIES AND TotalValue MEANS AND MAX\'S:\n')
for c_info in company_all:
    print(c_info)

#1. 3 suppose that desirable product value is:
#K_company_i = 1/<K>*A_i
average_mean = 0.0

for c_item in company_all:
    average_mean += c_item[-1]
average_mean = average_mean/len(company_all)

print('\nAVERAGE MEAN TOTAL VALUE OF ALL UNIQUE COMPANIES WITH ALL AGES ENTRIES: ', average_mean)

#2.1 for all companies with age bound = 1 and less than 5
#save total value
company_minage_bound = list()
for company_info in company_ages:
    try:
        mean_total = column_value_by_row(dfc_total_means, 'Company', company_info[0]).iloc[0, 1]
        #print(mean_total)
        company_minage_bound.append((company_info[0], company_info[1:-1][0], company_info[2], mean_total))
    except:
        # lose some data if no mean value of TotalValue for current company
        pass

print('\nAVERAGE TOTAL VALUE FOR COMPANIES WITH ONE MINIMUM AGE BOUND:\n')
for c_info in company_minage_bound:
    print(c_info)

#2.2 for each that company product them current totalvalue
#with k = (maxmean - mean)/2 of company with all age entries
compnay_updated_totals = list()
for c_info_once in company_minage_bound:
        #print(c_info_once[0])
        if c_info_once[-1] < average_mean:
            booster = average_mean/c_info_once[-1] #minimum bound value when totalvalue stay equal average
            boosted_total = booster*c_info_once[-1]
            #print('totalvalue must be producted = ', c_info_once[-1], ' on: ', booster, ' boosted totalvalue: ', boosted_total)
            compnay_updated_totals.append((c_info_once[0],
                                           c_info_once[1:-1][0],
                                           c_info_once[2],
                                           {"multiplier": round(booster, 2),
                                            "boosted_total": round(boosted_total, 2)}))
        else:
            #print('once company totalvalue = ', c_info_once[-1])
            compnay_updated_totals.append((c_info_once[0],
                                           c_info_once[1:-1][0],
                                           c_info_once[2],
                                           {"multiplier": 1.0,
                                            "boosted_total": round(c_info_once[-1], 2)}))

print('\nBOOSTED TOTAL VALUE FOR COMPANIES WITH ONE MINIMUM AGE BOUND:\n')
for company_data in compnay_updated_totals:
    print(company_data)