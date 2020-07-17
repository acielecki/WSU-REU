import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class se:
    @staticmethod
    def get_file_to_check(data_frame):
        df_To_beMatched = data_frame[["commit.message"]]
        # print(df_To_beMatched.head())
        return(df_To_beMatched)

    @staticmethod
    def checker(wrong_options, correct_options):
        names_array = []
        ratio_array = []
        for wrong_option in wrong_options:
            if wrong_option in correct_options:
                names_array.append(wrong_option)
                ratio_array.append('100')
            else:
                x = process.extractOne(wrong_option, correct_options, scorer=fuzz.partial_ratio)
                names_array.append(x[0])
                ratio_array.append(x[1])
        return names_array, ratio_array
    
    @staticmethod
    def check_against_list(df_To_beMatched):
        df_Original_List = pd.read_fwf(
            '/Users/pandit_ji/Desktop/MS/ra/Collecting commit-yash(June 18)/Data/assessment.txt')
        df_Original_List.columns = ['CWE-ID']
        str2Match = df_To_beMatched['commit.message'].fillna('######').tolist()
        strOptions = df_Original_List['CWE-ID'].fillna('######').tolist()
        name_match, ratio_match = se.checker(str2Match, strOptions)
        dfm3 = pd.DataFrame()
        dfm = pd.DataFrame()
        dfm3['commit.message'] = pd.Series(str2Match)
        dfm3['security code'] = pd.Series(name_match)
        dfm3['correct_ratio'] = pd.Series(ratio_match)
        for ratio in (dfm3['correct_ratio']):
            dfm3=(dfm3[dfm3.correct_ratio>80])  
        return(dfm3)
    
    
    
    @staticmethod
    def check_for_Cwe(df_To_beMatched):
        df_Original_List = pd.read_csv(
                '/Users/pandit_ji/Desktop/MS/ra/Collecting commit-yash(June 18)/Data/699.csv')
        
        df_Original_List=df_Original_List[["CWE-ID"]]
#         print(df_Original_List)
        str2Match = df_To_beMatched['commit.message'].fillna('######').tolist()
        strOptions = df_Original_List['CWE-ID'].fillna('######').tolist()
        name_match, ratio_match = se.checker(str2Match, strOptions)
        dfm3 = pd.DataFrame()
        dfm = pd.DataFrame()
        dfm3['commit.message'] = pd.Series(str2Match)
        dfm3['security code'] = pd.Series(name_match)
        dfm3['correct_ratio'] = pd.Series(ratio_match)
        for ratio in (dfm3['correct_ratio']):
            dfm3=(dfm3[dfm3.correct_ratio>80])  
        return(dfm3)
    
    @staticmethod
    def write_to_csv(df):
        df.to_csv("SecCheck_"+id+".csv",mode="a")
    
df_To_beMatched=se.get_file_to_check(pd.read_csv("/Users/pandit_ji/Desktop/MS/ra/Collecting commit-yash(June 18)/Data/vue.csv"))
df_from_list=se.check_against_list(df_To_beMatched)
df_from_cwe=se.check_for_Cwe(df_To_beMatched)
