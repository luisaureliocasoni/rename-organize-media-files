# Renomeador e Organizador de Imagens e Vídeos em Python

Esse programa surgiu com a demanda de organizar e renomear centenas de fotos, que tem os nomes todos desnormalizados, de acordo com as informações de metadata dos arquivos.

Para ler os metadados das imagens, uso a biblioteca [Exif](https://pypi.org/project/exif/) do próprio Python. Para ler os metadados de vídeos, verificando que a maioria das câmeras só criam arquivos MP4, decidi usar uma versão portátil da biblioteca [FFMpeg](https://www.ffmpeg.org/), produzido pelo pessoal da [Video Help](https://www.videohelp.com/software/ffmpeg), que oferece versões portáteis compiladas.

Para rodar o comando do FFMPEG do terminal, baseei na versão deste [gist do Github](https://gist.github.com/jaivikram/4690569), que possui alguns problemas, em relação ao seu uso no Windows, e sua manipulação de dados enviados ao stderr. Assim, decidi usar a biblioteca [subprocess do Python](https://docs.python.org/3/library/subprocess.html), que nos permite capturar diretamente em uma variável - evitando arquivos temporários -  o resultado de um comando, mesmo que o resultado seja enviado ao stderr do console. Além disso, troquei o comando de ffmpeg.exe para ffprobe.exe, para receba uma saída sem erros a respeito das informações do vídeo. 

Para verificar se o arquivo é uma imagem ou é um vídeo, usei o módulo [mimetypes](https://docs.python.org/3/library/mimetypes.html), nativo no Python. Para copiar os arquivos, preservando os atributos, usei o módulo - também nativo - [shutil](https://docs.python.org/3/library/shutil.html).

## Requisitos

* Python 3.8 ou superior - com PIP
* Windows - porém pode ser usado para Mac ou Linux, seguindo as instruções de adaptação

## Instalação

1. Clone esse repositório
2. Verifique a versão do FFMpeg:
   1. Se estiver usando Windows, verifique no link do pessoal da [Video Help](https://www.videohelp.com/software/ffmpeg) uma versão mais recente portátil do FFMpeg, de acordo com a sua plataforma. Descompacte os arquivos na pasta `ffmpeg` do repositório.
   2. Se estiver usando Linux ou MacOS, [baixe nesse link](https://www.videohelp.com/software/ffmpeg) uma versão portátil do FFMpeg para a sua plataforma. Descompacte os arquivos na pasta `ffmpeg` do repositório. Além disso, altere na linha 22 do arquivo `rename_images.py` as barras invertidas pelas barras normais, para que o Python encontre o executável.
3. Instale os requisitos rodando o comando `pip3 install -f requirements.txt`
4. Rode o comando: `py rename_images.py <pasta_origem> <pasta_destino>`, onde `<pasta_origem>` é a pasta com os arquivos de origem e `<pasta_destino>` é a pasta com os arquivos de destino.
5. Aproveite!

## Licença

**Este código está sob a licença MIT**

**This code is covered from MIT Licence**

Copyright 2020 Luis Aurelio Casoni

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the  "Software"), to deal in the Software without restriction, including  without limitation the rights to use, copy, modify, merge, publish,  distribute, sublicense, and/or sell copies of the Software, and to  permit persons to whom the Software is furnished to do so, subject to  the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Dúvidas

Pode abrir uma Issue comigo. Aproveite esse código!

