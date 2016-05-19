前些天有人提出个想法，要八一八心灵，看看都有哪些人在跳。结果这么多天过去了，还没人拿出点东西来，于是我觉得要不新闻我来搞哈哈。
改自 https://github.com/Puhao/ 的cc98爬虫
抓取心灵前n页的帖子，记录到文件中，并用jieba做词频分析，最终结果在cut.txt。与原版相比，不需要mongodb，也没有多线程呵呵呵
主程序go.py
====
CC98
====

#爬虫
设定板块的ID号，然后爬虫开始去追踪版面信息，把该板块的每个帖子里，每层楼的发帖者，发帖时间，楼层，发帖内容，改帖子信息存储到MongoDB数据库。

#热词统计
选取帖子超过30页的帖子，进行分词热词统计，然后过滤掉一些无用的热词，每个帖子的热词存储在MongoDB数据库里面。 
 
#依赖库
1.	Beautifusoup4  
	用来解析HTML页面，定位和提取HTML页面里面所需存储的信息。  
	```
	pip install beautifulsoup4
	```
2.	lxml  
	Beautifulsoup使用的第三方解析器  
	```
	pip install lxml
	```

4.	jieba  
	用于分词  
	`` pip install jieba ``
	
