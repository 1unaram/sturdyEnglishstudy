from datetime import datetime
from time import sleep

import schedule

from tasks import *

# 스터디 시작일
study_start_date = datetime(2024, 12, 8)


# 스터디 시작일로부터 14일이 지날 때마다 True 반환
def is_every_two_weeks():
    current_date = datetime.now()
    days_diff = (current_date - study_start_date).days

    return days_diff % 14 == 0


# 작업
def job():
    if is_every_two_weeks():
        # CLEAR 페이지 Library로 이동
        move_pages_to_library()

        # 스터디 기간 블록 변경
        change_period_block()

        print(f'[{datetime.now()}] Complete to do the job')


# 매일 새벽 2시에 실행
print('Start running the job')
schedule.every().day.at("02:00").do(job)

# 1분마다 작업 확인
while True:
    schedule.run_pending()
    sleep(60)
