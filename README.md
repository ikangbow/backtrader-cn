## backtrader-cn

### 快速上手

python 版本

	$ python --version
	Python 3.6.0

注：

- 项目中使用了 `f-string`，所以，需要 `Python 3.6` 以上的版本。
- 可以使用 `pyenv` 安装不同版本的 `Python`，用 `pyenv virtualenv` 创建彼此独立的环境。

#### 下载代码

	$ git clone https://github.com/pandalibin/backtrader-cn.git

#### 安装 `mongodb`

##### Mac OSX

安装项目需要的软件包：

	$ brew install mongodb
	$ brew services start mongodb
	$ xcode-select --install  # 安装`arctic`模块报错提示缺少`limits.h`

##### Ubuntu/Debian

安装项目需要的软件包：

	$ sudo apt-get install gcc build-essential  # arctic
	$ sudo apt-get install mongodb

安装 Python modules

> ~~$ pip install -U -r requirements.txt~~

> `pip install -r requirements.txt` 会并行安装 Python modules。
>
> `tushare` 没有将它安装时依赖的包在 `setup.py` 的 `install_requires` 中做声明，导致如果在 `lxml` 安装之前安装 `tushare` 就会报错。

	$ make pip

获取股票数据

	$ python data_main.py

计算入场信号

	$ python frm_main.py

### 备注

使用方法

1. 运行data_main.py，使用tushare进行数据下载

    1.1 数据格式
                open  high  close   low     volume
    date                                          
    2018-05-30  3.35  3.35   3.27  3.26  496207.09
    2018-05-31  3.28  3.34   3.33  3.28  287609.91

2. 运行train_main.py,参数寻优

    2.1 参数寻优：均线策略需要长短期两个值,bar的个数*0.1为短线，bar的个数*0.2为长线个数,即（1，2）（1，7）（1，12）。。。

3. 运行frm_main.py,计算进场信号

4. 运行stock_match_warn.py,打印买卖点信号


