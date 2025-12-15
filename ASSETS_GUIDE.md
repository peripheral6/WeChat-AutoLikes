# Assets 资源文件清单 - 截图指南

## 文件夹结构

你需要创建以下文件夹和文件：

```
WeChat-AutoLikes/
├── assets/
│   ├── pengyouquan.png      (1) 朋友圈图标
│   ├── dianzan.png          (2) 点赞按钮
│   ├── yizan.png            (3) 已点赞状态
│   ├── nozan.png            (4) 未点赞状态
│   ├── pinglun.png          (5) 评论按钮
│   └── fasong.png           (6) 发送按钮（可选）
├── wechat_automation_gui.py
├── wechat_core_engine.py
└── 其他文件...
```

## 每个文件的具体说明

### 1️⃣ `assets/pengyouquan.png` - 朋友圈图标

**用途**: 从微信主界面定位朋友圈按钮

**位置**: 微信主界面左侧导航栏中的朋友圈图标

**截图方法**:

```
1. 打开微信
2. 点击左侧导航栏的"朋友圈"（会变成选中状态）
3. 截图这个图标（就是那个圈形的图标）
4. 大小建议: 40x40 - 50x50 像素
5. 确保背景清晰，便于识别
```

**示例**:

- ⭕ 一个圆形图标，可能是灰色、蓝色或其他颜色
- 通常在"微信" "通讯录" "朋友圈" "我" 这一行中

---

### 2️⃣ `assets/dianzan.png` - 点赞按钮

**用途**: 识别点赞按钮的位置

**位置**: 朋友圈内容下方的点赞按钮

**截图方法**:

```
1. 打开朋友圈
2. 找到任意一条朋友圈内容
3. 在内容下方找到 "👍 赞" 这个按钮
4. 截图这个按钮（包括图标和文字）
5. 大小建议: 30x30 - 50x50 像素
6. 最好截取"赞"这个字或者拇指向上的图标
```

**示例**:

- 👍 拇指向上的图标，或者 "赞" 字
- 在 "评论" "分享" 按钮的左侧

---

### 3️⃣ `assets/yizan.png` - 已点赞状态

**用途**: 识别已经点赞过的状态（避免重复点赞）

**位置**: 点赞后，点赞按钮会变成"已赞"的样子

**截图方法**:

```
1. 打开朋友圈
2. 找到一条你已经点过赞的内容
3. 观察点赞按钮的样式（通常会变成蓝色或其他颜色）
4. 截图这个"已赞"的样子
5. 大小建议: 30x30 - 50x50 像素
```

**示例**:

- 👍 拇指图标变成了蓝色/红色
- 或者 "赞" 字变成了蓝色
- 或者出现 "✓ 已赞"

---

### 4️⃣ `assets/nozan.png` - 未点赞状态

**用途**: 识别未点赞的状态（还可以点赞）

**位置**: 点赞按钮默认的样子

**截图方法**:

```
1. 打开朋友圈
2. 找到一条你还没有点过赞的内容
3. 观察点赞按钮的样式（通常是灰色）
4. 截图这个"未赞"的样子
5. 大小建议: 30x30 - 50x50 像素
```

**示例**:

- 👍 拇指图标是灰色的
- 或者 "赞" 字是灰色的
- 或者显示为空心的样式

---

### 5️⃣ `assets/pinglun.png` - 评论按钮

**用途**: 识别评论按钮（当启用评论功能时）

**位置**: 点赞按钮右侧的评论按钮

**截图方法**:

```
1. 打开朋友圈
2. 在内容下方找到评论按钮
3. 截图这个按钮
4. 大小建议: 30x30 - 50x50 像素
5. 通常是一个"气泡"或"💬"的图标
```

**示例**:

- 💬 气泡图标，或者 "评论" 字
- 在点赞按钮的右侧

---

### 6️⃣ `assets/fasong.png` - 发送按钮（可选）

**用途**: 评论时的发送按钮（如果启用了评论功能）

**位置**: 评论输入框旁边的发送按钮

**截图方法**:

```
1. 打开朋友圈，点击某条内容的评论
2. 在评论输入框下方找到发送按钮
3. 截图这个按钮
4. 大小建议: 30x40 像素
```

**示例**:

- ➤ 箭头指向右边
- 或者 "发送" 字
- 或者飞机 ✈️ 图标

---

## 截图建议

### ✅ 好的截图

```
✓ 只截图需要的图标部分，不要包含太多周围内容
✓ 确保图标清晰，对比度高
✓ 大小统一（建议30-50像素）
✓ 背景简洁
✓ 选择灰色状态（未点赞）和蓝色状态（已点赞）的对比
```

### ❌ 不好的截图

```
✗ 太大（包含太多内容）
✗ 太小（看不清）
✗ 模糊或低对比度
✗ 包含其他UI元素造成混淆
✗ 背景复杂
```

---

## 如何准备这些文件

### 方法 1: 使用截图工具（推荐）

**Windows 内置截图工具**:

```
1. Windows + Shift + S (打开截图工具)
2. 框选要截图的区域
3. 自动保存到剪贴板
4. Ctrl + V粘贴到画图/PS中
5. 保存为PNG格式
```

**微信截图功能**:

```
1. 使用微信的截图功能 (Ctrl + Alt + A)
2. 框选图标
3. 保存
```

### 方法 2: 使用在线工具

- 粘贴到 https://www.photopea.com (在线 PS)
- 或者使用 Windows 自带的"画图"程序

### 方法 3: 使用 Python 截图脚本

```python
import pyautogui
from PIL import Image

# 手动截图朋友圈的某个区域
# 例如：截图坐标 (x1, y1, x2, y2)
screenshot = pyautogui.screenshot(region=(500, 600, 50, 50))
screenshot.save('assets/dianzan.png')

print("✅ 已保存到 assets/dianzan.png")
```

---

## 创建 assets 文件夹

### 使用命令行创建:

**Windows PowerShell**:

```powershell
# 进入项目目录
cd E:\GitHub\WeChat-AutoLikes

# 创建assets文件夹
mkdir assets

# 查看是否创建成功
dir assets
```

**或者直接在资源管理器中**:

```
1. 打开 E:\GitHub\WeChat-AutoLikes
2. 右键 -> 新建 -> 文件夹
3. 命名为 "assets"
```

---

## 文件格式要求

| 属性     | 要求               |
| -------- | ------------------ |
| **格式** | PNG (.png)         |
| **大小** | 30-50 像素（宽高） |
| **DPI**  | 72 DPI (标准)      |
| **颜色** | RGB 或 RGBA        |
| **压缩** | PNG 压缩           |

---

## 验证文件是否正确

### 1. 检查文件是否存在

```powershell
# 检查assets文件夹
dir E:\GitHub\WeChat-AutoLikes\assets

# 应该看到：
# dianzan.png
# yizan.png
# nozan.png
# pinglun.png
# pengyouquan.png
# fasong.png (可选)
```

### 2. 验证程序能找到文件

运行 Python 测试:

```python
from wechat_core_engine import get_resource_path
import os

files = [
    'assets/dianzan.png',
    'assets/yizan.png',
    'assets/nozan.png',
    'assets/pinglun.png',
    'assets/pengyouquan.png'
]

for file in files:
    path = get_resource_path(file)
    exists = os.path.exists(path)
    print(f"{'✅' if exists else '❌'} {file} - {path}")
```

**期望输出**:

```
✅ assets/dianzan.png - E:\GitHub\WeChat-AutoLikes\assets\dianzan.png
✅ assets/yizan.png - E:\GitHub\WeChat-AutoLikes\assets\yizan.png
... (全部为✅)
```

---

## 回到原始点赞方法

我需要恢复 `find_and_click_dianzan()` 函数的使用。修改之前添加的代码：

**在 `wechat_automation_gui.py` 或 `wechat_core_engine.py` 中**：

```python
# 恢复原始的点赞方法
if find_and_click_dianzan(
    target_name,
    name_position,
    max_scroll_attempts=5,
    enable_comment=enable_comment,
    comment_text=comment_text,
    stop_flag_func=stop_flag_func
):
    print(f"✅ 成功给 {target_name} 点赞！")
    return True
```

不使用新的 `simple_click_dianzan_by_position()` 方法。

---

## 总结清单

准备资源文件的步骤：

- [ ] 1. 创建 `assets/` 文件夹
- [ ] 2. 截图 `pengyouquan.png` (朋友圈图标)
- [ ] 3. 截图 `dianzan.png` (点赞按钮)
- [ ] 4. 截图 `yizan.png` (已点赞状态)
- [ ] 5. 截图 `nozan.png` (未点赞状态)
- [ ] 6. 截图 `pinglun.png` (评论按钮)
- [ ] 7. 截图 `fasong.png` (发送按钮 - 可选)
- [ ] 8. 运行验证脚本确认文件存在
- [ ] 9. 测试程序是否能识别这些图标

---

## 需要帮助?

如果在截图或保存时遇到问题：

1. 确保 PNG 格式（不要用 JPG）
2. 确保文件名完全正确（大小写敏感）
3. 确保放在正确的 `assets/` 文件夹中
4. 如果有任何问题，告诉我文件名和大小

---

**更新日期**: 2025-12-14  
**方案**: 用户自己提供 assets 截图  
**优势**: 可根据实际 UI 精确匹配  
**工作量**: 中等 (需要截图 6 个文件)
