# jd_category
主要是抓取京东分类和商品列表，主要思路是根据分类来抓取所有产品信息，经观察得到https://dc.3.cn/category/get 为获取所有分类信息，先获取所有分类信息，存入数据库，然后在写一个根据分类链接抓取商品数据的spider。现只实现了抓取分类信息
## 1、添加数据表
二级分类表
```CREATE TABLE jd_second_cate (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=322 DEFAULT CHARSET=utf8;


三级分类表
CREATE TABLE `jd_third_cate` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pid` int(10) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=160 DEFAULT CHARSET=utf8;
```
