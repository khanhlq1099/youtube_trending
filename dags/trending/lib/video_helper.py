import re

def type_helper(type:str):

    if type == "SHORTS": return type
    else: return "VIDEO"

def date_helper(date:str):
    if "Streamed" in date:
        # date = date.removeprefix('Streamed ')
        date = date.replace('Streamed ','')
    
    if "weeks" in date:
        date = str(int(re.findall("\d+", date)[0]) * 7) + " days"

    # upload_date = date.removesuffix(' ago')
    upload_date = date.replace(' ago','')

    return upload_date

def views_helper(views:str):
    views = views.replace(' views','')
    temp = re.findall("\d+", views)
    if "M" in views:
        if len(temp) == 2: 
            views = temp[0] + '.' + temp[1] +'00.000'
        else: views = temp[0] + '.000.000'
    else: views = temp[0]  + '.000'

    # print(views)
    return views

def video_helper(id:str):
    if 'shorts' in id:
        id = id.replace('/shorts/','')
    elif 'watch' in id:
        id = id.replace('/watch?v=','')
    
    return id

# views_helper('18M views')
