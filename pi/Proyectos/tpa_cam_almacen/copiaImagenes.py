import shutil, os, time, datetime
from datetime import timedelta
from os import listdir
from os.path import isfile, join

# Definimos funcion para eliminar los archivos de una carpeta
def delete_Files(folder):
	try:
      		files_dump = [join(folder, c) for c in listdir(folder)];
      		files_dump = filter(lambda c: isfile(c), files_dump);
      		[os.remove(c) for c in files_dump];
	except Exception as inst:
		err = "Error al eliminar ficheros: " + type(inst) + " / " + inst.args + " / " + inst;
		print err;
		write_log(err);

# Definimos variables para leer / escribir en el log.
def read_log:
	try:
		dato = "";
		f = open("copiaImagenes.log");
		cont = f.readlines();
		f = close("copiaImagenes.log");
		dato = cont[len(cont)-1];
	except Exception as int:
		err = "Error al leer log: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

	return dato;


def write_log(data):
	try:
		f = open("copiaImagenes.log", "a");
		data = str(datetime.datetime.now()) + " / " + data;
		f.write (data);
		f = close("copiaImagenes.log");
	except Exception as inst:
		err = "Error al escribir en el log: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                # En este caso no escribimos en el log porque nos ha dado error precisamente esto... OJO.

# Definicion de variables
fftp = "/home/camarauser/FTP/camaras/tpa_almacen/";
fweb = "/var/www/html/Proyectos/tpa_almacen/images/";
fusb = "";
lista_archivos = [];
prime_ejc = true; # La inicializamos a true, suponemos que no se ha ejecutado hoy.
est_ant = 0;

#Estados:
#        0: El script se ha iniciado pero no ha llegado a hacer nada.
#        1: El script ha eliminado la carpeta de "anteAyer" del directorio web.
#        2: El script ha movido la carpeta de "ayer" a la carpeta "anteAyer"  en el directorio web.
#        3: El script ha movido la carpeta de "hoy" a la carpeta de "ayer" y ha creado una nueva carpeta "hoy" en el directorio web.
#        4: El script ha creado una carpeta con fecha del dia anterior en el usb.
#        5: El script ha movido todas las imagenes del ftp del dia anterior en el usb.
#        6: El script ha copiado las imagenes que ha tomado hasta ahora a la carpeta  "hoy" para el dia actual.
#                En este estado el script debe copiar las nuevas imagenes del ftp a la carpeta hoy del directorio web.
#                Tras copiar imagenes el escript escribira la fecha y hora y mantendra el estado 6 hasta el dia siguiente.

# Veamos el estado de la ultima ejecucion
# Es la primera del dia?
f_ant = datetime.datetime.strptime(read_log[0:24], '%Y-%m-%d %H:%M:%S.%f');

if (f_ant.date() == datetime.datetime.today().date())
	prime_ejec = false;
else
	# Si no es la primera ejecucion del dia chequeamos el estado.
	est_ant = int(read_log[29:30]);

# Tratamos los posibles casos del fichero
if (prime_ejec):
	try:
		write_log ("0");
		prime_ejec=false;
		est_ant = 0;
	except Exception as inst:
		err = "Error al tratar la primera ejecucion: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);
#        0: El script se ha iniciado pero no ha llegado a hacer nada.
if (est_ant == 0):
	try:
		os.remove(join(fweb,"anteAyer");
		write_log("1");
		est_ant = 1;
	except Exception as inst: 
		err = "Error al eliminar la carpeta anteAyer: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

#        1: El script ha eliminado la carpeta de "anteAyer" del directorio web.
if (est_ant == 1):
	try:
		os.rename(join(fweb,"ayer"), join (fweb,"anteayer"));
		write_log ("2");
		est_ant = 2;
	except  Exception as inst:
                err = "Error al mover carpeta ayer a anteAyer: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

#        2: El script ha movido la carpeta de "ayer" a la carpeta "anteAyer"  en el directorio web.
if (est_ant == 2):
	try:
                os.rename(join(fweb,"hoy"), join (fweb,"ayer"));
                os.mkdir(join(fweb,"hoy"));
		write_log ("3");
                est_ant = 3;
        except  Exception as inst:
                err = "Error al mover carpeta hoy a ayer: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

#        3: El script ha movido la carpeta de "hoy" a la carpeta de "ayer" y ha creado una nueva carpeta "hoy" en el directorio web.
if (est_ant == 3):
	 try:
                # Crear carpeta con fecha del dia anterior en usb.
                write_log ("4");
                est_ant = 4;
        except  Exception as inst:
                err = "Error al crear carpeta con fecha de ayer en usb: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

#        4: El script ha creado una carpeta con fecha del dia anterior en el usb.
if (est_ant == 4):
	 try:
                MueveImagenes (1, fftp, fusb, "mv");
                write_log ("5");
                est_ant = 5;
        except  Exception as inst:
                err = "Error al mover las imagenes de ayer al usb: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);

#        5: El script ha movido todas las imagenes del ftp del dia anterior en el usb.
if ((est_ant == 5)):
	try:
                MueveImagenes (0, fftp, fweb, "cp"); #parametros: (delta_days, ruta_origen, ruta_destino, accion ("cp"-copiar, "mv"-mover)
                write_log ("5");
                est_ant = 5;
        except  Exception as inst:
                err = "Error al copiar las imagenes de hoy a web: " + type(inst) + " / " + inst.args + " / " + inst;
                print err;
                write_log(err);
#        6: El script ha copiado las imagenes que ha tomado hasta ahora a la carpeta  "hoy" para el dia actual.
#                Tras copiar imagenes el escript escribira la fecha y hora y mantendra el estado 6 hasta el dia siguiente.
# Este esta 6 realmente no es necesario

for cosa in listdir(fftp):
    lista_archivos += [cosa];
f_act = datetime.date.today();
f_arch_pen = f_act - timedelta(days=3);
carp_pen = f_act;
n_day = 2;

# Tratamiento de imagenes para visualizacion en la web.
# Creamos en el pen una carpeta (si no existe) con nombre fecha de hace 3 dias
	# TO DO
# Movemos las imagenes del ftp de hace 3 dias (anteAyer) a esa carpeta
	# TO DO

# Pensar esta parte
# Eliminamos la carpeta de anteAyer de la web
#os.remove(join(fweb,"anteAyer");
# Cambio de nombre carpeta ayer->anteAyer
#os.rename(join(fweb,"ayer"), join (fweb,"hoy"));
# Cambio de nombre de la carpeta hoy->ayer
#os.rename(join(fweb,"hoy"), join(fweb,"ayer"));
# Creamos una nueva carpeta llamada hoy
#os.mkdir(join(fweb,"hoy"));


# Eliminamos los archivos en las carpetas actuales
delete_Files (join (fweb, "anteAyer/"));
print "Eliminados archivos de ante ayer";
delete_Files (join (fweb, "ayer/"));
print "Eliminados archivos de ayer";
delete_Files (join (fweb, "hoy/"));
print "Eliminados archivos de hoy";
cont = 0;
while (n_day >=0):
	fweb = "/var/www/html/Proyectos/tpa_almacen/images/"
	day= datetime.timedelta(days=n_day);
	f_copi = f_act - day;
	fecha_copiar = str(f_copi);

	fecha_format = fecha_copiar[2:4] + fecha_copiar[5:7] + fecha_copiar[8:10];
	if n_day == 2:
		fweb = fweb + "anteAyer/";
	elif n_day == 1:
		fweb = fweb + "ayer/";
	elif n_day == 0:
		fweb = fweb + "hoy/";
	else:
		fweb = "/home/pi/Documents/images/";
	cont = 0; # inicializamos contador
	for arch in lista_archivos:
		arch_format = arch[1:7];
		if arch_format == fecha_format:
			#os.remove(ruta+arch)
			cont = cont + 1;
			if (cont == 10): # guardamos 1 de cada 10 imagenes
				cont = 0;
				shutil.copyfile(fftp + arch, fweb + arch);
				print "Archivo copiado: ",arch;
	n_day = n_day - 1;

print "Copiadas las imagenes a web:" + fweb, lista_archivos, fecha_copiar, fecha_format;
