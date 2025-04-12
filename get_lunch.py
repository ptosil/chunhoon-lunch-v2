import requests
import json
from datetime import datetime, timedelta

# ✅ 학교 식별자
ATPT_OFCDC_SC_CODE = "J10"       # 경기도교육청 코드
SD_SCHUL_CODE = "7530626"        # 충훈고등학교 코드
API_KEY = "00672036b41d4c5b9c44e53c64bd288f"  # 너의 NEIS 인증키

# ✅ 오늘부터 7일간 날짜 생성
today = datetime.today()
dates = [(today + timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]

# ✅ 날짜별로 급식 수집
meal_data = {}
for date in dates:
    url = (
        f"https://open.neis.go.kr/hub/mealServiceDietInfo?"
        f"KEY={API_KEY}&Type=json&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}"
        f"&SD_SCHUL_CODE={SD_SCHUL_CODE}&MLSV_YMD={date}"
    )
    try:
        res = requests.get(url)
        res.raise_for_status()
        rows = res.json()["mealServiceDietInfo"][1]["row"]
        meals = [row["DDISH_NM"].replace("<br/>", "\n").split("\n") for row in rows]
        flat = [item.strip() for sublist in meals for item in sublist if item.strip()]
        meal_data[date] = flat
    except:
        meal_data[date] = []

# ✅ JSON 저장
with open("lunch.json", "w", encoding="utf-8") as f:
    json.dump(meal_data, f, ensure_ascii=False, indent=2)

print("✅ lunch.json 자동 생성 완료!")
