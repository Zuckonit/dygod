## 安装

```
python setup.py install
```

## 用法


```
Usage: dygod [OPTIONS] COMMAND [ARGS]...

Options:
  --host TEXT  homepage url
  -h, --help   Show this message and exit.

Commands:
  list
  search
```


### list命令

#### help

```
dygod --help

Usage: dygod list [OPTIONS]

Options:
  -l, --list                show all categories  [default: False]
  -s, --select INTEGER      choose a category  [default: 0]
  -p, --page INTEGER RANGE  which page  [default: -1]
  -h, --help                Show this message and exit.
```

#### 例子

* 查看所有电影类目

```
➜  dygod list -l

0  欧美电视
1  最新综艺
2  最新影片
3  游戏下载
4  动漫资源
5  手机电影
6  华语电视
7  经典影片
8  国内电影
9  日韩电视
10  欧美电影
11  旧版综艺
```

* 查看某个类目的电影

```
➜  dygod list -s 0

[1/38] 2017年美国欧美剧《罪恶黑名单第五季》连载至9
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季01.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季02.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季03.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季04.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季05.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季06.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季07.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单第五季08.mp4
		ftp://m:m@tv.kaida365.com:2199/罪恶黑名单第五季09.mp4
		ftp://m:m@tv.kaida365.com:2199/罪恶黑名单第五季10.mp4
[1/38] 2017年美国欧美剧《烈阳第一季》连载至5
		ftp://m:m@tv.kaida365.com:2199/烈阳第一季01.mp4
		ftp://m:m@tv.kaida365.com:2199/烈阳第一季02.mp4
		ftp://m:m@tv.kaida365.com:2199/烈阳第一季03.mp4
		ftp://m:m@tv.kaida365.com:2199/烈阳第一季04.mp4
		ftp://m:m@tv.kaida365.com:2199/烈阳第一季05.mp4

```

### search命令

#### help

```
dygod search -h

Usage: dygod search [OPTIONS]

Options:
  -p, --page INTEGER  which page  [default: 0]
  -k, --keyword TEXT  search keyword  [default: ]
  -h, --help          Show this message and exit.
```


#### 例子

* 搜索电影

```
➜  dygod dygod search -k 罪恶黑名单
[0/0] 2017年美国欧美剧《罪恶黑名单:救赎第一季》连载至8
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季01.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季02.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季03.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季04.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季05.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季06.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季07.mp4
		ftp://m:m@tv.dl1234.com:2199/罪恶黑名单救赎第一季08.mp4
[0/0] 2013美国罪案悬疑剧《罪恶黑名单》更新至22集[中英双字]
```
