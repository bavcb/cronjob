from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension, RunReportRequest
import mysql.connector
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/mnt/c/Users/VCB/Downloads/test-api-ga4-435907-52b9f02d6a3f.json'

# สร้าง Client เพื่อเชื่อมต่อกับ GA4 API
client = BetaAnalyticsDataClient()

# กำหนดการร้องขอข้อมูล
request = RunReportRequest(
    property="properties/307754729",  # ใส่ Property ID ของ GA4
    dimensions=[Dimension(name="country")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="2023-01-01", end_date="today")]
)

# รันการดึงข้อมูล
response = client.run_report(request)

# เชื่อมต่อกับ MySQL
connection = mysql.connector.connect(
    host="159.138.255.180",
    user="root",
    password="Vcb168899@",
    database="vcb_ba2"
)
cursor = connection.cursor()
sql = "INSERT INTO test_backup_ga4 (country, active_users) VALUES (%s, %s)"

for row in response.rows:
    data = (row.dimension_values[0].value, row.metric_values[0].value)
    cursor.execute(sql, data)
    
connection.commit() # save การเปลี่ยนแปลง
connection.close() # ปิดการเชื่อมต่อ
