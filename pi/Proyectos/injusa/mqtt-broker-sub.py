import ssl
import sys
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
 
import paho.mqtt.client

 
def on_connect(client, userdata, flags, rc):
	#print('connected (%s)' % client._client_id)
	client.subscribe(topic='miraisra/injusa/datos', qos=0)
 
def on_message(client, userdata, message):
	#print('------------------------------')
	#print('topic: %s' % message.topic)
	#print('payload: %s' % message.payload)
	#print('qos: %d' % message.qos)
	get_data (message.payload)
		
def get_data (payload):	
	datos = payload.split('-')
	#print ('-')
	id_maquina = datos[1][3:]
	id_modo = datos[2][3:]
	fase1 = datos[3][3:]
	fase2 = datos[4][3:]
	fase3 = datos[5][3:]
	ciclos = datos[6][3:]
	#print (id_maquina, id_modo, fase1, fase2, fase3, ciclos)
	db_save (id_maquina, id_modo, fase1, fase2, fase3, ciclos)
	
def db_save(id_maquina, id_modo, fase1, fase2, fase3, ciclos):
	#print ('inserting...')
	#insert_data();
	try:
		#print ('trying...')
		current_Date = datetime.now()
		formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
		connection = mysql.connector.connect(host='localhost',
								 database='injusa',
								 user='root',
								 password='D1egoarmando')
		sql_insert_query = (""" INSERT INTO `Consumos` (`timestamp`, `id_maquina`, `id_modo`, `fase1`, `fase2`, `fase3`, `ciclos`) VALUES (%s,%s,%s,%s,%s,%s,%s) """ )#, (formatted_date, int(float(id_maquina)), int(float(id_modo)), float(fase1), float(fase2), float(fase3), float(ciclos)) )#  (formatted_date, 1, 1, 1.1, 1.1, 1.1, 0) )
		#sql_insert_query = (""" INSERT INTO `Consumos` (`timestamp`, `id_maquina`, `id_modo`, `fase1`, `fase2`, `fase3`, `ciclos`) VALUES (CURRENT_TIMESTAMP,1,0,5,0,0,0) """)
		insert_tuple = ( formatted_date, id_maquina, id_modo, fase1, fase2, fase3, ciclos )
		#print ('done')
		cursor = connection.cursor(prepared=True);
		#print ('done1')
		result  = cursor.execute(sql_insert_query, insert_tuple)
		#print ('done2')
		connection.commit()
		#print ('Record inserted successfully into table')
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		#print("Failed inserting record into table {}".format(error))
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
			#print('MySQL connection is closed')	
	#print ('inserted')

def insert_data (id_maquina, id_modo, fase1, fase2, fase3):
	try:
		#print ('trying...')
		connection = mysql.connector.connect(host='localhost',
								 database='injusa',
								 user='root',
								 password='D1egoarmando')
		sql_insert_query = """ INSERT INTO `Consumos`
							  (`timestamp`, `id_maquina`, `id_modo`, `fase1`, `fase2`, `fase3`) VALUES ('%s','%s','%s','%s','%s','%s')"""
		current_Date = datetime.now()
		formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')
		insert_tuple = (current_Date, id_maquina, id_modo, fase1, fase2, fase3)
		#print ('done')
		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()
		#print ("Record inserted successfully into table")
	except mysql.connector.Error as error :
		connection.rollback() #rollback if any exception occured
		#print("Failed inserting record into table {}".format(error))
	finally:
		#closing database connection.
		if(connection.is_connected()):
			cursor.close()
			connection.close()
			#print("MySQL connection is closed")	
	
def main():
    client = paho.mqtt.client.Client(client_id='isra-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=8883)
    client.loop_forever()
	

 
if __name__ == '__main__':
    main()
 
sys.exit(0)
