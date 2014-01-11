title: Alembic Database Migration
theme: ../themes/remark-dark.css
name: inverse
layout: true
class: inverse

---
class: center middle

# 使用 Alembic 进行数据库迁移
[greatghoul@GDG西安201312]

---
class: menu

# 如何进行数据库迁移

- **数据误置管理工具** 操作简单、手动维护、无法版本化、无法自动化 
- **SQL 脚本** 门槛高、差异大、版本管理、操作不便、低自动化
- **数据库迁移工具** API 简单易懂、数据库适配，方便移植、高自动化

---
class: menu

# 目前比较优秀的 Migration 工具

- ActiveRecord Migration
- Django Database Migration: South, Django Evoution, dmigrations
- SQLAlchemy Migration: Alembic

---
class: center middle

**Alembic** 是由 **SQLAlchemy** 作者编写的一套数据迁移工具。

<https://bitbucket.org/zzzeek/alembic>

---
class: menu

# 安装 Alembic

    $ pip install alembic
    $ cd /path/to/yourproject
    $ alembic init alembic

生成的文件结构如下

    yourproject/
        alembic.ini
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
    
    # max length of characters to apply to the "slug" field
    #truncate_slug_length = 40
    
    # set to 'true' to run the environment during
    # the 'revision' command, regardless of autogenerate
    # revision_environment = false
    
    sqlalchemy.url = driver://user:pass@localhost/dbname
    # sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/scriptfan

---

# Migration脚本

创建一个 Migration 脚本

    $ alembic revision -m "create account table"
    Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
    t_table.py...done

Migration 脚本结构

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
        pass

    def downgrade():
        pass

---

# Migration脚本

脚本中明确指定当前版本和上一版本

    # revision identifiers, used by Alembic.
    revision = 'ae1027a6acf'
    down_revision = '1975ea83b712'

通过 `upgrade` 和 `downgrade` 方法来维护数据库 Schema

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

# 表操作

添加表

    op.create_table(
        'account',
        Column('id', INTEGER, primary_key=True),
        Column('name', VARCHAR(50), nullable=False),
        Column('description', NVARCHAR(200))
        Column('timestamp', TIMESTAMP, server_default=func.now())
    )

重命名表

    op.rename_table('accounts', 'employees')

删除表

    op.drop_table("accounts")

---

# 字段操作

添加字段

    op.add_column('organization',
        Column('name', String())
    )

    op.add_column('organization',
        Column('account_id', INTEGER, ForeignKey('accounts.id'))
    )

修改字段

    op.alter_column('categories', 'name', 
        existing_type=sa.Integer,
        existing_nullable=False,
        type_=sa.String(255)
    )

删除字段

    op.drop_column('organization', 'account_id')

---

# 其它操作

直接执行 SQL

    op.execute('drop table accounts;')

添加外键

    op.create_foreign_key(
                "fk_user_address", "address",
                "user", ["user_id"], ["id"])

---

# 迁移操作

升级或降级

    $ alembic upgrade head
    $ alembic downgrade base

定量升级或者降级

    $ alembic upgrade +2
    $ alembic downgrade -1

升级或者降级到指定版本 `ae1027a6acf`，版本号不一定写全，能唯一确定即可

    $ alembic upgrade ae1027a6acf
    $ alembic upgrade ae1
    $ alembic downgrade ae1027a6acf

生成 sql 脚本

    alembic upgrade 1975ea83b712:ae1027a6acf --sql > migration.sql

执行过的 migration 会被记录在 `alembic_version` 表里面

---

# Alembic集成

- [Flask Alembic](https://github.com/tobiasandtobias/flask-alembic)
- [Uliweb Alembic](https://uliweb.readthedocs.org/en/latest/manage_guide.html?highlight=alembic#alembic)

---

# 参考资料

 * [Alembic 项目主页](https://bitbucket.org/zzzeek/alembic)
 * [Alemmbic 0.6.2 文档](http://alembic.readthedocs.org/en/latest/index.html)
 * [Django Database Migrations](https://docs.djangoproject.com/en/dev/topics/migrations/)
 * [Active Record Migrations](http://guides.rubyonrails.org/migrations.html)
 * [Uliweb Alembic 集成]()

---
class: center middle

## Thank you!
Slideshow created using [remark](http://github.com/gnab/remark).
