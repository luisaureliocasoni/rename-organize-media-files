from exif import Image
import sys
import shutil
import re
import os
import glob
import subprocess
import mimetypes
from os import listdir, path
from os.path import isfile, join

# metodos

def getVideoDetails(filepath):
    # roda o comando ffprobe para pegar as informações do arquivo
    # o output do comando é entregue a variavel ffmpeg_info
    # por bizzarice, o resultado do ffprobe é colocado no stderr, por isso,
    # tive que redirecionar o stderr para lá
    # o separador de pastas está configurado como \\, por que estou rodando no Windows
    # se estiver usando o linux, mude isso.
    ffmpeg_info = subprocess.check_output(
        "ffmpeg\\bin\\ffprobe.exe -i \"%s\"" % (filepath),
        stderr=subprocess.STDOUT,
        shell=True)

    # o resultado de check_output é uma string binária 
    # converte para unicode e divide as linhas do resultado do console
    ffmpeg_info_unicode = ffmpeg_info.decode('utf-8')
    lines = ffmpeg_info_unicode.splitlines(True)

    # faz o trabalho de extracao dos valores
    metadata = {}
    for l in lines:
        l = l.strip()
        if l.startswith('Duration'):
            metadata['duration'] = re.search('Duration: (.*?),', l).group(0).split(':',1)[1].strip(' ,')
            metadata['bitrate'] = re.search(r"bitrate: (\d+ kb/s)", l).group(0).split(':')[1].strip()
        if l.startswith('Stream #0:0'):
            metadata['video'] = {}
            metadata['video']['codec'], metadata['video']['profile'] = [e.strip(' ,()') for e in re.search(r'Video: (.*? \(.*?\)),? ', l).group(0).split(':')[1].split('(')]
            metadata['video']['resolution'] = re.search(r'([1-9]\d+x\d+)', l).group(1)
            metadata['video']['bitrate'] = re.search(r'(\d+ kb/s)', l).group(1)
            metadata['video']['fps'] = re.search(r'(\d+ fps)', l).group(1)
        if l.startswith('Stream #0:1'):
            metadata['audio'] = {}
            metadata['audio']['codec'] = re.search('Audio: (.*?) ', l).group(1)
            metadata['audio']['frequency'] = re.search(', (.*? Hz),', l).group(1)
            metadata['audio']['bitrate'] = re.search(r', (\d+ kb/s)', l).group(1)
        if l.startswith('creation_time'):
            metadata['datetime'] = re.search(
                r"(([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2}))", l
            ).group(1)
    return metadata

# variaveis do sistema
filename = sys.argv[0]
has_datetime = True

error_message = '''
PYTHON RENAME IMAGES FROM METADATA DATETIME BETA0
Rename all image files using the datetime metadata, contributing to organize files

'''
error_message += "Usage py "+filename+" input_folder output_folder\n" 
files_renamed = 0
files_copied = 0
files_written = {}


# le os parametros informados na chamada do comando
# ele deve ter dois argumentos na chamada - a origem e o destino do arquivo
args = sys.argv[1:]

if (len(args) != 2):
    print(error_message)
    exit(99)


# pega a lista de arquivos do diretório
# lembre-se que args[0] eh o diretorio em que se estao os arquivos de origem
filelist = [f for f in listdir(args[0]) if isfile(join(args[0], f))]

# verifica se o path de destino existe
if (path.exists(args[1]) == False):
    os.mkdir(args[1])
    print("Criado o diretório " + args[1])

# itera na lista de arquivos
for filename in filelist:

    has_datetime = True

    # verifica se eh uma imagem ou e um video
    mimetypes.init()
    mimestart = mimetypes.guess_type(join(args[0], filename))[0]

    if (mimestart != None):
        # vai pegar a primeira parte do MIME type, que indica o tipo do arquivo
        mimestart = mimestart.split('/')[0]
    else:
        print("Nao é um arquivo de mídia: " + filename)
        continue

    # verifica se eh uma imagem ou nao
    if (mimestart == 'image'):
        #eh uma imagem
        # abre cada arquivo
        with open(join(args[0], filename), 'rb') as img_file:
            
            try:
                image = Image(img_file)
                # verifica se a imagem tem metadata exif
                if (image.has_exif):
                    # verifica qual atributo existe
                    if (hasattr(image, 'datetime')):
                        # pega a data e a hora do arquivo
                        datetime_file = (image.datetime)
                    elif (hasattr(image, 'datetime_original')):
                        # pega a data e a hora do arquivo
                        datetime_file = (image.datetime_original)
                    else:
                        print ("Nao tem dateTime: " + filename)
                        has_datetime = False
                    
                    if (has_datetime):
                        # pega a extensao do arquivo 
                        file_extension = filename.split('.')[-1]
                        # faz a conversao da data e hora para o formato desejado, formando o novo filename
                        new_filename = (re.sub(
                            r"([0-9]{4})\:([0-9]{2}):([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})",
                            r"IMG_\1\2\3_\4\5\6",
                            datetime_file
                            ))
                        # extrai o ano, para facilitar a organizacao
                        year = re.search(
                            r"([0-9]{4})\:([0-9]{2}):([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})",
                            datetime_file
                        ).group(1)

                else:
                    print ("Nao tem exif: " + filename)
                    has_datetime = False
            except AssertionError as aError:
               print ("Nao tem exif: " + filename)
               has_datetime = False
            

            
                
    elif (mimestart == 'video'):
        # assumimos aqui que é um video
        # extrai o metadata, de acordo com o FFMPEG
        metadata = (getVideoDetails(join(args[0], filename)))
        # pega da data e a hora
        datetime_file = metadata['datetime']
        # pega a extensao do arquivo 
        file_extension = filename.split('.')[-1]
        # faz a conversao da data e hora para o formato desejado, formando o novo filename
        new_filename = (re.sub(
            r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})",
            r"VID_\1\2\3_\4\5\6",
            datetime_file
            ))
        # extrai o ano, para facilitar a organizacao
        year = re.search(
            r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})",
            datetime_file
        ).group(1)
    
    else: 
        print("Nao é um arquivo de mídia: " + filename)
        continue

    # verifica se a pasta do ano existe
    # mas antes, verifica se tem datetime, se nao tiver, coloco um nome padrao para year
    if (has_datetime == False):
        year = "sem_data"

    if (path.exists(join(args[1], year)) == False):
        os.mkdir(join(args[1], year))
        print("Criado o diretório " + join(args[1], year))
    
    # copia o arquivo, com o nome novo, no local novo e com os mesmos atributos
    if (has_datetime):
        if new_filename in files_written:
            # tratamento de conflito de nomes de arquivo
            # copia o filename original, para recuperacao previa
            filename_old = new_filename 
            # cria um novo filename, apondo um número sequencial, para evitar conflitos
            new_filename = new_filename + "_" + str(files_written[new_filename])
            # atualiza o número de arquivos escritos com o mesmo timestamp
            files_written[filename_old] = files_written[filename_old] + 1
        else:
            # se nao tiver o arquivo previamente, salva para posterior consulta
            files_written[new_filename] = 1

        # monta o nome do novo arquivo
        new_filename = new_filename + "." + file_extension
        
        # copia
        shutil.copy2(join(args[0], filename), join(args[1], year, new_filename))
        files_renamed = files_renamed + 1
        
    else:
        shutil.copy2(join(args[0], filename), join(args[1], year, filename))

    files_copied = files_copied + 1
    

print("Operacao encerrada.")
print(str(len(filelist)) + " foram encontrados")
print("Destes, " + str(files_copied) + " foram copiados.")
print("Destes, " + str(files_renamed) + " foram renomeados e copiados.")

