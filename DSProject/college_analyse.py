import pandas as pd
from pyecharts.charts import Bar, Pie, Geo, Liquid
from pyecharts.commons.utils import JsCode
from pyecharts import options as opts
from pyecharts.globals import ChartType, CurrentConfig, NotebookType

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

# 通过panda库读取csv文件并对数据再次进行去重、清洗操作
df = pd.read_csv("college_data.csv")
df_new = df.drop_duplicates(subset=['name'])

# 获取各地区院校数量
df_site = df_new[df_new['site'] != '——']
df_site = df_site[df_site['site'] != '------']
site_counts = df_site['site'].value_counts()
dict_site = {'name': site_counts.index, 'counts': site_counts.values}
# data存储着各地区的院校数量
data_site = pd.DataFrame(dict_site)

# 高校质量分析
df_title = df_new[df_new['title'] != '——']
# 获取各地区985院校数量
df_985 = df_title[df_title['title'] == '211985']
site_counts_985 = df_985['site'].value_counts()
dict_site_985 = {'name': site_counts_985.index, 'counts': site_counts_985.values}
data_985 = pd.DataFrame(dict_site_985)
# 获取各地区211院校数量
df_211 = df_title[df_title['title'] == '211']
df_211 = pd.concat([df_211, df_985], ignore_index=True)
site_counts_211 = df_211['site'].value_counts()
dict_site_211 = {'name': site_counts_211.index, 'counts': site_counts_211.values}
data_211 = pd.DataFrame(dict_site_211)

# 高校类型分析
df_type = df_new[df_new['type'] != '——']
df_type = df_type[df_type['type'] != '------']
df_type_counts = df_type['type'].value_counts()
dict_type_counts = {'name': df_type_counts.index, 'counts': df_type_counts.values}
data_type_counts = pd.DataFrame(dict_type_counts)

#高校属性分析
df_nature = df_new[df_new['nature'] != '——']
df_nature = df_nature[df_nature['nature'] != '------']
df_nature_counts = df_nature['nature'].value_counts()
dict_nature_counts = {'name': df_nature_counts.index, 'counts': df_nature_counts.values}
data_nature_counts = pd.DataFrame(dict_nature_counts)

# 绘制各城市高校数量柱形图
bar = Bar()
bar.add_xaxis(data_site['name'].values.tolist())
bar.add_yaxis("", data_site['counts'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
    title_opts=opts.TitleOpts(title="中国各省市高校数量",subtitle="王麒翔"),
    datazoom_opts=opts.DataZoomOpts(type_= "inside"),
)
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(240, 128, 128, 1)' 
                }, {
                    offset: 1,
                    color: 'rgba(255, 99, 71, 1)'
                }], false)"""),
                "barBorderRadius": [42, 42, 42, 42],
                "shadowColor": 'rgb(0, 160, 142)',
            }})
bar.render("中国各省市高校数量.html")

# 绘制中国高校分布热力图
geo = Geo()
geo.add_schema(maptype="china", zoom=1.2)
geo.add("中国高校分布热力图", [list(z) for z in zip(data_site['name'].values.tolist(), data_site['counts'].values.tolist())],
       type_=ChartType.HEATMAP,symbol_size = 15, is_large=True, label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title="中国高校分布热力图",subtitle="王麒翔"),
        )
geo.render("中国高校分布热力图.html")

# 绘制985高校分布饼状图
pie = Pie()
pie.add("", [list(z) for z in zip(data_985['name'].values.tolist(), data_985['counts'].values.tolist())],
       radius=["30%", "75%"],
            center=["40%", "50%"],
            rosetype="radius")
pie.set_global_opts(
            title_opts=opts.TitleOpts(title="中国各省市985高校数量排行",subtitle="王麒翔"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ),
        )
pie.render("中国各省市985高校数量排行.html")

# 绘制各城市985高校数量柱形图
bar = Bar()
bar.add_xaxis(data_985['name'].values.tolist())
bar.add_yaxis("", data_985['counts'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
    title_opts=opts.TitleOpts(title="中国各省市985高校数量", subtitle="王麒翔"),
    datazoom_opts=opts.DataZoomOpts(type_= "inside"),
)
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [42, 42, 42, 42],
                "shadowColor": 'rgb(0, 160, 155)',
            }})
bar.render("中国各省市985高校数量.html")

# 绘制211高校分布饼状图
pie = Pie()
pie.add("", [list(z) for z in zip(data_211['name'].values.tolist(), data_211['counts'].values.tolist())],
       radius=["30%", "75%"],
            center=["40%", "50%"],
            rosetype="radius")
pie.set_global_opts(
            title_opts=opts.TitleOpts(title="中国各省市211高校数量排行", subtitle="王麒翔"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ),
        )
pie.render("中国各省市211高校数量排行.html")

# 绘制各城市211高校数量柱形图
bar = Bar()
bar.add_xaxis(data_211['name'].values.tolist())
bar.add_yaxis("", data_211['counts'].values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
    title_opts=opts.TitleOpts(title="中国各省市211高校数量", subtitle="王麒翔"),
    datazoom_opts=opts.DataZoomOpts(type_= "inside"),
)
bar.set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [42, 42, 42, 42],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
bar.render("中国各省市211高校数量.html")

sum_counts = data_211['counts'].sum()
data_211['rate'] = data_211['counts'].apply(lambda x : x/sum_counts)

# 绘制中国高质量高校分布热力图
geo = Geo()
geo.add_schema(maptype="china")
geo.add("中国高质量高校分布热力图", [list(z) for z in zip(data_211['name'].values.tolist(), data_211['counts'].values.tolist())],
       type_=ChartType.HEATMAP)
geo.set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=30),
            title_opts=opts.TitleOpts(title="中国高质量高校分布热力图", subtitle="王麒翔"),
        )
geo.render("中国高质量高校分布热力图.html")

# 绘制中国占比前十城市高质量高校占比
liquid = Liquid()
liquid.add('', [sum(data_211['rate'].values[:11])])
liquid.set_global_opts(title_opts=opts.TitleOpts(title="中国高质量高校最多的十个城市拥有的高质量高校在整个国家中的占比", subtitle="王麒翔"))
liquid.render("中国占比前十城市高质量高校占比.html")

# 绘制中国高校类型分析饼状图
pie = Pie()
pie.add("", [list(z) for z in zip(data_type_counts['name'].values.tolist(), data_type_counts['counts'].values.tolist())],
       radius=["30%", "75%"],
            center=["40%", "50%"],
            rosetype="radius")
pie.set_global_opts(
            title_opts=opts.TitleOpts(title="中国高校类型分析", subtitle="王麒翔"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ),
        )
pie.render("中国高校类型分析饼状图.html")


# 绘制中国高校属性分析饼状图
pie = Pie()
pie.add("", [list(z) for z in zip(data_nature_counts['name'].values.tolist(), data_nature_counts['counts'].values.tolist())],
    )
pie.set_global_opts(
            title_opts=opts.TitleOpts(title="中国高校属性分析", subtitle="王麒翔"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ),
        )
pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}: {d}%"))
pie.render("中国高校属性分析饼状图.html")
