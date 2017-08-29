# 网易严选模仿

####网站端使用Django + MySQL + Celery + Redis
提供首页商品列表功能、商品详情页面和分类页面, 实现简单的页面展示功能


####爬虫端使用Scrapy  每日定时从严选的某个频道爬取商品信息
- 用redis-scrapy做分布式爬虫
- 使用user agent池，轮流选择之一来作为user agent
- 禁止cookies
- 从代理网站上爬取代理, 每隔一段时间会检查代理的状态, 使用可用的代理爬取网站
- 每次爬取网站数据, 都会对返回内容求hash值,代表本次获得内容,
下次更新时如果哈希值相同则不再更新数据库

####目录结构
- netease_spider 项目主配置
- netease banner models
- goods 商品、分类等相关
- spider 爬虫相关
- utils 工具函数

#### 环境需求
mysql + redis + python 相关

#### 其他说明
- 配置环境是请修改 netease_spider/local_setings.py 更改redis和mysql的配置
- 注意爬虫的执行顺序, 先爬取category 在爬取goods, 定时任务里这两个任务也是有先后之分的
- 由于时间比较紧, 只在自己的开发机上搭建了环境, 没有在其他的平台测, 回去也会修改
