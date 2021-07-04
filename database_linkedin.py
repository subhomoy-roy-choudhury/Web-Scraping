import sqlite3
import json
import os

conn = sqlite3.connect('linkedin_job_finder.db')
print("Opened database successfully")

# conn.execute('''CREATE TABLE LINKEDIN_JOB_FINDER
#         (ID INT PRIMARY KEY     NOT NULL,
#         JOBID           CHAR(50),
#         TITLE           CHAR(50),
#         COMPANY         CHAR(50),
#         PLACE           CHAR(50),
#         DATE            CHAR(50),
#         LINK            CHAR(50),
#         DESCRIPTION     TEXT,
#         JOB_FUNCTION    CHAR(50),
#         EMPLOYMENT_TYPE CHAR(50),
#         INDUSTRIES      CHAR(50));
#         ''')
# print("Table created successfully")

PATH = os.getcwd()
JSON_FILEPATH = os.path.join(PATH,'linkedin_job_finder.json')
with open(JSON_FILEPATH, 'r') as f:
    data_master = json.load(f)

i = 1

for data in data_master :

    conn.execute(f"INSERT INTO LINKEDIN_JOB_FINDER (ID,JOBID,TITLE,COMPANY,PLACE,DATE,LINK,DESCRIPTION,JOB_FUNCTION,EMPLOYMENT_TYPE,INDUSTRIES) \
        VALUES ('{i}','{data['job_id']}','{data['title']}','{data['company']}','{data['place']}','{data['date']}','{data['link']}','{data['description']}','{data['job_function']}','{data['employment_type']}','{data['industries']}')");

    i += 1

conn.commit()
print("Records created successfully")

conn.close()