# 错误修复记录 - ensure_wechat_is_active 参数错误

## 问题

运行"给所有人点赞"功能时报错：

```
❌ 给所有人点赞功能出错: ensure_wechat_is_active() got an unexpected keyword argument 'target_window_keyword'
```

## 原因

`pengyouquan_like_all_action()` 函数调用时使用了错误的参数：

```python
# ❌ 错误的调用方式
if not ensure_wechat_is_active(target_window_keyword="朋友圈"):
```

但 `ensure_wechat_is_active()` 函数的定义不接受任何参数：

```python
# ✅ 正确的函数签名
def ensure_wechat_is_active():
```

## 解决方案

修改调用方式，移除不支持的参数：

```python
# ✅ 正确的调用方式
if not ensure_wechat_is_active():
```

## 修改位置

**文件**: `wechat_core_engine.py`
**函数**: `pengyouquan_like_all_action()`
**行号**: 约 2960-2968

## 修改内容

```python
# 之前（第2962行）：
if not ensure_wechat_is_active(target_window_keyword="朋友圈"):
    print("❌ 朋友圈窗口未激活")
    if status_callback:
        status_callback("❌ 朋友圈窗口未激活，无法继续")

# 之后：
if not ensure_wechat_is_active():
    print("❌ 微信窗口未激活")
    if status_callback:
        status_callback("❌ 微信窗口未激活，无法继续")
```

## 验证

✅ 修复已应用  
✅ 函数可正常导入  
✅ GUI 程序正常启动  
✅ 错误已解决

## 后续测试

现在可以正常测试"给所有人点赞"功能。运行步骤：

1. 打开朋友圈
2. 在 GUI 中选择"给所有人点赞"模式
3. 点击"▶ 开始点赞"
4. 观察日志和循环检测计数器

---

修复日期: 2025-12-14
状态: ✅ 已完成
