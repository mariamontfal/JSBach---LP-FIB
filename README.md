# EL DOBLE INTÈRPRET JSBACH

## GEI-LP (2021-2022 Q2)

Nota: 10

## Autora

Maria Montalvo Falcón

## Propòsit

Aquesta pràctica proposa un doble intèrpret per a un llenguatge de programació musical anomenat JSBach. La sortida d'aquest doble intèrpret serà una partitura amb les notes que el programa acumula durant l'execució amb la comanda <:> i els fitxers de so: .midi, mp3 i .wav.

## Presentació del llenguatge

```
- l'assignació amb `<-`
- la lectura amb `<?>`
- l'escriptura amb `<!>`
- la reproducció amb `<:>`
- la invocació de procediments
- el condicional amb `if` i potser `else`
- la iteració amb `while`
- l'afegit a llistes amb `<<`
- el tall de llistes amb `8<`
- l[i] per consultar l'i-èsim element d'una llista l. Els índexs de les llistes comencen per 1.
- els comentaris entre ~~~ seran ignorats
```

## Invocació del procediment

`python3 jsbach.py arxiuCodi.jsb [MetodeOpcional]` El mètode que s'executa per defecte és el Main, però es pot indicar qualsevol mètode com a l'inicial si està descit a arxiuAmbElCodi.jsb (aquest arxiu pot tenir qualsevol nom i extensió). A més, si el mètode té paràmetres, s'han d'indicar els paràmetres corresponents que es desitja passar separats amb espais.

## Fitxers generats

```
- bac.pdf: amb la partitura generada
- bac.midi: fitxer de so amb la extensió .midi
- bac.wav: fitxer de so amb la extensió .wav
- bac.mp3: fitxer de so amb la extensió .mp3

** Atenció! Primer es computarà el programa.
   Un cop la computació finalitzi i es visualitzi el càlcul, 
   s'imprimirà per terminal la línia:

   "Computation finished, please, press any key to generate music files"
   
   Un cop es seleccioni qualsevol tecla, es procedirà a la generació 
   dels fitxers musicals en cas de que el programa els contingui
```

## Codi d'exemple: Hanoi

```
~~~ Notes de Hanoi ~~~

Hanoi |:
    src <- {C D E F G}
    dst <- {}
    aux <- {}
    HanoiRec #src src dst aux
:|

HanoiRec n src dst aux |:
    if n > 0 |:
        HanoiRec (n - 1) src aux dst
        note <- src[#src]
        8< src[#src]
        dst << note
        <:> note
        HanoiRec (n - 1) aux dst src
    :|
:|
```

## Eines utilitzades al projecte

`ANTLR, Python3, Timidity++, ffmpeg i Lilipond`

## Instal·lació de les eines

### Linux

```
1) Actualitzar els repositoris de /etc/apt/sources: 
    $ sudo apt update
2) Buscar i actualitzar nous paquetes disponibles: 
    $ sudo apt upgrade
3) Instal·lar python3:
    $ sudo apt install python 3
4) Instal·lar python runtime: 
    $ pip3 install antlr4-python3-runtime 
5) Instal·lar lilypond: 
    $ sudo apt install lilypond
6) Instal·lar timidity: 
    $ sudo apt install timidity
7) Instal·lar ffmpeg: 
    $ sudo apt install ffmpeg
```

### MacOS

```
1) Instal·lar HomeBrew: 
    https://brew.sh/index_ca
2) Instal·lar python3: 
    $ brew install python3
4) Instal·lar python runtime: 
    $ pip3 install antlr4-python3-runtime 
5) Instal·lar lilypond: 
    $ brew install lilypond
6) Instal·lar timidity: 
    $ brew install timidity
7) Instal·lar ffmpeg: 
    $ brew install ffmpeg
```

### Windows

```
Johann Sebastian Bach no tindria un Windows 11 amb vulnerabilitats de sistema que crasheja constantment
```

### ANTLR UNIX

```
1) Descàrrega:
    $ cd /usr/local/lib
    $ curl -O https://www.antlr.org/download/antlr-4.10.1-complete.jar
2) Afegir antlr-4.10.1-complete.jar al CLASSPATH:
    $ export CLASSPATH=".:/usr/local/lib/antlr-4.10.1-complete.jar:$CLASSPATH"
3) Creació d'àlies: 
    $ alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.10.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
    $ alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.10.1-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'
```

## Compilació i execució

```
- Compilar la gramàtica: 
    $ antlr4 -Dlanguage=Python3 -no-listener -visitor jsbach.g4
- Executar: 
    $ python3 jsbach.py arxiuCodi.jsb [FuncioOpcional] [ParametresOpcionals]
```

## Extensions
```
Extensions a JSBach coming on Summer 2022
```

## 

<img src= "https://raw.githubusercontent.com/jordi-petit/lp-jsbach-2022/main/firma.png"
align="right"/>


<br />
<br />
<br />
<br />


<img src="https://www.upc.edu/comunicacio/ca/identitat/descarrega-arxius-grafics/fitxers-marca-principal/upc-positiu-p3005.png" alt="drawing" width="200"/>
