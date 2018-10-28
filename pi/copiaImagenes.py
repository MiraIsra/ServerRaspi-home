import shutil, os, time, datetime
from os import listdir
#forigen = "home/camarauser" + os.sep + "ftp" + os.sep + "camaras" + os.sep + "tpa_almacen" + os.sep
forigen = "/home/camarauser/ftp/camaras/tpa_almacen/";
fdestino = "/var/www/html/tpa_almacen/images/";
lista_archivos = [];
for cosa in listdir(forigen):
    lista_archivos += [cosa];
f_act = datetime.date.today();
#day= datetime.timedelta(days=1)
#day= datetime.timedelta(days=2);
n_day = 2;
#f_copi = f_act - day;
#fecha_copiar = str(f_copi);

#fecha_format = fecha_copiar[2:4] + fecha_copiar[5:7] + fecha_copiar[8:10];

while (n_day >=0):
	fdestino = "/var/www/html/tpa_almacen/images/"
	day= datetime.timedelta(days=n_day);
	f_copi = f_act - day;
	fecha_copiar = str(f_copi);

	fecha_format = fecha_copiar[2:4] + fecha_copiar[5:7] + fecha_copiar[8:10];
	if n_day == 2:
		fdestino = fdestino + "anteAyer/";
	elif n_day == 1:
		fdestino = fdestino + "ayer/";
	elif n_day == 0:
		fdestino = fdestino + "hoy/";
	else:
		fdestino = "/home/pi/Documents/images/";
	for arch in lista_archivos:
		arch_format = arch[1:7];
		if arch_format == fecha_format:
			#os.remove(ruta+arch)
			shutil.copyfile(forigen + arch, fdestino + arch);
			print "Archivo copiado: ",arch;
	n_day = n_day - 1;

print fdestino, lista_archivos, fecha_copiar, fecha_format;
