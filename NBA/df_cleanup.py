import pandas as pd
    
def get_df():
    try:
        nba_data_df = pd.read_csv("year_stats.csv", index_col = 0, header=[0,1])
    except Exception as e:
        print(f"An error occured: {e}")
        
    nba_data_df = nba_data_df.droplevel(0, axis=1)
    modern_nba_df = nba_data_df.loc[(nba_data_df["Season"] >= "1979-80")]
    
    def configure_height(height_str):   #configure the height since it gets converted into day-month from feet
        #also convert to mm.
        month_dict = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12}
        inch_str, feet_str = height_str.split("-")
        feet_str = month_dict[feet_str]
        return round((int(feet_str)*0.3048) + (int(inch_str)*0.0254),2) * 100
    
    
    def configure_weight(weight_str):   #Convert weight to kg
        return round(int(weight_str)*0.45359237,1)
      
    modern_nba_df["Ht"] = modern_nba_df["Ht"].apply(lambda x: configure_height(x))
    modern_nba_df["Wt"] = modern_nba_df["Wt"].apply(lambda x: configure_weight(x))
    
    modern_nba_df[["FG%", "eFG%", "FT%", "3P%"]] = modern_nba_df[["FG%", "eFG%", "FT%", "3P%"]] * 100
    modern_nba_df = modern_nba_df.drop(["ORB%","FT/FGA","G","Lg", "MP", "Age", "TRB"], axis=1)
    
    return modern_nba_df
      
def print_cleanedup_df(df):
    with pd.ExcelWriter('Cleaned_nba.xlsx') as writer:
        df.to_excel(writer, index=False)



    

