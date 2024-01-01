版本
pip install flask==2.1.3
pip install werkzeug==0.16.1
测试：
cd moviebox

===

flask forge (--drop) 创建数据库并导入原始数据
flask run

===
flask shell 
//flask initdb 创建数据库

from app import db
db.create_all()

from app import movie_info

m1 = movie_info(movie_id='1001',title='战狼2',release_date='2017/7/27',country='中国',type='战争',year='2017')
db.session.add(m1)  # 把新创建的记录添加到数据库会话
db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
