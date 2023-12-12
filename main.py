from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os


# Функция для авторизации и получения сервиса
def get_calendar_service():
    creds = None
    # Имя файла с учетными данными
    token_pickle = 'token.pkl'
    # Если существует файл с токеном, используем его
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # Если нет действительных учетных данных, запрашиваем их
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',
                                                             ['https://www.googleapis.com/auth/calendar'])
            creds = flow.run_local_server(port=0)
        # Сохраняем учетные данные для следующего запуска
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


# Функция для добавления события
def create_event(start_time_str, summary, duration=75, description=None, location=None):
    service = get_calendar_service()
    start_time = datetime.fromisoformat(start_time_str)
    end_time = start_time + timedelta(minutes=duration)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Europe/Kiev',
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()


# Добавляем 22 занятия
start_date = datetime(2023, 12, 18)
count = 0
while count < 22:
    if start_date.weekday() == 0 or start_date.weekday() == 3:  # Понедельник или четверг
        start_time = start_date.strftime('%Y-%m-%dT19:15:00')
        create_event(start_time, 'Hilel DevOps Class')
        count += 1
    start_date += timedelta(days=1)
