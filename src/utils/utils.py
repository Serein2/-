import pymysql
import os
import sys
import pathlib
import pandas as pd
import numpy as np

import utils.config as config

def getconnect():
    """
    return connect
    """
    conn = pymysql.connect(host=config.host,
                           user=config.user,
                           password=config.password,
                           db=config.db,
                           port=config.port)
    return conn


def get_cityinfo(conn, values,type):
    """
    return pollution or climate or pred of db type(tuple)
    """
    sql = "select * from {} where city in (%s, %s, %s, %s, %s)".format(type)
    cursor = conn.cursor()
    sql = sql.format(type)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    cursor.close()

    conn.close()
    
    return result, cursor


def getdataFrameBytime(result, cursor, time='M'):
    df = pd.DataFrame(result,columns=[i[0] for i in cursor.description])
    df['date']  = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.groupby('city').resample(time).mean()
    df['city'] = [i[0] for i in df.index]
    df.index = [i[1] for i in df.index]
    return df





