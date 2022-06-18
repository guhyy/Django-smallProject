django前后端不分离实现小项目，对数据库的增删改查，下载excel表格，【发送电子邮件】（很麻烦，个人测试用）  
1.安装python   
2.pip install pymysql   
  pip install mysqlclient    
  pip install django   
  pip install pandas   
3.在settings里更改DATABASES为你自己的mysql信息（端口，密码等） 【当然需要安装mysql，并先建个数据库】名字和DATABASES中'NAME'的值对应   
4.在项目根目录启动命令窗口，执行: python manage.py makemigrations     python manage.py migrate   
5.同上，执行 python manage.py runserver （后面可以加IP地址和端口号，默认不写是127.0.0.1:8000，可以写0.0.0.0:8000 这样对应本机公网IP，如果你是IP别人即可访问，可改端口）  
6.访问后，默认页面没有设置，可以先访问/login/  
