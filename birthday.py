import sys
import os
# 添加本地库路径
sys.path.insert(0, './libs')
from datetime import datetime, timedelta
import requests
import json

from lunarcalendar import Converter, Solar, Lunar

# 生日数据
lunar_data = [
    {"name": "树文", "month": 6, "day": 23, "is_lunar": True},
    {"name": "必兴", "month": 2, "day": 11, "is_lunar": False},
    {"name": "兆霖", "month": 12, "day": 10, "is_lunar": False},
    {"name": "文希", "month": 3, "day": 18, "is_lunar": False},
    {"name": "彤彤", "month": 10, "day": 29, "is_lunar": False},
    {"name": "付禹", "month": 2, "day": 15, "is_lunar": False},
    {"name": "绍安", "month": 7, "day": 27, "is_lunar": True},
    {"name": "志强", "month": 5, "day": 23, "is_lunar": False},
    {"name": "平安", "month": 2, "day": 5, "is_lunar": False},
    {"name": "张超", "month": 3, "day": 6, "is_lunar": False},
    {"name": "思巍", "month": 9, "day": 8, "is_lunar": False},
    {"name": "王勇", "month": 6, "day": 18, "is_lunar": False},
    {"name": "后同", "month": 9, "day": 7, "is_lunar": False},
    {"name": "朱紫云", "month": 11, "day": 16, "is_lunar": False},
    {"name": "王伟勇", "month": 3, "day": 17, "is_lunar": True},
    {"name": "静茹姐", "month": 12, "day": 24, "is_lunar": False},
    {"name": "刘贤程", "month": 6, "day": 8, "is_lunar": False},
    {"name": "任锦梅", "month": 4, "day": 18, "is_lunar": True},
    {"name": "熊紫晴", "month": 10, "day": 24, "is_lunar": False},
    {"name": "周盈", "month": 1, "day": 10, "is_lunar": False},
    {"name": "邬伊美", "month": 5, "day": 13, "is_lunar": False},
    {"name": "胡王光", "month": 7, "day": 14, "is_lunar": False},
    {"name": "沈玮姐", "month": 6, "day": 21, "is_lunar": True},
    {"name": "哲昂", "month": 6, "day": 15, "is_lunar": True},
    {"name": "露仁", "month": 3, "day": 19, "is_lunar": False},
    {"name": "陈欢", "month": 5, "day": 15, "is_lunar": False},
    {"name": "游航", "month": 5, "day": 20, "is_lunar": False},
    {"name": "重阳", "month": 9, "day": 9, "is_lunar": True},
    {"name": "张乐", "month": 10, "day": 30, "is_lunar": False},
    {"name": "泽明", "month": 1, "day": 12, "is_lunar": False},
    {"name": "可婷", "month": 12, "day": 20, "is_lunar": True},
    {"name": "黄儒", "month": 4, "day": 27, "is_lunar": True},
    {"name": "景如", "month": 1, "day": 15, "is_lunar": False},
    {"name": "可媖", "month": 8, "day": 6, "is_lunar": False},
    {"name": "弋欣", "month": 1, "day": 29, "is_lunar": False},
    {"name": "常春", "month": 8, "day": 12, "is_lunar": True}
]

new_data = [
    {"name": "宣召", "month": 3, "day": 10, "is_lunar": False},
    {"name": "厚恩", "month": 4, "day": 25, "is_lunar": False},
    {"name": "无暇", "month": 4, "day": 28, "is_lunar": False},
    {"name": "超群", "month": 12, "day": 25, "is_lunar": True},
    {"name": "宇希", "month": 10, "day": 3, "is_lunar": False},
    {"name": "文涛", "month": 9, "day": 18, "is_lunar": False},
    {"name": "永志", "month": 2, "day": 6, "is_lunar": False},
    {"name": "恩赐", "month": 11, "day": 18, "is_lunar": False},
    {"name": "王丽", "month": 1, "day": 25, "is_lunar": False},
    {"name": "黎城", "month": 2, "day": 16, "is_lunar": False},
    {"name": "阳兴", "month": 8, "day": 21, "is_lunar": False},
    {"name": "光锐", "month": 4, "day": 7, "is_lunar": False},
    {"name": "婉婷", "month": 12, "day": 20, "is_lunar": False},
    {"name": "嘉靖", "month": 8, "day": 4, "is_lunar": False},
    {"name": "test", "month": 6, "day": 9, "is_lunar": False},
    {"name": "test2", "month": 6, "day": 10, "is_lunar": False},
]

# 合并所有数据
all_birthdays = lunar_data + new_data

def get_birthday_date(birthday, year):
    """获取某年的生日日期（公历）"""
    if birthday["is_lunar"]:
        lunar = Lunar(year, birthday["month"], birthday["day"], isleap=False)
        return Converter.Lunar2Solar(lunar)
    else:
        return Solar(year, birthday["month"], birthday["day"])

def check_upcoming_birthdays():
    """检查今天和明天的生日"""
    # 获取当前北京时间
    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    today = beijing_now.date()
    tomorrow = today + timedelta(days=1)
    
    print(f"当前北京时间：{beijing_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"检查日期：今天 {today}，明天 {tomorrow}")
    print("=" * 50)
    
    today_birthdays = []
    tomorrow_birthdays = []
    
    for birthday in all_birthdays:
        # 检查今年和明年（跨年情况）
        for year_offset in [0, 1]:
            year = today.year + year_offset
            solar_date = get_birthday_date(birthday, year)
            check_date = solar_date.to_date()
            
            # 确定日期显示格式
            if birthday["is_lunar"]:
                date_str = f"农历{birthday['month']}月{birthday['day']}日"
            else:
                date_str = f"{birthday['month']}月{birthday['day']}日"
            
            if check_date == today:
                today_birthdays.append({
                    "name": birthday["name"],
                    "date_str": date_str,
                    "is_lunar": birthday["is_lunar"]
                })
            elif check_date == tomorrow:
                tomorrow_birthdays.append({
                    "name": birthday["name"],
                    "date_str": date_str,
                    "is_lunar": birthday["is_lunar"]
                })
    
    return today_birthdays, tomorrow_birthdays

def send_pushplus_message(title, content):
    """发送 PushPlus 消息"""
    my_token = os.environ.get('MY_TOKEN')
    test_token = os.environ.get('TEST_TOKEN')
    
    if not my_token:
        print("错误：MY_TOKEN 未设置")
        return False
    
    data = {
        "token": my_token,
        "title": title,
        "content": content,
        "template": "txt"
    }
    
    if test_token:
        data["to"] = test_token
        print(f"将发送给好友")
    
    try:
        response = requests.post("https://www.pushplus.plus/api/send", json=data, timeout=10)
        result = response.json()
        print(f"API 响应: {result}")
        
        if result.get('code') == 200:
            print("✓ 消息发送成功！")
            return True
        else:
            print(f"✗ 消息发送失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False

def main():
    print("=" * 50)
    print("生日提醒程序启动")
    print("=" * 50)
    
    # 检查生日
    today_birthdays, tomorrow_birthdays = check_upcoming_birthdays()
    
    # 构建消息内容
    message_lines = []
    
    # 生成标题
    title_parts = []
    if today_birthdays:
        names = [b["name"] for b in today_birthdays]
        title_parts.append(f"今日生日：{', '.join(names)}")
    if tomorrow_birthdays:
        names = [b["name"] for b in tomorrow_birthdays]
        title_parts.append(f"明日生日：{', '.join(names)}")
    
    if title_parts:
        title = "🎂 " + " | ".join(title_parts)
    else:
        title = "📅 生日提醒"
    
    if today_birthdays:
        message_lines.append("🎂 【今日生日】 🎂")
        for b in today_birthdays:
            message_lines.append(f"  {b['name']} · {b['date_str']}")
        message_lines.append("")
    
    if tomorrow_birthdays:
        message_lines.append("🎁 【明日生日】 🎁")
        for b in tomorrow_birthdays:
            message_lines.append(f"  {b['name']} · {b['date_str']}")
        message_lines.append("")
    
    if not today_birthdays and not tomorrow_birthdays:
        message_lines.append("📅 今天和明天都没有生日")
        print("没有生日需要提醒")
    else:
        print("找到以下生日：")
        for line in message_lines:
            print(line)
    
    message_lines.append("")
    message_lines.append("---")
    beijing_now = datetime.utcnow() + timedelta(hours=8)
    message_lines.append(f"⏰ 提醒时间：{beijing_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    content = "\n".join(message_lines)
    
    # 发送消息
    if today_birthdays or tomorrow_birthdays:
        print("\n正在发送提醒消息...")
        print(f"标题：{title}")
        send_pushplus_message(title, content)
    else:
        print("\n没有生日，跳过发送")
    
    print("=" * 50)
    print("程序执行完成")
    print("=" * 50)

if __name__ == "__main__":
    main()