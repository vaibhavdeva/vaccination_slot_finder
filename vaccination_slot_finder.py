import requests
import os
import datetime
import time
import pandas as pd
import smtplib, ssl, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import multiprocessing

from parameters import Parameters


def extract_slots_as_table(resp, expected_keys):
    try:
        expected_data = [{key:center[key] for key in expected_keys} for center in resp["sessions"]]
        return pd.DataFrame(expected_data).to_html(columns = expected_keys, index=False, justify="center")
    except e as Exception:
        print(e)
        return f"<p>Unable to extract data from response due to error {e} </p>"

def send_email(sender, receiver, password, port, resp, expected_keys):
    email_msg = MIMEMultipart("alternative")
    email_msg["Subject"] = "Vaccination slots available"
    email_msg["From"] = sender
    email_msg["To"] = receiver
    
    email_body_p2 = extract_slots_as_table(resp, expected_keys)
    email_body_p2 = MIMEText(email_body_p2, "html")
    email_msg.attach(email_body_p2)
    
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, email_msg.as_string())
            
    except Exception as e:
        print(e)


def find_slot_for_single_day(lookup_horizon):

    while True:
        for pincode in Parameters.pincodes:
            try:
                
                # check of slots
                today_date = datetime.date.today() + datetime.timedelta(days=lookup_horizon)
                today_date = today_date.strftime("%d-%m-%Y")
                response = requests.get(url = f"{Parameters.endpoint}{Parameters.find_by_pin}", 
                                        params = {"pincode":pincode, "date":today_date},
                                    headers = {"User-Agent":Parameters.user_agent})

                if response.status_code == 200:
                    response_body = response.json()
                    if len(response_body["sessions"]) > 0 :
                        send_email(
                            Parameters.sender_email,
                            Parameters.receiver_email, 
                            Parameters.password, 
                            Parameters.port, 
                            response_body, 
                            Parameters.expected_keys
                            )
                        
                        print(f"{lookup_horizon} >>> Email sent at {datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')}")
                    else:
                        pass
                else:
                    continue
                
            except Exception as e:
                print(e)
               
        time.sleep(Parameters.interval)

if __name__ == "__main__":

    p1 = multiprocessing.Process(target=find_slot_for_single_day, args=(0,))
    p2 = multiprocessing.Process(target=find_slot_for_single_day, args=(1,))
    p3 = multiprocessing.Process(target=find_slot_for_single_day, args=(2,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()