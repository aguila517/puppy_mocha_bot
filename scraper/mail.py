import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_mail(service, query):
  today = date.today()
  yesterday = today - timedelta(1)
  user_id = 'moches.yun@gmail.com'
  mail_list = []

  # Dates have to formatted in YYYY/MM/DD format for gmail
  #query = "from:minil.yun@icloud.com OR minil.yun@gmail.com is:unread in:inbox newer_than:1d"

  response = service.users().messages().list(userId=user_id, q=query).execute()
  messages = response.get("messages", [])
  message_count = 0
  for message in messages:
      msg = service.users().messages().get(userId=user_id, id=message["id"]).execute()
      message_count = message_count + 1
      email_data = msg["payload"]["headers"]
      for values in email_data:
          name = values["name"]
          if name == "From":
              from_name = values["value"]
              print(from_name)
              subject = [j["value"] for j in email_data if j["name"] == "Subject"]
              mail_list.append(subject)
  return mail_list

def open_gmail_tunnel():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("./credential/token.json"):
    creds = Credentials.from_authorized_user_file("./credential/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./credential/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("./credential/token.json", "w") as token:
      token.write(creds.to_json())
  
  return creds

def get_user_cfg(creds, query):
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    return get_mail(service, query)
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return []
