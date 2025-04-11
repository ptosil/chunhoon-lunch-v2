import requests
import datetime
import json

# 오늘 날짜 구하기
today = datetime.datetime.now().strftime('%Y%m%d')

# NEIS API URL 구성
url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530626&MLSV_YMD={today}&KEY=00672036b41d4c5b9c44e53c64bd288f&Type=json"

# API 요청
response = requests.get(url)
data = response.json()

print(data)

# 데이터 파싱
try:
    meal_info = data['mealServiceDietInfo'][1]['row'][0]
    lunch_data = {
        "date": meal_info['MLSV_YMD'],
        "menu": meal_info['DDISH_NM'].replace('<br/>', '\n')
    }
except KeyError:
    lunch_data = {
        "date": today,
        "menu": "급식 정보가 없습니다."
    }

# JSON 저장
with open("lunch.json", "w", encoding="utf-8") as f:
    json.dump(lunch_data, f, ensure_ascii=False, indent=2)

print("✅ lunch.json 생성 완료!")
