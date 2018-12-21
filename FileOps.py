import xlrd
abbr_dict = {}
stopwords_list = []
def readExcelFile(filename, candidate, category):
    try:
        wb = xlrd.open_workbook(filename)
    except:
        print ('FILE NOT FOUND!!')    
    original_tweets = []   
    sheet = wb.sheet_by_name(candidate)
    no_of_rows = sheet.nrows
    if category == 'train':
        for rownum in range(2, no_of_rows):
            try:
                tweet = ''.join(sheet.cell(rownum, 3).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 6).value
            except:
                print ("Some error occurred. RowNum: ", ''.join(sheet.cell(rownum, 3).value))
            
            if sentiment not in (1.0, -1.0, 2.0, 0.0):
                sentiment = 0.0            
            tweet_tuple = tweet, sentiment
            original_tweets.append(tweet_tuple)
    else:
        if candidate == 'Obama':
            for rownum in range(no_of_rows):
                tweet = ''.join(sheet.cell(rownum, 0).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 4).value
                
                tweet_tuple = tweet, sentiment
                original_tweets.append(tweet_tuple)
        else:
            for rownum in range(2, no_of_rows):
                tweet = ''.join(sheet.cell(rownum, 3).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 7).value
                
                tweet_tuple = tweet, sentiment
                original_tweets.append(tweet_tuple)
    
    return original_tweets

def readAbbrFile(abbrFile):
    global abbr_dict
    
    f = open(abbrFile)
    lines = f.readlines()
    f.close()
    for i in lines:
        tmp = i.split('|')
        abbr_dict[tmp[0]] = tmp[1]

    return abbr_dict


def readStopwordsFile(stopwordsFile):
    # stopwords_list
    global stopwords_list
    
    with open(stopwordsFile) as f:
        lines = f.readlines()
    
    for word in lines:
        stopwords_list.append(word.strip())
    
    return list(set(stopwords_list))
