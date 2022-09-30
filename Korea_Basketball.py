import requests
from bs4 import BeautifulSoup

#국내 농구 일정
months = [1,2,3,4,5,10,11,12]
for month in months :
    url = f"https://sports.news.naver.com/basketball/schedule/index?date=20221001&month={month}&year=2022&teamCode=&category=kbl"
    res = requests.get(url)
    res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

    soup = BeautifulSoup(res.text, "lxml")
    soupData = [soup.findAll("div",{"class" : "sch_tb"}),soup.findAll("div",{"class" : "sch_tb2"})] #짝수, 홀수
    dataList = []
    for dataTb in soupData:
        for data in dataTb:
            #모든 날짜
            dateValue = data.find("span", {"class": "td_date"}).text
            if (len(dateValue.split(" ")[0].split(".")[1]) == 1):
                dateValue = dateValue.split(" ")[0].split(".")[0] + ".0" + dateValue.split(" ")[0].split(".")[1] + " " + dateValue.split(" ")[1]
            matchNum = data.find("td")["rowspan"] #경기가 없는 날의 rowspan == 5, 있는 날의 rowspan은 경기수
            if (int(matchNum) == 5):
                matchNum = '1'
            for i in range(int(matchNum)):
                matchData = {} #모든 경기정보 저장하는 딕셔너리
                #날짜
                matchData["date"] = dateValue
                #시간
                matchData["time"] = data.findAll("tr")[i].find("span", {"class": "td_hour"}).text
                if matchData["time"] != "-":  # 경기 일정이 있을때
                    # 홈팀
                    matchData["home"] = data.findAll("tr")[i].find("span", {"class": "team_lft"}).text
                    # 어웨이팀
                    matchData["away"] = data.findAll("tr")[i].find("span", {"class": "team_rgt"}).text
                    # VS일 시 무승부나 진행예정경기
                    if data.findAll("tr")[i].find("strong", {"class": "td_score"}).text != "VS":  # 종료된 경기일 때
                        # 홈팀 스코어
                        matchData["homeScore"] = \
                        data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                        # 어웨이팀 스코어
                        matchData["awayScore"] = \
                        data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[1]
                    else:  # 진행 예정 경기일 떄
                        matchData["homeScore"] = "-"
                        matchData["awayScore"] = "-"
                    #경기장
                    matchData["stadium"] = data.findAll("tr")[i].findAll("span", {"class": "td_stadium"})[0].text
                else:  # 경기 일정이 없을 시
                    matchData["home"] = "-"
                    matchData["away"] = "-"
                    matchData["homeScore"] = "-"
                    matchData["awayScore"] = "-"
                    matchData["stadium"] = "-"
                dataList.append(matchData)

    #데이터 정렬
    result = sorted(dataList,key= lambda x: x["date"].split(" ")[0])
    print(result)











