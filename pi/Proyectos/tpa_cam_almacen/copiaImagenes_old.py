import shutil, os, time, datetime
from datetime import timedelta
from os import listdir
from os.path import isfile, join

# Definimos funcion para eliminar los archivos de una carpeta
def delete_Files(folder):
      files_dump = [join(folder, c) for c in listdir(folder)];
      files_dump = filter(lambda c: isfile(c), files_dump);
      [os.remove(c) for c in files_dump];


# Definicion de variables
forigen = "/home/camarauser/FTP/camaras/tpa_almacen/";
fweb = "/var/www/html/Proyectos/tpa_almacen/images/";
fpen = "";
lista_archivos = [];
for cosa in listdir(forigen):
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
	print "voy a entrar en for:" + fweb + "  " + fecha_format;
	for arch in lista_archivos:
		arch_format = arch[1:7];
		if arch_format == fecha_format:
			#os.remove(ruta+arch)
			cont = cont + 1;
			if (cont == 10): # guardamos 1 de cada 10 imagenes
				cont = 0;
				shutil.copyfile(forigen + arch, fweb + arch);
				print "Archivo copiado: ",arch;
	n_day = n_day - 1;

print "Copiadas las imagenes a web:" + fweb, lista_archivos, fecha_copiar, fecha_format;
