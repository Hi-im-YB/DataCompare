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

#group age slices [N group * M age set]
FIRST_GROUP = [0.0, 1.0, 2.0]
SECOND_GROUP = [3.0, 4.0, 5.0]
THIRD_GROUP = [6.0, 7.0, 8.0, 9.0, 10.0]
FOURTH_GROUP = [11.0, 12.0, 13.0, 14.0, 15.0]
SIXTH_GROUP = [16.0]

#group sets
YEARS_SLICE = {1 : FIRST_GROUP,
               1.15: SECOND_GROUP,
               1.35 : THIRD_GROUP,
               1.55: FOURTH_GROUP,
               1.75 : SIXTH_GROUP}

#exist data file
INPUT_DATA_PATH = '../common/data.csv'
input_file = pd.read_csv(INPUT_DATA_PATH)


def is_year_in_years_slice(company_age):
    #by default return 1 st group if None age bound/...
    actual_group = 1.00
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
    for company_info in zip(company_profile['Company'], company_profile['YrsExperience'], company_profile['Title']):
        company_profile_filtered.append(company_info)
    return list(set(company_profile_filtered))


#make list of tuples with [(Company, Age1, Age2, ..., AgeN)]
def filter_by_age_and_name(company_profile_filtered):
    company_ages_by_names_raw = {}
    print("Filtered companies & ages length: ", len(company_profile_filtered))
    company_ages_by_names_raw = {}
    for c_name, c_age, c_title in company_profile_filtered:
        company_ages_by_names_raw.setdefault(c_name, [c_name]).append((c_age, c_title, ))
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

# get actual company info from data source
company_name = column_data_by_name(input_file, 'Company')
company_experience = column_data_by_name(input_file, 'YrsExperience')
company_profile = {}
company_profile['Company'] = company_name
company_profile['YrsExperience'] = company_experience
company_profile['Title'] = column_data_by_name(input_file, 'Title')
company_total = column_data_by_name(input_file, 'TotalValue')
company_profile['TotalValue'] = company_total

# filter and process data by steps
company_profile_filtered = filter_by_unique_rows(company_profile)
company_ages_by_names = filter_by_age_and_name(company_profile_filtered)
company_data_result = company_min_age_subset(company_ages_by_names)

#companies with age bounds entries
print('\nCOMPANIES SET DIM: ', len(company_data_result))
print('\nCOMPANIES ENTRIES:\n')
for company_info in company_data_result:
    print(company_info)

#For each company have the next connection: Company -> Title = Base = AnnualBonus -> YrsExperience
#Save YrsExperience factor for each current Company -> Title/Base/AnnualBonus
#For each saved Company -> Title/Base/AnnualBonus calculate