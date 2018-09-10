@echo off
setlocal EnableDelayedExpansion
title Encrypt and decrypt string
color a

rem Create Encrypt/Decrypt arrays
set "charSet=abcdefghijklmnopqrstuvwxyz1234567890@#$*(.,- \/"
set i=0
for %%a in (
    UDFM45 H21DGF FDH56D FGS546 JUK4JH
    ERG54S T5H4FD RG641G RG4F4D RT56F6
    VCBC3B F8G9GF FD4CJS G423FG F45GC2
    TH5DF5 CV4F6R XF64TS X78DGT TH74SJ
    BCX6DF FG65SD 4KL45D GFH3F2 GH56GF
    45T1FG D4G23D GB56FG SF45GF P4FF12
    F6DFG1 56FG4G USGFDG FKHFDG IFGJH6
    87H8G7 G25GHF 45FGFH 75FG45 54GDH5
    45F465 HG56FG DF56H4 F5JHFH SGF4HF
    45GH45 56H45G ) do (
   for %%i in (!i!) do for /F "delims=" %%c in ("!charSet:~%%i,1!") do (
      set "ENC[%%c]=%%a"
      set "DEC[%%a]=%%c"
   )
   set /A i+=1
)

echo Enter a string to encrypt:
set /p Encrypt=
REM cls
set Encrypt2=%Encrypt%
set "EncryptOut="
:encrypt2
   set "EncryptOut=%EncryptOut%!ENC[%Encrypt2:~0,1%]!"
   set "Encrypt2=%Encrypt2:~1%"
if defined Encrypt2 goto encrypt2
echo %EncryptOut%> "%~dp0encrypted.txt"
echo/
set /p CryptedPass=< "%~dp0encrypted.txt"
echo Input string clear text ===^> %Encrypt%
echo/
echo Output string crypted   ===^> %CryptedPass%
pause

set /p Decrypt=< "%~dp0encrypted.txt"
REM cls
ECHO/
ECHO/
set Decrypt2=%Decrypt%
set "DecryptOut="
:decrypt2
   set "DecryptOut=%DecryptOut%!DEC[%Decrypt2:~0,6%]!"
   set "Decrypt2=%Decrypt2:~6%"
if defined Decrypt2 goto decrypt2
echo Input string: %Decrypt%
echo/
echo Output string: %DecryptOut%
pause
