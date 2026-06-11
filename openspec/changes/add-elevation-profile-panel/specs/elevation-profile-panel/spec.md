## ADDED Requirements

### Requirement: Map container height reduction
地图容器 SHALL 占主内容区高度的 3/4（原为 100%），为下方路线数据面板腾出 1/4 高度空间。

#### Scenario: Map resizes correctly
- **WHEN** 用户登录后进入主界面
- **THEN** 地图容器高度为主内容区的 75%，下方空出 25% 高度给路线数据面板

### Requirement: Route stats summary display
路线数据面板 SHALL 在上方 1/5 区域显示三项关键指标：距离（公里制，数值下方标注"距离"）、累计爬升（米制，数值下方标注"累计爬升"）、累计下降（米制，数值下方标注"累计下降"）。

#### Scenario: Route data displayed after planning
- **WHEN** 路线规划完成且收到 elevation 事件
- **THEN** 面板显示 "XX.X km" 标注"距离"、"XXX m" 标注"累计爬升"、"XXX m" 标注"累计下降"

#### Scenario: Panel empty before route
- **WHEN** 尚未规划任何路线
- **THEN** 面板显示占位提示"规划路线后将显示数据"

### Requirement: Elevation profile chart
路线数据面板 SHALL 在下方 4/5 区域使用 Canvas 绘制海拔剖面图：仅用半透明渐变填充区域表现地形轮廓，不绘制折线描边。纵轴为海拔高度（m），横轴为距离（km）。

#### Scenario: Chart renders with elevation data
- **WHEN** 收到 elevation 事件且包含轨迹点数组
- **THEN** Canvas 绘制纯填充面积海拔剖面图（无折线描边），渐变填充 + 坐标轴标注，横轴为距离（km），纵轴为海拔（m）

#### Scenario: Chart handles empty data
- **WHEN** 路线无高程数据
- **THEN** 图表区域显示"暂无高程数据"

### Requirement: Visual style consistency
路线数据面板 SHALL 遵循项目 earth-tone 设计系统，使用 --color-surface 背景、--color-border 边框、--radius-lg 圆角。

#### Scenario: Panel matches design system
- **WHEN** 面板渲染完成
- **THEN** 面板背景色、边框色、圆角与项目其他卡片组件一致
