from datetime import datetime, timedelta, timezone
from os import getenv

from dotenv import load_dotenv
from requests import patch, post

load_dotenv()
database_id = getenv('DATABASE_ID')
secret_key = getenv('SECRET_KEY')
period_block_id = getenv('PERIOD_BLOCK_ID')


# CLEAR 상태의 페이지를 Library로 이동

def get_target_pages_from_database():
    global secret_key, database_id

    req_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    data = {
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "status": {
                        "equals": "CLEAR"
                    }
                },
                {
                    "property": "Library",
                    "checkbox": {
                        "equals": False
                    }
                }
            ]
        }
    }

    response = post(req_url, headers=headers, json=data)

    result_list = response.json().get('results')
    target_pages = []

    for result in result_list:
        target_pages.append({
            'id': result.get('id'),
            'deadline': result.get('properties').get('Deadline').get('date').get('start')
        })
    return target_pages


def move_pages_to_library():
    global secret_key

    target_pages = get_target_pages_from_database()

    for page in target_pages:
        req_url = f'https://api.notion.com/v1/pages/{page.get("id")}'
        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }

        page['deadline'] = datetime.fromisoformat(page.get('deadline'))
        if page.get('deadline').tzinfo is None:
            page['deadline'] = page['deadline'].replace(tzinfo=timezone.utc)
        if page.get('deadline') < datetime.now(timezone.utc):
            patch(req_url, headers=headers, json={"properties": {"Library": {"checkbox": True}}})


# 스터디 기간 블록 변경
def change_period_block():
    global secret_key, period_block_id

    req_url = f'https://api.notion.com/v1/blocks/{period_block_id}'
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    # String of current date
    current_date = datetime.now().strftime('%m월 %d일')

    # String of 14 days later
    deadline = (datetime.now() + timedelta(days=13)).strftime('%m월 %d일')

    # change content as currnet date
    patch(req_url, headers=headers, json={
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"Study: {current_date} ~ {deadline}"
                    }
                }
            ]
        }
    })
