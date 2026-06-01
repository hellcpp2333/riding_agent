## 1. 创建 CSS 设计系统 + 反模式修复

- [x] 1.1 创建 `static/css/style.css`（设计令牌、组件样式、焦点可见、无障碍、prefers-reduced-motion）
- [x] 1.2 在 `index.html` 中替换 `<style>` 为 `<link rel="stylesheet">`，修复反模式（transition:all → 显式属性，outline:none → focus-visible）

## 2. 认证页面改造

- [x] 2.1 添加品牌区域（渐变背景、图标、标题、副标题）
- [x] 2.2 重构表单卡片和 Element Plus 覆盖样式（44px 输入框、聚焦环、验证反馈）

## 3. Sidebar 和聊天界面

- [x] 3.1 优化 header/导航/会话控件（聚焦环、悬停态）
- [x] 3.2 重构消息气泡（颜色、间距、淡入动画）、工具指示器（脉冲）、输入框（聚焦光晕）

## 4. 路书管理和地图

- [x] 4.1 重新设计路书卡片（悬停/选中态、空状态）、导入按钮
- [x] 4.2 添加地图选中路书信息浮动卡片

## 5. 验证

- [x] 5.1 确认地图布局原样保留（#sidebar 380px + #map-container flex:1）
- [x] 5.2 确认无 transition:all、无裸 outline:none、所有加载文本使用 …、正确使用 &nbsp;
- [x] 5.3 确认所有现有功能正常
