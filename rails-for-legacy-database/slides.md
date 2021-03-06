title: Rails for Legacy Database
theme: ../themes/remark-dark.css
name: inverse
layout: true
class: inverse
---
class: center middle
# Rails for Legacy Database
[greatghoul@scriptfan-201301]
---
class: center middle
## Convention Over Configuration
然后，有时你不得去面对一些必要的配置，比如，遗留数据库...
---
## 背景

### - 老数据库
### - 不能修改
### - 命名不规范
### - 大量冗余
### - 自定规则主键
---
## 那么遗留数据库有哪些痛

### - **表名的差异**
### - 主键的差异
### - 时间戳的差异

---
## 表名的差异

不同的 ``DBA`` 数据库表的命名方式真的千差万别

    create table driver(...);
    create table order_detail(...);
    create table person(...);

而 ``Rails`` 默认是这样

    Driver ................ drivers
    OrderDetail ..... order_details
    Person ................ people

**其它**：表前缀(如 ``wp_``) 或后缀 (如 ``_tb``)
---
## 表名的差异
.left-column[
### - 少量单数
]
.right-column[
如果数据库中只有少数表名为单数模式，则可以单独在 migrate 时做修改。

``migration`` 

    class CreateGroups < ActiveRecord::Migration
      def change
        create_table :groups do |t|
            # ...
        end
      end
      rename_table :groups, :group
    end

或者

    create_table :group do |t|
        # ...
    end
    
``model``

    class Group < ActiveRecord::Base
      self.table_name = 'group'
      # attr_accessible .... 
    end      
    
]
---
## 表名的差异
.left-column[
### - 少量单数
### - 大量单数
]
.right-column[
如果大部分的表都为单数，就没有必要逐个修改表名，rails 提供了统一的[配置方法](http://guides.rubyonrails.org/configuring.html#configuring-active-record)，来自动生成单数表名，对于个别复数或者不规则的情况，可能参考上一切的方法修改。

``config/application.rb``

    class Application < Rails::Application
       # ...
       config.active_record.pluralize_table_names = false 
    end

设置为单数模式后 generator 会自动生成单数表名

    rails g model Customer name:string

生成的 migrate  

    class CreateCustomer < ActiveRecord::Migration
      def change
        create_table :customer do |t|
          t.string :name

          t.timestamps
        end
      end
    end

]
---
## 表名的差异
.left-column[
### - 少量单数
### - 大量单数  
### - 前缀后缀
]
.right-column[
Wordpress 及一些 CMS 会有表名前缀或者后缀的规则

``config/application.rb``

    class Application < Rails::Application
      # ...
      config.active_record.table_name_prefix = 'foo_'
      config.active_record.table_name_suffix = '_bar'
    end

执行

    $ rails g modal Detail name:string

    # migration output
    create_table :details do |t|
      t.string :name
      # ...
    end
    
    # database output
    create table foo_details_bar ( ... );

前后缀作用于全局，但可在 model 中显式指定表名绕过规则。

    self.table_name = 'details'
]
---
## 那么遗留数据库有哪些痛

### - 表名的差异
### - **主键的差异**
### - 时间戳的差异
---
## 主键的差异

### 命名

``detail_id``, ``id``  

### 类型

字符型：UUID、按规则拼接  
复合型：复合主键

---
## 主键的差异
.left-column[

### - 名称差异 

]
.right-column[
``migration`` 

    class CreateDetails < ActiveRecord::Migration
      def change
        create_table :details, :primary_key => :detail_id do |t|
          # attributes ...
        end
        # ... 
      end
    end
    
``model``

    class Detail < ActiveRecord::Base
      # ...
      self.primary_key = :detail_id
      self.sequence_name = 'YOUR_SEQUENCE_NAME' # Oracle only
      alias_attribute :id, :detail_id
      # attr_accessible .... 
    end      

**TIP: ** 查找ORACLE表的SEQUENCE
    
    select * from user_sequences
    where sequence_name like '%TABLE_NAME%'

]
---
## 主键的差异
.left-column[

### - 名称差异 
### - 类型差异 

]
.right-column[
非默认类型主键无法识别

`migration` 

    class CreateDetails < ActiveRecord::Migration
      def change
        create_table :details, :id => false do |t|
          t.string, :code, :limit => 36
          # attributes ...
        end
        execute 'ALTER TABLE details ADD PRIMARY KEY(code);'
        # ... 
      end
    end
    
_根据数据库的不同，这里设置主键的语句会有变化_

`model`

    class Detail < ActiveRecord::Base
      # ..
      self.primary_key = :code
      # attr_accessible .... 
    end      
    
]
---
## 主键的差异
.left-column[

### - 名称差异 
### - 类型差异 
### - UUID 

]
.right-column[
``lib/extras/uuid_helper.rb``

    require 'rubygems'
    require 'uuidtools'

    module UUIDHelper
      def self.included(base)
        base.class_eval do
          before_create :set_guuid

          def set_guuid
            self.code = UUIDTools::UUID.random_create.to_s
          end
        end
      end
    end

``config/application.rb``

    config.autoload_paths += %W(#{config.root}/extras)
    
``model``

    class Detail < ActiveRecord::Base
      include UUIDHelper
      # attr_accessible .... 
    end      
]
---
## 主键的差异
.left-column[

### - 名称差异 
### - 类型差异 
### - UUID
### - 规则拼接 

]
.right-column[
与 [UUID](#13) 类似，先使用 [类型差异](#12) 一节中的方法设置一个字符型的主键

`model`

    class Detail < ActiveRecord::Base
      before_create :set_code

      def set_code
        self.code = "#{attr1}-#{attr2}" 
      end
    end      
]
---
## 主键的差异
.left-column[

### - 名称差异 
### - 类型差异 
### - UUID
### - 规则拼接 
### - 联合主键

]
.right-column[

gem [composite_primary_keys](http://compositekeys.rubyforge.org/)
    
``migration``

    create_table :detail, :id => false do |t|
      t.integer :id1
      t.integer :id2
      t.string :name
    end
    execute 'ALTER TABLE detail ADD PRIMARY KEY(id1, id2);'

``model``

    class Detail < ActiveRecord::Base 
      self.primary_keys = :id1, :id2 
    end

``relations``

    belongs_to :detail, :foreign_key => [:id1, :id2]

``query``

    Detail.find(1, 1)
]
---
## 那么遗留数据库有哪些痛

### - 表名的差异
### - 主键的差异
### - **时间戳的差异**
---
## 时间戳的差异

Rails默认时间戳

    created_at, updated_at

公司数据库中的时间戳

    created_date, last_modified_date

**解决方法**

``config/initializers/active_record.rb``

    module ActiveRecord
      module Timestamp      
        private
        def timestamp_attributes_for_update #:nodoc:
          [:last_modified_date, :updated_at, :updated_on, :modified_at]
        end
        def timestamp_attributes_for_create #:nodoc:
          [:create_date, :created_at, :created_on]
        end      
      end
    end
---
## Tip#1 vim 快速将表字段转为 Generate 语句
``vim配置``

    " 转换公司的DB描述
    function DbConvert()
      :%s/^\s*\(\S\+\)\s\+varchar\s\+\(\d\+\)\s*$/    \1:string{\2} \\/g
      :%s/^\s*\(\S\+\)\s\+int\s*$/    \1:integer \\/g
      :%s/^\s*\(\S\+\)\s\+datetime\s*$/    \1:datetime \\/g
      :%s/^\s*\(\S\+\)\s\+tinyint\s*$/    \1:boolean \\/g
    endfunction

``调用``

    :call DbConvert()

    # source
    column1 varchar 10
    column2 int
    column3 tinyint
    column4 datetime

    # output
    rails g scaffold Detail \
        column1:string{10} \
        column2:integer \
        column3:boolean \
        column4:datetime
---
## Tip#2 快速将数据库转为 Model 文件
``单表``

    rails g model table_name

``整库``

    gem install rmre
    rmre -a mysql -d dbname -u user -p pwd -o app/models

    # output
    class District < ActiveRecord::Base
        self.table_name = 'district'
        self.primary_key = :district_code

    end

_[rmre](https://github.com/bosko/rmre) 会自动为你配置好主键和表名_

``attr_accessible``

    :%s/\(\w\+\)\s*\n/:\1, /g
    
    # source 
    title
    body

    # output
    :title, :body

---
## Tip#3 显式的指定Model主键，关系和表名

``理由``

 * 有的gem不规范，不会认异于 Rails 约定的主键和关系
 * 异于约定的表名、主键和关系配置显示指定可以提高速度

``显式指定关系``

    belongs_to :detail, :class_name => Detail, :foreign_key => :detail_id

---
## 参考资料

 * [Universally Unique Identifier, UUID](http://zh.wikipedia.org/wiki/UUID)
 * [Ruby and Rails Naming Conventions](http://itsignals.cascadia.com.au/?p=7)
 * [Rails Composite Primary Keys](http://compositekeys.rubyforge.org/)
 * [Ruby on Rails Guides](http://guides.rubyonrails.org/)
 * [Ruby on Rails RDoc](http://api.rubyonrails.org/)
 * [Ruby on Rails 3 Model Working with Legacy Database](http://jonathanhui.com/ruby-rails-3-model-working-legacy-database)
 * [Getting rails to play with a legacy Oracle database](http://www.pixellatedvisions.com/2009/06/08/getting-rails-to-play-with-a-legacy-oracle-database)
 * [Rails and Legacy Databases - RailsConf 2009](http://www.slideshare.net/napcs/rails-and-legacy-databases-railsconf-2009)

---
name: last-page
template: inverse
class: center middle

## Thank you!
Slideshow created using [remark](http://github.com/gnab/remark).
