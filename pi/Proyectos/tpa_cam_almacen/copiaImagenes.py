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
        err = "Error al eliminar ficheros: " + inst.args + " / " + inst;
        print err;
        write_log(err);

# Definimos variables para leer / escribir en el log.
def read_log():
    try:
        dato = "";
        f = open("copiaImagenes.log");
        cont = f.readlines();
        f.close();
        dato = cont[len(cont)-1];
    except Exception as inst:
        err = "Error al leer log: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

    return dato;


def write_log(data):
    try:
        f = open("copiaImagenes.log", "a");
        data = str(str(datetime.datetime.now()) + " / " + data);
        f.write ("\n" + data);
        f.close();
    except Exception as inst:
        err = "Error al escribir en el log: " + str(inst.args) + " / " + str(inst);
        print err;
                # En este caso no escribimos en el log porque nos ha dado error precisamente esto... OJO.

def MueveImagenes (dias, forigen, fdestino, metodo, porc): #parametros: (delta_days, ruta_origen, ruta_destino, metodo("cp"-copiar, "mv"-mover), porcentaje (se copiaran 1 de cada X imagenes, donde X es porc))
    cont = 0;
    lista_archivos = [];
    for cosa in listdir(forigen):
        lista_archivos += [cosa];
    f_act = datetime.date.today();
    f_arch_a_mover = f_act - timedelta(days=dias); #Indica la fecha que tienen que tener los archivos a mover
    s_f_arch_a_mover = str(f_arch_a_mover);

    s_f_arch_a_mover_format = s_f_arch_a_mover[2:4] + s_f_arch_a_mover[5:7] + s_f_arch_a_mover[8:10];

    cont = 0; # inicializamos contador
    for arch in lista_archivos:
                f_arch_lista_format = arch[1:7];
                if s_f_arch_a_mover_format == f_arch_lista_format:
                        cont = cont + 1;
                        if (cont == porc): # guardamos 1 de cada "porc" imagenes
                            cont=0;
                            if (metodo=="cp"):
                                shutil.copyfile(forigen + arch, fdestino + arch);
                                print "Archivo copiado: ",arch;

                            elif (metodo=="mv"):
                                shutil.move(forigen + arch, fdestino);
                                print "Archivo movido:", arch;

    print "Copiadas las imagenes:" + forigen, fdestino, metodo, dias;

# Definimos funcion para eliminar carpeta de una ruta y una fecha
def EliminaImagenes (ruta, dias):
    f_elim = datetime.date.today() - delta(days=dias);
    s_f_elim = str(f_elim);
    shutil.rmtree(join(ruta, s_f_elim));
    print "Eliminada la carpeta: " + s_f_elim + " del directorio " + ruta;


# Definicion de variables
fftp = "/home/camarauser/FTP/camaras/tpa_almacen/";
fweb = "/var/www/html/Proyectos/tpa_almacen/images/";
fusb = "/media/usb/images/";

prime_ejec = True; # La inicializamos a true, suponemos que no se ha ejecutado hoy.
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
log = "init";
log = read_log();
f_ant = datetime.datetime.strptime(log[0:24], '%Y-%m-%d %H:%M:%S.%f');

if (f_ant.date() == datetime.datetime.today().date()):
    prime_ejec = False;

# Si no es la primera ejecucion del dia chequeamos el estado.
est_ant = int(log[29:30]);

print "prime_ejec:" + str(prime_ejec) + "   est_ant:" + str(est_ant);

# Tratamos los posibles casos del fichero
if (prime_ejec):
    try:
	EliminaImagenes (fusb, 11);
        write_log ("0");
        prime_ejec=False;
        est_ant = 0;
    except Exception as inst:
        err = "Error al tratar la primera ejecucion: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);
#        0: El script se ha iniciado pero no ha llegado a hacer nada.
if (est_ant == 0):
    try:
        shutil.rmtree(join(fweb,"anteAyer"));
	#os.remove(join(fweb,"anteAyer"));
        write_log("1");
        est_ant = 1;
    except Exception as inst:
        err = "Error al eliminar la carpeta anteAyer: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

#        1: El script ha eliminado la carpeta de "anteAyer" del directorio web.
if (est_ant == 1):
    try:
        os.rename(join(fweb,"ayer"), join (fweb,"anteAyer"));
        write_log ("2");
        est_ant = 2;
    except Exception as inst:
        err = "Error al mover carpeta ayer a anteAyer: "+ str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

#        2: El script ha movido la carpeta de "ayer" a la carpeta "anteAyer"  en el directorio web.
if (est_ant == 2):
    try:
        os.rename(join(fweb,"hoy"), join (fweb,"ayer"));
        os.mkdir(join(fweb,"hoy"));
        write_log ("3");
        est_ant = 3;
    except Exception as inst:
        err = "Error al mover carpeta hoy a ayer: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

#        3: El script ha movido la carpeta de "hoy" a la carpeta de "ayer" y ha creado una nueva carpeta "hoy" en el directorio web.
if (est_ant == 3):
    try:
        f_ayer = str(datetime.date.today() - timedelta(days=1));
        os.mkdir (join(fusb, f_ayer));
        write_log ("4");
        est_ant = 4;
    except Exception as inst:
        err = "Error al crear carpeta con fecha de ayer en usb: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

#        4: El script ha creado una carpeta con fecha del dia anterior en el usb.
if (est_ant == 4):
    try:
        MueveImagenes (1, fftp, join(fusb, f_ayer), "mv", 1);
        write_log ("5");
        est_ant = 5;
    except Exception as inst:
        err = "Error al mover las imagenes de ayer al usb: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);

#        5: El script ha movido todas las imagenes del ftp del dia anterior en el usb.
if ((est_ant == 5)):
    try:
        MueveImagenes (0, fftp, join(fweb, "hoy"), "cp", 10); #parametros: (delta_days, ruta_origen, ruta_destino, metodo("cp"-copiar, "mv"-mover), porcentaje)
        write_log ("5");
        est_ant = 5;
    except Exception as inst:
        err = "Error al copiar las imagenes de hoy a web: " + str(inst.args) + " / " + str(inst);
        print err;
        write_log(err);
#        6: El script ha copiado las imagenes que ha tomado hasta ahora a la carpeta  "hoy" para el dia actual.
#                Tras copiar imagenes el escript escribira la fecha y hora y mantendra el estado 6 hasta el dia siguiente.
# Este esta 6 realmente no es necesario

