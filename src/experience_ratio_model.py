import pandas as pd

#Company Specifier -> Company YrsExperience
# experience_factor = {
#
# "0 - 2": 1,
# "3 - 5": 1.15,
# "6 - 10": 1.35,
# "11 - 15": 1.55,
# "16 or more": 1.75
#
# }

#YrsExpCompanyN/YrsExpCompany1 - find density of YrsExperience value for each Company between all other Companies
#Company |YrsExp| YrsFactor|CompanyN_YrsFactor/Compnay_YrsFactor_1 |

#experience years slices [N group * M age set]
FIRST_GROUP = [0.0, 1.0, 2.0]
SECOND_GROUP = [3.0, 4.0, 5.0]
THIRD_GROUP = [6.0, 7.0, 8.0, 9.0, 10.0]
FOURTH_GROUP = [11.0, 12.0, 13.0, 14.0, 15.0]
SIXTH_GROUP = [16.0]

EXPERIENCE_SET = {1 : FIRST_GROUP,
               1.15: SECOND_GROUP,
               1.35 : THIRD_GROUP,
               1.55: FOURTH_GROUP,
               1.75 : SIXTH_GROUP}

#exist data file
INPUT_DATA_PATH = '../common/data.csv'
input_file = pd.read_csv(INPUT_DATA_PATH)


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

# find median in list
def median(input_list):
    dim = len(input_list)
    sorted_list = sorted(input_list)
    return round((sum(sorted_list[dim//2 - 1:dim // 2+1])/2.0, sorted_list[dim // 2])[dim % 2], 2) if dim else None

# find intersection between experience factor
# and current company experience years
def is_year_in_years_slice(company_ages):
    years_groups = list()
    # for the case when we have NAN value
    # assume that it is equals
    # to minimum factor = 1.0
    DEFAULT_GROUP_FACTOR = 1.0
    #for each company age
    for company_age in company_ages:
        #for each experience group ages slice
        for exp_set in EXPERIENCE_SET.items():
            #for each group factor save company factor
            #if it's experience year in one of the fifth group
            if company_age == 'nan':
                years_groups.append([DEFAULT_GROUP_FACTOR])
            if float(company_age) >= float(exp_set[1][0]) and \
                float(company_age) <= float(exp_set[1][-1]):
                actual_group = exp_set[0]
                years_groups.append(actual_group)
            elif float(company_age) > float(SIXTH_GROUP[0]):
                years_groups.append(sorted(EXPERIENCE_SET.keys())[-1])
            elif float(company_age + 0.5) == float(exp_set[1][0]) or \
                float(company_age + 0.5) == float(exp_set[1][-1]) or \
                float(company_age - 0.5) == float(exp_set[1][0]) or \
                float(company_age - 0.5) == float(exp_set[1][-1]):
                years_groups.append(exp_set[0])
    #print('common years: ', years_groups)
    #save sorted by ascending order
    #YrsExperience factor set for each current Company
    return sorted(list(set(years_groups)))


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
def get_factor_ages_intersection(company_ages_by_names):
    #print("Filtered companies by ages length: ", len(company_ages_by_names))
    result = list()
    # Company, ages, [factor1, ..., factor N]
    # group by each category data
    for c_info in company_ages_by_names:
        #print('company name', c_info[0], 'ages: ', c_info[1:-1])
        result.append((c_info[0], c_info[1:-1], is_year_in_years_slice(c_info[1:-1])))
        #print('ages slice: ', is_year_in_years_slice(c_info[1:-1]))
    return result


# get actual company info from the data set source
company_name = column_data_by_name(input_file, 'Company')
company_experience = column_data_by_name(input_file, 'YrsExperience')
company_profile = {}
company_profile['Company'] = company_name
company_profile['YrsExperience'] = company_experience
company_total = column_data_by_name(input_file, 'TotalValue')
company_profile['TotalValue'] = company_total

#1. 1 find instersection between YrsExperience factor set
# and each Company YrsExperience values.
# For each company have the next connection:
# Company -> Title <-> Base <-> AnnualBonus -> YrsExperience
# filter and process data by steps and work with only YrsExperience
company_profile_filtered = filter_by_unique_rows(company_profile)
company_ages_by_names = filter_by_age_and_name(company_profile_filtered)
company_ages_factors_set = get_factor_ages_intersection(company_ages_by_names)

print('\nCOMPANIES SET DIM: ', len(company_ages_factors_set))
print('\nCOMPANIES ENTRIES WITH ALL EXPERIENCE YEARS:\n')
for company_info in company_ages_factors_set:
    print(company_info)

#1. 2 for each company experience factor set calculate mean experience factor
company_ages_factors_mean_set = list()
for company_info in company_ages_factors_set:
    company_ages_factors_mean_set.append((company_info[0], company_info[1],
                                          tuple(company_info[2]), median(company_info[2])))

print('\nCOMPANIES WITH MEAN FACTORS SET DIM: ', len(company_ages_factors_mean_set))
print('\nCOMPANIES ENTRIES WITH ALL EXPERIENCE YEARS INCLUDE FACTORS MEANS:\n')
for company_info in company_ages_factors_mean_set:
    print(company_info)

# 1. 3 calculate ratio of mean factors
# of years experience between all companies
processed_companies = list()
for company_orig in company_ages_factors_mean_set:
    for company_comp in company_ages_factors_mean_set:
        if company_orig[0] != company_comp[0]:
            if company_comp[3] and company_orig[3]:
                ratio_factor = round(company_orig[3]/company_comp[3], 2)
                processed_companies.append((company_orig[0], company_orig[1],
                                            company_orig[3],
                                            company_comp[0], company_comp[1],
                                            company_comp[3], ratio_factor))

print('\nPROCESSED COMPANIES WITH RATION FACTORS DIM: ', len(processed_companies))
print('\nPROCESSED COMPANIES WITH RATION FACTORS:\n')
#sort alphabetically processed data
processed_companies = list(sorted(processed_companies, key=lambda slice: slice[0]))
for company_info in processed_companies:
    print(company_info)

# transpose data
company_data_result = list(map(list, zip(*processed_companies)))
#save final result to pandas dataframe
df = pd.DataFrame(list(zip(company_data_result[0], company_data_result[1],
                           company_data_result[2], company_data_result[3],
                           company_data_result[4], company_data_result[5],
                           company_data_result[-1])),
               columns =['Company(i) (i != j)', 'YrsExperience(i)', 'YrsExperience\nmean factor (i)',
                         'Company(j) (i != j)', 'YrsExperience(j)', 'YrsExperience\nmean factor (j)',
                         'YrsExperience\nfactors ratio (i/j)'])
#save dataframe to output file
df.to_csv('companies_age_factors.csv', index=False, encoding='utf-8')
