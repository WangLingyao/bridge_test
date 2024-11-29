# 回测框架与api使用说明
回测框架搭建：backtrader

数据下载来源：tushare

策略：当12日的价格均线穿越26日的价格均线时买入。当价格跌破26均线时卖出。


[前言]

尊敬的面试官~您好！

我在此之前没有使用backtrader的经历，也无fastapi连接前后端启用经验，因此本框架是这两天自己靠着网络资源（CSDN，B站 ，GPT提问等）初学的，如有不完善的地方请您谅解！感谢！


[文件使用说明]

Strategy.py:回测框架

注：其中tushare使用的TOCKEN为本人账号，如需使用您可以填充自己的TOCKEN

您需要做的：

1、在该文件夹下（backtest文件夹）的终端输入：uvicorn api:app --reload

若成功会出现以下文字

![image](https://github.com/user-attachments/assets/fb387a26-2fd1-4e83-b4e6-6f48c5f97c22)

2、打开request.py文件，输入您想要回测的股票代码（沪深300），回测周期，以及您的初始资金和每次买入想要的比例

 （若不改动默认为平安银行，回测周期为2023年1月1日到12月31日。本金为1,000,000,每次买入为本金的百分之20）
 
3、进行完这一步您应该可以看到结果，如下图所示：（200表示输出成功的状态）

![image](https://github.com/user-attachments/assets/592964a4-e1ef-42f8-8153-557835b5e88c)


4、您也可以在浏览器访问“http://127.0.0.1:8000/results”看到相同的结果

<img width="446" alt="image" src="https://github.com/user-attachments/assets/8cb1e49f-c240-4f0d-9d12-d7ee80c77346">



除此之外，我还用cerebro.plot()画了一下策略执行的折线图

![image](https://github.com/user-attachments/assets/bb857171-f5f2-4767-a3db-59945a7cfa40)



[其他补充]：

此策略在平安银行上貌似是有亏损的，但测试过程中我发现在000004.SZ国农科技是可以盈利的，或许可以构建更好的投资组合 

通过这个面试项目，我发现使用backtrader进行回测更加便捷，也在短时间内收获了很多新的知识。

期待您能给我更多的指导！



