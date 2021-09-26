# IP Viewer and Logger
Show your IP address!
```
$ curl http://ip.stevenyu.tw/
111.246.89.186
Taiwan, Taichung 
HiNet (hinet.net)
```

- Usage 
    - `sudo docker image build -t ip_logger .`
    - `sudo docker run -d -p 8001:8001 -v ip_db:/web/database ip_logger`
    - Use proxypass for apache or nginx
- Demo
    - http://ip.stevenyu.tw
    - http://ip.stevenyu.tw/log
        - ![](https://i.imgur.com/1WmByRh.png)
