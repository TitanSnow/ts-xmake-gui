Start-Process -FilePath xmake -ArgumentList '-P winpty\src' -Wait
Copy-Item build\winpty.dll build\winpty-agent.exe -Destination .
