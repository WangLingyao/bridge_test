from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import Strategy
import json

app=FastAPI()

#定义请求
class BacktestRequest(BaseModel):
    stock_code:str='000001.SZ'
    start_date:str='20230101'
    end_date:str='20231231'
    principal:float=1000000
    buy_percent:float=0.2

backtest_results={}


@app.post("/Strategy")
async def start_backtest(request: BacktestRequest):
    stock_code = request.stock_code
    start_date = request.start_date
    end_date = request.end_date
    principal = request.principal
    buy_percent = request.buy_percent

    # 调用回测函数
    results = Strategy.run_backtest(stock_code, start_date, end_date, principal, buy_percent)

    if not results:
        raise HTTPException(status_code=400, detail="Backtest failed or no results generated")

    backtest_results["last"] = results

    return results


@app.get("/results")
async def get_results():
    # 检查是否有回测结果
    if "last" not in backtest_results:
        raise HTTPException(status_code=404, detail="No backtest results available")

    return backtest_results["last"]
