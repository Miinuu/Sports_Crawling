import requests
from bs4 import BeautifulSoup

#국내 배구 일정
months = [1,2,3,4,8,9,10,11,12]
for month in months:
    url = f"https://sports.news.naver.com/volleyball/schedule/index?date=20221004&month={month}&year=2022&teamCode=&category="
    res = requests.get(url)
    res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

    soup = BeautifulSoup(res.text, "lxml")
    soupData = [soup.findAll("div", {"class": "sch_tb"}),soup.findAll("div", {"class": "sch_tb2"})]  # sch_tb 짝수날짜, sch_tb2 홀수날짜
    dataList = []
    for dataTb in soupData:
        for data in dataTb:
            # 모든 날짜
            dateValue = data.find("span", {"class": "td_date"}).text
            if (len(dateValue.split(" ")[0].split(".")[1]) == 1):
                dateValue = dateValue.split(" ")[0].split(".")[0] + ".0" + dateValue.split(" ")[0].split(".")[1] + " " + dateValue.split(" ")[1]
            matchNum = data.find("td")["rowspan"]  # 경기가 없는 날의 rowspan == 5, 있는 날의 rowspan은 경기수
            if (int(matchNum) == 5):
                matchNum = '1'
            for i in range(int(matchNum)):
                matchData = {} #경기정보를 저장하는 딕셔너리
                #날짜정보
                matchData["date"] = dateValue
                #경기시간
                matchData["time"] = data.findAll("tr")[i].find("span", {"class": "td_hour"}).text
                if matchData["time"] != "-":  # 경기 일정이 있을때
                    # 홈팀
                    matchData["home"] = data.findAll("tr")[i].find("span", {"class": "team_lft"}).text
                    # 어웨이팀
                    matchData["away"] = data.findAll("tr")[i].find("span", {"class": "team_rgt"}).text
                    if data.findAll("tr")[i].find("strong", {"class": "td_score"}).text != "VS":  # 종료된 경기일 때
                        # 홈팀 스코어
                        matchData["homeScore"] = data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                        # 어웨이팀 스코어
                        matchData["awayScore"] = data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[1]
                    else:  # 진행 예정 경기일 떄
                        matchData["homeScore"] = "-"
                        matchData["awayScore"] = "-"
                    # 남성부 / 여성부 경기
                    matchData["gender"] = data.findAll("tr")[i].findAll("span", {"class": "td_event"})[0].text
                    # 경기장
                    matchData["stadium"] = data.findAll("tr")[i].findAll("span", {"class": "td_stadium"})[0].text
                    # 라운드
                    matchData["round"] = data.findAll("tr")[i].findAll("span", {"class": "td_round"})[0].text
                else:  # 경기 일정이 없을 시
                    matchData["home"] = "-"
                    matchData["away"] = "-"
                    matchData["homeScore"] = "-"
                    matchData["awayScore"] = "-"
                    matchData["gender"] = "-"
                    matchData["stadium"] = "-"
                    matchData["round"] = "-"
                dataList.append(matchData)

    #데이터 정렬
    result = sorted(dataList,key= lambda x: x["date"].split(" ")[0])
    print(result)


