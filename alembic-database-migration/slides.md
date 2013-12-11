title: Alembic Database Migration
theme: ../themes/remark-dark.css
name: inverse
layout: true
class: inverse center middle

---

# 使用 Alembic 进行数据库迁移
[greatghoul@GDG西安201312]

---

# 如何进行数据库迁移

- 数据误置管理工具：操作简单、手动维护、无法版本化、无法自动化 
- SQL 脚本：门槛高、不同数据库差异大、版本管理、操作不便、低自动化
- 数据库迁移工具：API 简单易懂、数据库适配，方便移植、高自动化

---

# 目前比较优秀的 Migration 工具

- ActiveRecord Migration
- Django Database Migration: South, Django Evoution, dmigrations
- SQLAlchemy Migration: Alembic

---

# Alembic

---

# 安装 Alembic

    $ pip install alembic
    $ cd /path/to/yourproject
    $ alembic init alembic

生成的文件结构如下

    yourproject/
        alembic/
            env.py
            README
            script.py.mako
            versions/
                3512b954651e_add_account.py
                2b1ae634e5cd_add_order_id.py
                3adcc9a56557_rename_username_field.py

---

# Alembic 配置文件

    # A generic, single database configuration.
    
    [alembic]
    # path to migration scripts
    script_location = alembic
    
    # template used to generate migration files
    # file_template = %%(rev)s_%%(slug)s
    
    # max length of characters to apply to the
    # "slug" field
    #truncate_slug_length = 40
    
    # set to 'true' to run the environment during
    # the 'revision' command, regardless of autogenerate
    # revision_environment = false
    
    sqlalchemy.url = driver://user:pass@localhost/dbname

---

# 创建 Migration 脚本

    $ alembic revision -m "create account table"
    Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
    t_table.py...done

Migration 脚本

    """create account table

    Revision ID: 1975ea83b712
    Revises: None
    Create Date: 2011-11-08 11:40:27.089406

    """

    # revision identifiers, used by Alembic.
    revision = '1975ea83b712'
    down_revision = None

    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        op.create_table(
            'account',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('description', sa.Unicode(200)),
        )

    def downgrade():
        op.drop_table('account')

---

# 执行 Migration

    $ alembic upgrade head
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running upgrade None -> 1975ea83b712

定量运行

    $ alembic upgrade +2
    $ alembic downgrade -1

TODO: 数据库中 schema 解l释

---

# 常用 Migration 方法

---

# Upgrading & Downgrading

---

# 参考资料

 * [Alembic 项目主页](https://bitbucket.org/zzzeek/alembic)
 * [Alemmbic 0.6.2 文档](http://alembic.readthedocs.org/en/latest/index.html)
 * [Uliweb 项目主页](https://github.com/limodou/uliweb)
 * [Django Database Migrations](https://docs.djangoproject.com/en/dev/topics/migrations/)
 * [Active Record Migrations](http://guides.rubyonrails.org/migrations.html)
 * [Uliweb Alembic 集成](https://uliweb.readthedocs.org/en/latest/manage_guide.html?highlight=alembic#alembic)

---

name: last-page
template: inverse

## Thank you!
Slideshow created using [remark](http://github.com/gnab/remark).
