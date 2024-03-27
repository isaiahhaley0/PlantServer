import Services.DBHandler as DB
import Services.Stats as Stats

def pct_diff(final, inital):
    top = final-inital
    bottom = (final+inital)/2
    total = (top/bottom)*100
    return total

def should_flash():
    mh = DB.DBHandler()
    current = mh.get_last()['light']
    hl = Stats.get_min_max()
    pct = pct_diff(hl[1],current)
    if pct < 10:
       return True
    else:
        return False