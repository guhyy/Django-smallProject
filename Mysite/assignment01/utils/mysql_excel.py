import pymysql
import pandas as pd
def export():
    conn = pymysql.connect(host='127.0.0.1',user='root',password='686907',port=3306,db='mywebsite',charset='utf8')
    sql = 'SELECT * FROM mywebsite.assignment01_equipment_info'
    df = pd.read_sql(sql, con=conn)
    print(df)
    df.to_excel(r"C:\Users\惠普\Desktop\Mysite\assignment01\static\data.xlsx", index=False)
    conn.close()
    
if __name__=='__main__':
    export()