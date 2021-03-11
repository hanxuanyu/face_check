import pymysql

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'hxuanyu',
    'passwd': 'com.hxuanyu.lcc520',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

DB_NAME = 'face_user'
TABLE_NAME_USER = 'user'
TABLE_NAME_SIGN = 'sign'
ITEM_ID = 'id'
ITEM_NAME = 'name'


def saveData(user_name):

    user_id = getUserCount()+1
    print(user_id)
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    conn.select_db(DB_NAME)
    try:
        value = [user_id, user_name]
        cursor.execute('INSERT INTO '+TABLE_NAME_USER+' values(%s,%s)', value)
        return True
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
        return False
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()


def getNameById(user_id):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    if len(getAllData()) < user_id:
        return 'not found error'
    try:
        conn.select_db(DB_NAME)
        # 查询数据条目
        cursor.execute('SELECT * FROM %s WHERE %s = %s' % (TABLE_NAME_USER, ITEM_ID, user_id))
        if cursor.rowcount == 1:
            print('查询成功')
        result = cursor.fetchall()[0]
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
        return ' '
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return result['id']


def getAllData():
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    try:
        conn.select_db(DB_NAME)
        # 查询数据条目
        cursor.execute('SELECT * FROM %s' % TABLE_NAME_USER)

        result = cursor.fetchall()
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
        result = -1
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return result


def getUserCount():
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    try:
        conn.select_db(DB_NAME)
        # 查询数据条目
        cursor.execute('SELECT * FROM %s' % TABLE_NAME_USER)

        result = cursor.rowcount
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会回滚
        conn.rollback()
        result = -1
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return result


def doSign(name, date):
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    conn.select_db(DB_NAME)
    try:
        cursor.execute('INSERT INTO ' + TABLE_NAME_SIGN + ' values(%s, %s)', (name, date))
        return True
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会回滚
        conn.rollback()
        return False
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()

if __name__ == '__main__':
    print(getNameById(1))
