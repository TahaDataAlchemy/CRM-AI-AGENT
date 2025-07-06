import os
from typing import List
from app.shared.utils.error import Error
from datetime import datetime
import json

class CommonFuntions:
    @staticmethod    
    def get_current_timestamp():
        datetimes = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        element = datetime.strptime(datetimes,"%Y-%m-%d %H:%M:%S")
        timestamp = datetime.timestamp(element)
        return int(timestamp)
    
    @staticmethod
    def get_diff(date1, date2):
        date1 = datetime.fromtimestamp(date1)
        date2 = datetime.fromtimestamp(date2)
        if date2 > date1:
            dif = date2 - date1
        elif date1 > date2:
            dif = date1 - date2
        else:
            dif = date2 - date1

        return dif.days
    
    @staticmethod
    def clean_message(message):
        """Remove emojis and special characters from message"""
        import re
        # Remove emojis and special Unicode characters
        cleaned = re.sub(r'[^\x00-\x7F]+', '', str(message))
        # Remove extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    @staticmethod
    def write_log(message):
        try:
            if os.path.exists(os.path.abspath('app/shared/logs/app_logs/app_logs.txt')):
                log_file = open(os.path.abspath('app/shared/logs/app_logs/app_logs.txt'),'r', encoding='utf-8')
                previous_data = log_file.read()
                log_file.close()

                tmp = previous_data +'\n'+ '['+str(datetime.now())+'][INFO]' + message
               

                log_file = open(os.path.abspath('app/shared/logs/app_logs/app_logs.txt'),'w', encoding='utf-8')
                log_file.write(tmp)
                log_file.close()
                return True
            else:
                # Create the file if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath('app/shared/logs/app_logs/app_logs.txt')), exist_ok=True)
                log_file = open(os.path.abspath('app/shared/logs/app_logs/app_logs.txt'),'w', encoding='utf-8')
                log_file.write('['+str(datetime.now())+'][INFO]' + message)
                log_file.close()
                return True
        except Exception as e:
            print(f"Error writing log: {str(e)}")
            return False
    
    @staticmethod
    def write_error_log(message):
        """Write error logs to app_errors directory"""
        try:
            if os.path.exists(os.path.abspath('app/shared/logs/app_errors/error_logs.txt')):
                log_file = open(os.path.abspath('app/shared/logs/app_errors/error_logs.txt'),'r', encoding='utf-8')
                previous_data = log_file.read()
                log_file.close()

                tmp = previous_data +'\n'+ '['+str(datetime.now())+'][ERROR]' + message
               

                log_file = open(os.path.abspath('app/shared/logs/app_errors/error_logs.txt'),'w', encoding='utf-8')
                log_file.write(tmp)
                log_file.close()
                return True
            else:
                # Create the file if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath('app/shared/logs/app_errors/error_logs.txt')), exist_ok=True)
                log_file = open(os.path.abspath('app/shared/logs/app_errors/error_logs.txt'),'w', encoding='utf-8')
                log_file.write('['+str(datetime.now())+'][ERROR]' + message)
                log_file.close()
                return True
        except Exception as e:
            print(f"Error writing error log: {str(e)}")
            return False
    
    @staticmethod
    def jsonload(TOKEN_FILE:str):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
        return token_data
    @staticmethod
    def jsonDumpRefreshToken(TOKEN_FILE:str,new_token_data:str):
        with open(TOKEN_FILE, "w") as f:
            token_data = json.dump(new_token_data,f)
    
    @staticmethod
    def jsonDump(TOKEN_FILE:str,token_data:str):
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f)

    

