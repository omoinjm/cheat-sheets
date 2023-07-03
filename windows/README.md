# Windows cheet-sheets

## Load macOs BigSur

- right click install.inf file and install

- 'win + r' and type control mouse

- under the `Poniters` tabs, change scheme to macOSBigSur

## Environment Variables
 
 - link: https://www.devdungeon.com/content/set-environment-variables-windows

## Hide files
 
 POWERSHELL
 
 ```powershell
 # hide file content within another file
 # delete file after doing this
 type file > demoFile:file
 
 # view contents
 cat demoFile:file
 
 # show hidden files in an alternate data stream
 dir /r
 
 # Another way
 # this just checks the show/hide hidden files under `view` -> `options` -> `change folder and view options` -> `view`
 attrib +h file
 
 
 ```
 
 ## Setup ssh on personal laptop
 
  - link: https://theitbros.com/ssh-into-windows/
