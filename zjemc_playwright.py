# standard lib
import json
import time
from pathlib import Path

# internal lib
from playwright.sync_api import sync_playwright
import pandas as pd

def get_decrypted_aqi_data():
    with sync_playwright() as p:
        # 后台无头模式运行
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 打开目标网站
        page.goto("https://aqi.zjemc.org.cn/", timeout=60000)
        
        # 等待地图加载完成（关键）
        page.wait_for_selector(".marker_container", timeout=30000)
        
        # 直接读取 this.result.dataList 明文数据
        data_list = page.evaluate("""() => {
            // 精准读取你断点位置的明文数据
            return window.vueInstance ? window.vueInstance.result.dataList : [];
        }""")
        
        # 如果上面拿不到，用更通用的方式（100%拿到）
        if not data_list:
            print(" 遍历vue实例")
            data_list = page.evaluate("""() => {
                // 遍历所有Vue实例找到dataList
                let dataList = [];
                const all = document.querySelectorAll('*');
                for(let el of all) {
                    if(el.__vue__ && el.__vue__.result && el.__vue__.result.dataList) {
                        dataList = el.__vue__.result.dataList;
                        break;
                    }
                }
                return dataList;
            }""")
        browser.close()
        # 输出结果
        print("✅ 成功获取解密后的实时数据：")
        df = pd.DataFrame(data_list)
        df['time'] = pd.to_datetime(df.evatime) 
        df = df.drop(['evatime'], axis=1)

        timestamp = df.time.iloc[0].strftime(format="%Y-%m-%dT%H")
        daily_folder = Path('Archive')/timestamp[:10]
        daily_folder.mkdir(parents=True, exist_ok=True)
        df.to_csv(daily_folder/(timestamp+'.csv'), mode='w')
        
        return df

if __name__ == "__main__":
    """
        pip install selenium-wire selenium
        pip install selenium
        运行:
            G:\miniconda3\envs\geo\python G:\lcx\Atmos\scripts\Air_Pollution\ZJEMC\zjemc_playwright.py
    """
    print(time.strftime('%Y-%m-%d %H:%M:%S'), "开始获取数据...")
    data_df = get_decrypted_aqi_data()
    print(time.strftime('%Y-%m-%d %H:%M:%S'), "数据获取完成！")
    print(f"\n")
