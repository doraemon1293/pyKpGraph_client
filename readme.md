---
title: 'pyKP项目进度日志'
author: '黄炎'
date: '2020-10-16'
---

# 项目进度

### 1015
- cluster 完成
- improved autocomplete performance

### 1013
- layer完成

### 1012
- 为修改显示eth port的错误重写query函数



### 1009
- Compose and audit 2G site/cell hour/day charts

### 1005
- Audit 4g cell & site / day & hour charts
- add special function to deal with charts with special requirments
- finish task in todo list

### 0915
- Audit 5g cell & site / day & hour charts

### 0913
- 解决todo list的一些问题

### 0910
- 重新设计得了数据的结构和 完成了重写 服务器/客户端 所有与数据库操作相关的代码 并测试确认效率满足需求

### 0828
- 测试服务器端上传数据 效率过低 需要重写

### 0825
- 4G Hour/Daily template

### 0822
- Tune Legend - (add special legend config)

### 0820
- Add reload template function

### 0815
- 编写GC部份的代码

### 0813
- 修改关于GP算法的BUG

### 0812
- 支持stackedBar

### 0810
- 添加5G kpi自定义aggregation function的配置

### 0808
- 解决使用twin axis 的图里左右坐标轴颜色冲突问题

### 0807
- 服务器端添加自动索引功能 加快查询速度

### 0805
- 增加 MainWindow界面自动切换功能

### 0801
- Report & Maintenance Tab UI

### 0730
- 改进数据上传代码支持批量上传 加快上传速度

### 0725
- 校对5G Daily template

### 0723
- 5G Daily template

### 0720
- 5G Daily Mongodb query 代码

### 0719
- 5G Daily 数据上传服务器端代码

### 0717
- 校对 5G Hourly Charts

### 0715
- 5G Hourly Mongodb query
- 5G Hourly template

### 0713
- kpi 公式编译模块

### 0710
- mpl_cls类

### 0705
- MainWindow UI

### 0703
- 5G Hour 数据上传服务器端

### 0702
- 服务器Mongodb搭建

# Todo
- [ ] Add Export charts function
- [ ] Keep cell name & site for different tab
- [ ] 添加Cluster支持
- [ ] Multi-Cell
- [ ] Worst Cell
- [ ] Export
- [ ] Add change day line
- [ ] 2G TRX TAB
- [ ] HO/NB


- [x] 添加Layer支持
- [x] 读取ep添加带宽+layer 信息
- [x] Compose template for 2G/4G
- [x] 根据query对象的带宽动态判断 DL/UL THrp (5:0.5/2 10:0.35/4 15:0.5/6 20:0.5/8)
- [x] 根据query对象的tech动态判断 SDR (800 0.45 非800 0.2)
- [x] 添加支持某些图片只在特定query level下显示的功能
- [x] Overall chars: PUSCH MCS - overall / PDSCH MCS - overall
- [x] 检查关于GP的公式 4g hour (gp agg 要改成sum)
- [x] 根据小区带宽画图: DL Spec Eff  / UL Spec Eff 
- [x] some charts need to span two columns
- [x] twin axis 的图里左右坐标轴颜色冲突问题
- [x] legend overlap for charts with many lines
- [x] 支持stackedBar
- [x] 添加Groupbar支持


# Known Bug
- [x] NaN value will clipping x axis at the beginning or end
  - Solution : https://stackoverflow.com/questions/34816098/matplotlib-how-to-plot-date-without-clipping-nan-at-the-beginning-and-end
- [x] unavail rate 需要考虑数据行数
- [x] 修正bar图overlap的问题: https://stackoverflow.com/questions/46175808/python-matplotlib-bars-overlapping-although-width-1

# Audit
|         | 2G_Hour | 2G_Daily | 4G_Hour | 4G_Daily | 5G_Hour | 5G_Daily |
|:-------:|:-------:|:--------:|:-------:|:--------:|:-------:|:--------:|
|   cell  |     X    |     X    |     X   |      X   |    X    |    X     |
|   site  |     X    |     X    |     X   |      X   |    X    |    X     |
| cluster |    X     |     X     |    X     |      X    |    X     |   X       |
|  layer  |    -     |    -      |     x   |      x    |    -    |     -    |

# Notes
- Qual & MCS	12	DL ReTXN Shares	QPSK 原公式错误

