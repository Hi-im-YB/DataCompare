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
#Company |YrsExp | YrsFactor|CompanyN_YrsFactor/Compnay_YrsFactor_1 |

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


# find intersection between experience factor
# and current company experience years
def is_year_in_years_slice(company_age):
    years_groups = list()
    DEFAULT_GROUP_FACTOR = 1.0
    #for each experience group
    for exp_set in EXPERIENCE_SET.items():
        #print('current experience data = ', exp_set, ' for company current experience value: ', company_age)
        #for each group factor save company factor
        #if it's experience year in one of the fifth group
        if company_age == 'nan':
            years_groups.append([DEFAULT_GROUP_FACTOR])
        if float(company_age) >= float(exp_set[1][0]) and \
            float(company_age) <= float(exp_set[1][-1]):
            #print('In bounds, minimum age for group: ', group_data[0])
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
    return list(set(years_groups))


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
    #print("Filtered companies by ages length: ", len(company_ages_by_names))
    result = list()
    for c_info in company_ages_by_names:
        #print('company name', c_info[0], 'ages: ', c_info[1:-1])
        for c_age in c_info[1:-1]:
            result.append((c_info[0], c_info[1:-1], is_year_in_years_slice(c_age)))
            #print('ages slice: ', is_year_in_years_slice(c_age))
    return result


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

#companies with all experience years
print('\nCOMPANIES SET DIM: ', len(company_data_result))
print('\nCOMPANIES ENTRIES WITH ALL EXPERIENCE YEARS:\n')

company_all_ages_filtered = list()
for tup in company_data_result:
    if tup not in company_all_ages_filtered:
        company_all_ages_filtered.append(tup)

for company_info in company_all_ages_filtered:
    print(company_info)

#For each company have the next connection: Company -> Title = Base = AnnualBonus -> YrsExperience
#Save average YrsExperience factor for each current Company
#For each saved Company average YrsExperience calculate nearest experience factor
#For each saved Company average YrsExperience calculate ratio between current Company experience factor and other N companies experience factor