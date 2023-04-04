import pandas as pd

class NBATimeFrame:
    
    def __init__(self, nba_df, start_year, end_year):
        self.__nba_timeframea_df = nba_df.loc[(nba_df["Season"] >= start_year) & (nba_df["Season"] <= end_year)]

    def get_defensive_stats_avg(self):
        blk_avg = round(self.__nba_timeframea_df["BLK"].mean(), 1)
        stl_avg = round(self.__nba_timeframea_df["STL"].mean(), 1)
        pf_avg = round(self.__nba_timeframea_df["PF"].mean(), 1)
        drb_avg = round(self.__nba_timeframea_df["DRB"].mean(), 1)
        
        return {"blk_avg": blk_avg, "stl_avg": stl_avg, "pf_avg": pf_avg, "drb_avg": drb_avg}
        
    def get_tov_and_assist_avgs(self):
        tov_avg = round(self.__nba_timeframea_df["TOV"].mean(), 1)
        ast_avg = round(self.__nba_timeframea_df["AST"].mean(), 1)

        return {"tov_avg": tov_avg, "ast_avg": ast_avg}

    def get_pace_avg(self):
        return round(self.__nba_timeframea_df["Pace"].mean(), 1)
    
    def get_tovproc_avg(self):
        return round(self.__nba_timeframea_df["TOV%"].mean(), 1)
    
    def get_pts_avg(self):
        return round(self.__nba_timeframea_df["PTS"].mean(), 1)
    
    def get_orb_avg(self):
        return round(self.__nba_timeframea_df["ORB"].mean(), 1)
    
    def get_ort_avg(self):
        return round(self.__nba_timeframea_df["ORtg"].mean(), 1)
  
   
    def get_build_stats_avg(self):
        height_avg = round(self.__nba_timeframea_df["Ht"].mean(),2)
        weight_avg = round(self.__nba_timeframea_df["Wt"].mean(),1)
        
        return {"height_avg": height_avg, "weight_avg": weight_avg}
        
    
    def get_shooting_proc_avg(self):
        fg_avg = round(self.__nba_timeframea_df["FG%"].mean(), 1)
        pt3_avg = round(self.__nba_timeframea_df["3P%"].mean(), 1)
        ft_avg = round(self.__nba_timeframea_df["FT%"].mean(), 1)
        efg_avg = round(self.__nba_timeframea_df["eFG%"].mean(), 1)
        
        return {"fg_avg": fg_avg, "pt3_avg": pt3_avg, "ft_avg": ft_avg, "efg_avg": efg_avg}
    
    def get_fga_avg(self):
        return round(self.__nba_timeframea_df["FGA"].mean(), 1)
    
    def get_3pa_avg(self):
        return round(self.__nba_timeframea_df["3PA"].mean(), 1)
    
    def get_fta_avg(self):
        return round(self.__nba_timeframea_df["FTA"].mean() ,1)
    
    def get_shots_made_avg(self):
        fgm_avg = round(self.__nba_timeframea_df["FG"].mean(), 1)
        pt3m_avg = round(self.__nba_timeframea_df["3P"].mean() ,1)
        ftm_avg = round(self.__nba_timeframea_df["FT"].mean(), 1)
        
        return {"fgm_avg": fgm_avg, "pt3m_avg": pt3m_avg, "ftm_avg": ftm_avg}