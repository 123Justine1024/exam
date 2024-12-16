import pandas as pd
import re
from bs4 import BeautifulSoup

# 解析保存的 HTML 文件
with open("gdp_2023.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 初始化数据存储
data = []

# 遍历所有表格行 <tr>
for row in soup.select("tbody tr"):  # 选择 <tbody> 下的所有 <tr>
    cells = row.find_all("td")  # 获取当前行的所有单元格
    if len(cells) >= 5:  # 确保行结构完整（至少 5 列）
        country_or_region = cells[1].get_text(strip=True)  # 第二列：国家或地区
        continent = cells[2].get_text(strip=True) if len(cells) > 2 else None  # 第三列：洲
        gdp_text = cells[3].get_text(strip=True)  # 第四列：GDP 原始数据

        # 提取括号内的 GDP 数值
        gdp_value_match = re.search(r"\(([\d,]+)\)", gdp_text)  # 匹配括号内的数字
        gdp_value = int(gdp_value_match.group(1).replace(",", "")) if gdp_value_match else None

        # 存储清洗后的数据
        data.append((country_or_region, continent, gdp_value))

# 转为 Pandas DataFrame
df = pd.DataFrame(data, columns=["Country/Region", "Continent", "GDP (Numeric)"])
df = df[df["Country/Region"] != "欧盟地区"]

# 查看 DataFrame 的形状
shape = df.shape
print(shape)
# Step 1: Group by continent and calculate total GDP per continent
continent_gdp = df.groupby('Continent')['GDP (Numeric)'].sum()
print(continent_gdp)
# Step 2: Calculate the world GDP
world_gdp = df['GDP (Numeric)'].sum()

# Step 3: Calculate the share of each continent in the world GDP
continent_gdp_share = (continent_gdp / world_gdp) * 100

# Step 4: Combine the total GDP and share into a DataFrame
gdp_summary = pd.DataFrame({
    'Total GDP': continent_gdp,
    'GDP Share (%)': continent_gdp_share
}).reset_index()

# Output the results
print(gdp_summary)
