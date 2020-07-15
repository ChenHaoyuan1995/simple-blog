# simple-blog


simple-blog是用tornado实现的简单博客系统。

## 版本要求
* python>=3.6

## 运行
1.安装项目依赖  
`pip install -r requirements.txt`

2.修改config.cfg配置文件  

3.创建相应数据库  
`python manage.py createdb`  

4.生成测试的数据(非必需)  
`python manage.py makedata`

5.启动服务  
`python manage.py runserver`
