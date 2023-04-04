import matplotlib.pyplot as plt
from nba_timeframe import NBATimeFrame
import df_cleanup
import numpy as np
import os
import matplotlib.ticker as mtick
from pandas.plotting import scatter_matrix


def get_eras_objects():
    nba_eras = {"1979-84": ["1979-80", "1983-84"], "1984-89": ["1984-85", "1988-89"],
                "1989-94": ["1989-90", "1993-94"], "1994-99": ["1994-95", "1998-99"],
                "1999-04": ["1999-00", "2003-04"], "2004-09": ["2004-05", "2008-09"],
                "2009-14": ["2009-10", "2013-14"], "2014-19": ["2014-05", "2018-19"],
                "2019-23": ["2019-20", "2022-23"]}
    
    nba_df = df_cleanup.get_df()
    df_cleanup.print_cleanedup_df(nba_df)
    nba_timeframe_objects = {}
    
    for era, years in nba_eras.items():
        start_year, end_year = years
        nba_timeframe_objects[era] = NBATimeFrame(nba_df, start_year, end_year)
        
    return nba_timeframe_objects
__timeframe_objects = get_eras_objects()

def plot_scatter_chart(ax, cmap, x_value, y_value, labels, title=None, xlabel=None, ylabel=None):
    color = cmap(np.arange(len(labels)))
    ax.scatter(x_value, y_value, c=color)
    
    for x, y, label in zip(x_value, y_value, labels):
        ax.annotate(label, (x, y))
        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
        
def plot_bar_chart(ax, data_dict, timef, colors, bar_width, legend_loc=None, title=None, ylabel=None,box_to_anchor=None):
    bar_dist = -bar_width
    
    for index, (label, data_arr) in enumerate(data_dict.items()):
        ax.bar(np.arange(len(timef)) + bar_dist, data_arr, width=bar_width, label=label, color = colors[index])
        bar_dist += bar_width

        for i, v in enumerate(data_arr):
            ax.annotate(str(v), xy=(i + (bar_dist-0.1) - bar_width/2, v), ha='center', va='bottom')
        
    ax.set_xticks(np.arange(len(timef)))
    ax.set_xticklabels(timef)
    ax.legend(bbox_to_anchor= box_to_anchor,loc=legend_loc)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

def plot_line_chart(ax, data_dict, timef, marker=None, title=None, ylabel=None, format_str="{}"):
    for label, stat in data_dict.items():
        ax.plot(timef, stat, label = label, marker=marker)

        for x, y in zip(timef, stat):
            ax.text(x, y, format_str.format(y), ha='center', va='bottom')

        ax.legend()
        ax.set_ylabel(ylabel)
        ax.set_title(title)

    
def plot_sizes_relationship(save=False):
    avg_heights = np.array([])
    avg_weights = np.array([])
    labels = np.array([])
   
    for timeframe, timeframe_obj in __timeframe_objects.items():
        build_stats = timeframe_obj.get_build_stats_avg()
        avg_heights = np.append(avg_heights, build_stats["height_avg"])
        avg_weights = np.append(avg_weights, build_stats["weight_avg"])
        labels = np.append(labels, timeframe) 
    
    fig, ax = plt.subplots(figsize=(16, 8))
    cmap = plt.get_cmap('Paired')
    plot_scatter_chart(ax, cmap, avg_weights, avg_heights, labels, title="Average height(mm) and weight(kg) relationship per timeframe", xlabel="Weight", ylabel="Height")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if save:
        plt.savefig("Size_relationship.png")
    else:
        print("Shows the change in height and weight overtime, very minimal change in height, a bit of change in weight.")
        plt.show()
  
def plot_shot_attempts(save=False):
    avg_fga = np.array([])
    avg_fta = np.array([])
    avg_3pta = np.array([])
    avg_fgm = np.array([])
    avg_ftm = np.array([])
    avg_3ptm = np.array([])
    timef = np.array([])
    colors_arr = ("#6929c4", "#1192e8", "#005d5d")
    
    for timeframe, timeframe_obj in __timeframe_objects.items():

        shot_makes_stats = timeframe_obj.get_shots_made_avg()
        timef = np.append(timef, timeframe)
        
        avg_fga = np.append(avg_fga, timeframe_obj.get_fga_avg())
        avg_fta = np.append(avg_fta, timeframe_obj.get_3pa_avg())
        avg_3pta = np.append(avg_3pta, timeframe_obj.get_fta_avg())
        
        avg_fgm = np.append(avg_fgm, shot_makes_stats["fgm_avg"])
        avg_ftm = np.append(avg_ftm, shot_makes_stats["ftm_avg"])
        avg_3ptm = np.append(avg_3ptm, shot_makes_stats["pt3m_avg"])
    attempts_dict = {"FT": avg_fta, "3P": avg_3pta, "FG": avg_fga}
    makes_dict = {"FT": avg_ftm, "3P": avg_3ptm, "FG": avg_fgm}  
    
    fig, axs = plt.subplots(1, 2, figsize=(18, 10))
    plot_bar_chart(axs[0], makes_dict, timef, colors_arr, bar_width=0.25, legend_loc="upper center", title="Shots made averages per timeframe", ylabel="Shot makes")
    plot_bar_chart(axs[1], attempts_dict, timef, colors_arr, bar_width=0.25, legend_loc= "upper center", title="Shot attempt averages per timeframe", ylabel="Shot attempts")
    fig.suptitle("Comparison of shot attempt and makes averages between different timeframes")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if save:
        plt.savefig("Shot_attempts_vs_makes.png")
    else:
        print("Comparison of makes and attempts between each timeframe.")
        plt.show()

def plot_3point_differences(save=False):
    avg_fga = np.array([])
    avg_fta = np.array([])
    avg_3pta = np.array([])
    timef= np.array([])
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        
        avg_fga = np.append(avg_fga, timeframe_obj.get_fga_avg())
        avg_fta = np.append(avg_fta, timeframe_obj.get_3pa_avg())
        avg_3pta = np.append(avg_3pta, timeframe_obj.get_fta_avg())
        timef = np.append(timef, timeframe)
    
    fig, axs = plt.subplots(1, 2, figsize=(18, 10))

    cmap = plt.get_cmap('Paired')
    plot_scatter_chart(axs[0], cmap, avg_3pta, avg_fga, timef, title="Relationship between field goal attempts and 3PT attempts", ylabel="All shot attempts", xlabel="Only 3 point shot attempts")
    plot_line_chart(axs[1], {"FT": avg_fta, "3P": avg_3pta}, timef, marker="o", title= "Change over time in 3PT and FT attempts", ylabel="Shot attempts")
    fig.suptitle("3 point attempt increase overtime")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    if save:
        plt.savefig("3PT_differences.png")
    else:
        print("These graphs show the rise in 3 Point shot attempts over spans of 5 years. Also decrease in FT attempts since more outside shots taken means less 2 point shots.")
        plt.show()

def plot_defensive_stats(save=False):
    blk_avg = np.array([])
    stl_avg = np.array([])
    pf_avg = np.array([])
    drb_avg = np.array([])
    timef = np.array([])
    colors = ("#6929c4", "#1192e8", "#005d5d", "#9f1853")
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        defensive_stats = timeframe_obj.get_defensive_stats_avg()
        blk_avg = np.append(blk_avg, defensive_stats["blk_avg"])
        stl_avg = np.append(stl_avg, defensive_stats["stl_avg"])
        pf_avg = np.append(pf_avg, defensive_stats["pf_avg"])
        drb_avg = np.append(drb_avg, defensive_stats["drb_avg"])
        timef = np.append(timef, timeframe)
        
    def_stats_dict = {"Fouls": pf_avg, "Blocks": blk_avg, "Steals": stl_avg, "Defensive rebounds": drb_avg} 
    fig, ax = plt.subplots(figsize=(15, 8))
    plot_bar_chart(ax, def_stats_dict, timef, colors, bar_width=0.2, title="Defensive stat averages for different timeframes", ylabel="Amounts")
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if save:
        plt.savefig("Defensive_stats.png")
    else:
        print("Steals numbers are pretty much the same. Blocks and fouls decrease since players shoot more threes. Defensive rebounds see an increase due to less opposing players underneath the basket.")
        plt.show()
   
def plot_fg_proc(save=False):
    fg_avg = np.array([])
    pt3_avg = np.array([])
    ft_avg = np.array([])
    efg_avg = np.array([])
    timef = np.array([])
    colors = ("#8B008B", "#2E8B57", "#FFD700", "#FFA500")
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        shootin_proc = timeframe_obj.get_shooting_proc_avg()
        fg_avg = np.append(fg_avg, shootin_proc["fg_avg"])
        pt3_avg = np.append(pt3_avg, shootin_proc["pt3_avg"])
        ft_avg = np.append(ft_avg, shootin_proc["ft_avg"])
        efg_avg = np.append(efg_avg, shootin_proc["efg_avg"])
        timef = np.append(timef, timeframe) 
    fg_dict = {"FT%": ft_avg, "FG%": fg_avg, "3P%": pt3_avg, "EFG%": efg_avg}
    
    fig, ax = plt.subplots(figsize=(18, 10))
    plot_line_chart(ax, fg_dict, timef, marker="o", title="FG% change over time", ylabel="Percentages", format_str="{:.1f}%")
    yticks = mtick.FuncFormatter(lambda y, _: '%.0f%%' % y )
    ax.yaxis.set_major_formatter(yticks)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if save:
        plt.savefig("FGproc.png")
    else:
        print("EFG stands for FG + (0.5*3P) / FGA. Its goal is to show what field goal percentage a two-point shooter would have to shoot at to match the output of a player who also shoots three-pointers.")
        print("Shows change over time in different field goal%. The most notable change is how efficiently teams shoot the three point basket. Also, due to the three point shot, EFG% gets steadily higher over time.")
        plt.show()
    
def plot_tov_to_assist_pace_relationship(save=False):
    apg_avg = np.array([])
    tov_avg = np.array([])
    timef = np.array([])
    pace = np.array([])
    colors = ("#8B008B", "#2E8B57")
    
    
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        assist_tov_avg = timeframe_obj.get_tov_and_assist_avgs()
        
        apg_avg = np.append(apg_avg, assist_tov_avg["ast_avg"])
        tov_avg = np.append(tov_avg, assist_tov_avg["tov_avg"])
        pace = np.append(pace, timeframe_obj.get_pace_avg())
        timef = np.append(timef, timeframe) 
    
    fig = plt.figure(figsize=(18,10))
    ax = plt.axes(projection="3d")
    timef_map = {v: i for i, v in enumerate(np.unique(timef))}
    colors = ["#8B008B", "#2E8B57", "#FFD700", "#FFA500", "#FF1493", "#00BFFF", "#FFC0CB", "#8A2BE2", "#87CEFA"]

    # Create scatter plot
    for i, t in enumerate(timef):
        ax.text(tov_avg[i], apg_avg[i], pace[i], t, fontsize=15)
        ax.scatter(tov_avg[i], apg_avg[i], pace[i], s=100, c=colors[timef_map[t]])
        
    ax.set_xlabel("Turnovers per game")
    ax.set_ylabel("Assists per game")
    ax.set_zlabel('Pace')
    plt.title('Relationship between pace, assists and turnovers')

    os.system('cls' if os.name == 'nt' else 'clear')
    
    if save:
        plt.savefig("Pace_assists_to_turnovers.png")
    else:
        print("Shows the relationship between assist and turnover averages and if pace has anything to do with it. The later eras have a big increase in pace, assist the ball at almost the same clip while committing less turnovers")
        plt.show()
    
def plot_points(save=False):
    ppg_avg = np.array([])
    timef = np.array([])
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        ppg_avg = np.append(ppg_avg, timeframe_obj.get_pts_avg())
        timef = np.append(timef, timeframe)
        
    fix, ax = plt.subplots(figsize=(16,8)) 
    plot_line_chart(ax, {"PPG": ppg_avg}, timef, marker="o", title="PPG change overtime", ylabel="PPG")
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if save:
        plt.savefig("Points_overtime.png")
    else:
        print("Shows points over time. Huge increase from the 90s-00s.")
        plt.show()
    
def plot_ortg_orb_relationship(save=False):
    ortg_avg = np.array([])
    orb_avg = np.array([])
    avg_3pt = np.array([])
    timef = np.array([])
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        ortg_avg = np.append(ortg_avg, timeframe_obj.get_ort_avg())
        orb_avg = np.append(orb_avg, timeframe_obj.get_orb_avg())
        avg_3pt = np.append(avg_3pt, timeframe_obj.get_3pa_avg())
        timef = np.append(timef, timeframe)
        
    fig, axs = plt.subplots(1, 2,figsize=(16, 8))
    cmap = plt.get_cmap('Paired')
    plot_scatter_chart(axs[0], cmap, orb_avg, ortg_avg, timef, xlabel="Offensive Rebound", ylabel="Offensive rating")    
    plot_line_chart(axs[1], {"3PA": avg_3pt, "ORB": orb_avg}, timef, marker="o")
    fig.suptitle("Relationship whether Offensive rebounds amount to more points")
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if save:
        plt.savefig("Offensive_rebound_prevalence.png")
    else:
        print("Offensive rating = points per 100 possesions. In other words, if only 100 possessions were in a game, how much, in this case a timeframe, would score.")
        print("Offensive rebounds dropped even though points per 100 possessions went up. More 3 point shot attempts means teams have to get back on defense and not gamble for rebounds, also the 3 points make up for less second chance points.")
        plt.show()
 
def plot_ortg_relationship(save=False):
    pace = np.array([])
    tov_proc = np.array([])
    ortg = np.array([])
    timef = np.array([])
    
    for timeframe, timeframe_obj in __timeframe_objects.items():
        
        pace = np.append(pace, timeframe_obj.get_pace_avg())
        tov_proc = np.append(tov_proc, timeframe_obj.get_tovproc_avg())
        ortg = np.append(ortg, timeframe_obj.get_ort_avg())
        timef = np.append(timef, timeframe)
        
    fig = plt.figure(figsize=(18,10))
    ax = plt.axes(projection="3d")
    timef_map = {v: i for i, v in enumerate(np.unique(timef))}
    colors = ["#8B008B", "#2E8B57", "#FFD700", "#FFA500", "#FF1493", "#00BFFF", "#FFC0CB", "#8A2BE2", "#87CEFA"]

    # Create scatter plot
    for i, t in enumerate(timef):
        ax.text(pace[i], tov_proc[i], ortg[i], t, fontsize=15)
        ax.scatter(pace[i], tov_proc[i], ortg[i], s=100, c=colors[timef_map[t]])
        
    ax.set_xlabel("Pace")
    ax.set_ylabel("Turnover%")
    ax.set_zlabel('Offensive rating')
    plt.title('Offensive rating relationship with Pace and Turnover%')
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if save:
        plt.savefig("Offensive_rating_relationship(Pace, Tov%).png")
    else:
        print("Offensive rating = points per 100 possesions. In other words, if only 100 possessions were in a game, how much, in this case a timeframe, would score.")
        print("As time goes on, teams increase their pace of play, score more per 100 possesions and lessen the turnover rate.")
        plt.show()

                 
def return_plots():
    return {"1": plot_points, "2": plot_shot_attempts, "3": plot_3point_differences,
            "4": plot_fg_proc, "5": plot_tov_to_assist_pace_relationship, "6": plot_ortg_orb_relationship,
            "7": plot_ortg_relationship, "8": plot_defensive_stats, "9": plot_sizes_relationship}

