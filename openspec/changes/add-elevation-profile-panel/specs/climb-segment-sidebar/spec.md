## ADDED Requirements

### Requirement: Climb segment detection on route
前端 SHALL 基于高程轨迹点数据，按 UCI 规则识别爬坡段：坡度 >= 3% 且连续长度 >= 500m 的区段合并为一个爬坡段。

#### Scenario: Climb segments detected
- **WHEN** 路线高程数据包含满足 UCI 标准的爬坡段
- **THEN** 地图路线对应区段以不同颜色标记（坡度色阶）

#### Scenario: No climb segments
- **WHEN** 路线全程坡度均 < 3% 或爬坡长度 < 500m
- **THEN** 不显示爬坡标记，侧边栏不出现切换入口

### Requirement: Climb segment color coding on map
地图路线上的爬坡段 SHALL 按坡度等级着色：绿色（<3%，无爬坡）、黄色（3-6%）、橙色（6-9%）、红色（9-12%）、深红色（>12%）。非爬坡段保持默认蓝色。

#### Scenario: Color-coded climb segments rendered
- **WHEN** 路线包含多个不同坡度的爬坡段
- **THEN** 地图上对应路段按坡度等级显示对应颜色

### Requirement: Climb sidebar panel
爬坡段侧边栏 SHALL 从右侧滑出（overlay 模式），顶部显示"第 X 个/共 Y 个"爬坡段切换控件，中间显示当前爬坡段详情（难度等级、平均坡度、距离、累计爬升），下方显示该爬坡段的海拔-距离图。

#### Scenario: Sidebar opens with climb data
- **WHEN** 用户点击地图上的爬坡段标记或切换按钮
- **THEN** 侧边栏从右侧滑入，显示当前爬坡段详情

#### Scenario: Navigate between climbs
- **WHEN** 用户点击"上一个"/"下一个"按钮
- **THEN** 侧边栏内容切换为对应爬坡段，地图高亮对应区段

#### Scenario: Close sidebar
- **WHEN** 用户点击关闭按钮或侧边栏外部遮罩
- **THEN** 侧边栏滑出消失

### Requirement: Climb segment elevation chart
爬坡段侧边栏内的海拔图 SHALL 以不同颜色标记坡度等级：绿色 <3%、黄色 3-6%、橙色 6-9%、红色 9-12%、深红色 >12%。图表 SHALL 采用纯填充面积图（无折线描边），填充色随坡度等级变化。

#### Scenario: Gradient-colored chart segments
- **WHEN** 爬坡段海拔图渲染
- **THEN** 海拔剖面图按坡度等级分段着色填充，颜色从绿到深红对应坡度由易到难

### Requirement: Sidebar style consistency
爬坡段侧边栏 SHALL 遵循 earth-tone 设计系统，使用相同的颜色变量和圆角规范。

#### Scenario: Sidebar matches design system
- **WHEN** 侧边栏渲染
- **THEN** 样式与项目其他面板一致
