import sql
import data_centers as cnn


def cal_backup():

    sql_server = cnn.sql_server()
    sql_server.execute(sql.cal_backup)
    sql_server.commit()
    sql_server.close()

