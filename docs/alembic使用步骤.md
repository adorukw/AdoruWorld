三、日常改表工作流（以后每次都是这 3 步）
1. 改 model.py          # 比如给 Post 加 meta_data 字段
2. alembic revision --autogenerate -m "add meta_data to post"
                       # 生成 versions/xxx_add_meta_data_to_post.py
3. alembic upgrade head # 应用
