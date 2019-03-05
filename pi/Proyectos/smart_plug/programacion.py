# Archivo para gestionar la programacion de turnos en el proyecto smart_plug
import shutil, os, time, datetime
from datetime import timedelta
#from datetime import datetime
import mysql.connector
import numpy as np

def SeleccionaEstadoActual():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="D1egoarmando",
    database="smart_plug"
  );
  mycursor = mydb.cursor();
  mycursor.execute("SELECT est1.id_enchufe as id_enchufe, est1.est_actual as est_actual, est1.est_deseado as est_deseado, est1.es_turno as es_turno, est1.hora as hora FROM `estado` as est1 INNER JOIN (SELECT DISTINCT MAX(id) AS id, id_enchufe FROM `estado` GROUP BY id_enchufe ORDER BY id DESC) as est2 ON est1.id = est2.id");
  myresult = mycursor.fetchall();
  return myresult;

def GetTurnos (id_enchufe):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="D1egoarmando",
    database="smart_plug"
  );
  mycursor = mydb.cursor();
  dia = datetime.datetime.today().weekday()+1;
  sql = "SELECT dia, hora, minutos, activo from programacion WHERE activo = 1 AND id_enchufe=%s AND dia=%s";
  val = (id_enchufe, dia);
  mycursor.execute (sql, val);
  myresult = mycursor.fetchall();

  return myresult;

def SeteaEstadoDeseadoEnchufe (est_actual, est_deseado, id_enchufe):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="D1egoarmando",
    database="smart_plug"
  );
  mycursor = mydb.cursor();
  sql = "INSERT INTO estado (id_enchufe, es_turno, est_actual, est_deseado, hora) VALUES (%s, 1, %s, %s, now())";
  val = (id_enchufe, est_actual, est_deseado);
  print sql;
  mycursor.execute(sql, val);
  mydb.commit();
  print "Datos insertados correctamente.";

# from /var/www/html/Proyectos/smart_plug/selector_estado.php import 

  
# Cada 5 minutos se ejecutara el escript se comprueba el ultimo estado de cada enchufe.
#    Si esta desactivado :
#		Se chequean los turnos programados de ese enchufe para el dia de hoy
#		Se calcula si se tiene que encencer de forma automatica
#		Se enciende anyadiendo un 1 en el campo es_turno
#    Si esta activado:
#	Se checkea si se ha activa de forma manual o automatica:
#    		Si se ha activado de forma manual no se hace nada
#    		Si se ha activado de forma automatica se comprueba la hora de activacion y los minutos programados por si hay que apagarlo.
# Nota 1: El script comprueba si hay algun turno que haya empezado hace 5 minutos o menos
# Nota 2: Cada vez que se actualice la bbdd desde el script se debera poner un 1 en el campo es_turno


#Llamamos a la funcion donde hacemos la select
est_actuales = SeleccionaEstadoActual();

print (np.matrix(est_actuales));

for estados in est_actuales:
  turnos = GetTurnos (estados[0]);
  print (np.matrix(turnos));
  for turno in turnos:
    print "hora_inicio:";
    
    # print datetime.datetime.strptime(turno[1], '%I:%M:%S');
    s_hora_inicio = str(turno[1]);
    s_hora_final = str(turno[1] + timedelta(minutes=turno[2]));
    s_hora_final_max = str( turno[1] + timedelta(minutes=turno[2]) + timedelta(minutes=9) ); # Variable que se crea para establecer un tiempo de apagado maximo. Este tiempo se compara con tiempo actual para decidir apagar, como el script se ejecuta cada 5 min se establece aqui un tiempo mayor a 5 min.
    if (len(s_hora_inicio)==7):
      s_hora_inicio = '0'+s_hora_inicio;
    if (len(s_hora_final)==7):
      s_hora_final = '0'+s_hora_final;
    if (len(s_hora_final_max)==7):
      s_hora_final_max = '0'+s_hora_final_max;

    hora_inicio = datetime.datetime.strptime(s_hora_inicio,'%H:%M:%S').time();
    hora_final = datetime.datetime.strptime(s_hora_final,'%H:%M:%S').time();
    hora_final_max = datetime.datetime.strptime(s_hora_final_max, '%H:%M:%S').time();

    print "hora_inicio, hora final:" + s_hora_inicio +", "+s_hora_final;
    print hora_inicio;
    print hora_final;
    if (estados[1] == 0): # Si el estado actual del id_enchufe tratado esta desactivado
      if ( (hora_inicio < datetime.datetime.now().time()) and (hora_final > datetime.datetime.now().time()) ): #Si tiene que encenderse por turno se enciende
        SeteaEstadoDeseadoEnchufe (estados[1], 1, estados[0]);
        print "Tiene que encenderse un turno";
      else: print "No se tiene que encender ningun turno";
    elif (estados[1] == 1): # si el estado actual del id_enchufe tratado esta activado.
      if (estados[3] == 1): # Si se ha activado de forma automatica
        if ((hora_final < datetime.datetime.now().time()) and (hora_final_max >  datetime.datetime.now().time() )): # Si la hora final del turno es mayor que la actual y menos que la actual mas 9 min. se apaga
          SeteaEstadoDeseadoEnchufe (estados [1], 0, estados[0]);
          print "Tiene que desactivarse un turno";
        else: print "No se tiene que desactivar por ningun turno";
      elif (estados[3] == 0): print "Esta activado de forma manual, no se desactiva";
