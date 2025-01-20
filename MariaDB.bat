@ECHO OFF
echo --MARIADB--
set /p "choise=Press 1 to stop server. Press 2 to start server "
if %choise%==1 net stop MariaDB
if %choise%==2 net stop MySQL90
if %choise%==2 net start MariaDB
