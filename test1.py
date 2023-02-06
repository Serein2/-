import pandas as pd
import numpy as np
import pymysql
conn = pymysql.connect(host='rm-bp10k0w05n83wz4af0o.mysql.rds.aliyuncs.com',
                           user='wiki',
                           password='13405427370aA',
                           db='wiki',
                           port=3306)
cursor = conn.cursor()
sql = "select * from pollution where city in (%s, %s, %s)" 
cursor.execute(sql,('长沙',"株洲","湘潭") )

result = cursor.fetchall()
print(result)
