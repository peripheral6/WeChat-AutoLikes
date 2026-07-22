#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Auto-Likes 优化补丁脚本
安全修改 wechat_core_engine.py 和 wechat_automation_gui.py
"""

import os
import sys

def read_file(path):
    """读取文件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    """写入文件内容"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def check_syntax(path):
    """检查Python语法"""
    import py_compile
    try:
        py_compile.compile(path, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(f"语法错误: {e}")
        return False

def apply_popup_verification_fix(core_engine_path):
    """修复 check_and_perform_dianzan 的弹窗验证"""
    content = read_file(core_engine_path)

    old_code = '''        # 点击点赞按钮弹出界面
        print(f"🎯 准备点击目标点赞点: ({dianzan_position[0]},{dianzan_position[1]})")
        pyautogui.click(dianzan_position[0], dianzan_position[1])
        print("✅ 已点击点赞按钮，等待界面弹出...")
        time.sleep(1.5)  # 等待界面弹出

        # 验证弹窗是否真的出现了（通过像素方差检查）
        try:
            popup_check_region = (
                max(0, dianzan_position[0] - 80),
                max(0, dianzan_position[1] - 20),
                300, 180
            )
            popup_shot = pyautogui.screenshot(region=popup_check_region)
            popup_array = np.array(popup_shot).astype(np.float32)
            # 弹窗会引入明显的视觉变化（半透明覆盖层或对话框）
            # 计算像素方差：如果有弹窗，颜色多样性会增加
            variance = np.var(popup_array)
            if variance < 50:  # 阈值：低于此值说明界面没有明显变化
                print("⚠️ 未检测到点赞弹窗出现（界面无明显变化），跳过图标检测")
                return False
            else:
                print(f"✅ 检测到界面变化（方差={variance:.1f}），弹窗已出现")
        except Exception as ve:
            print(f"⚠️ 弹窗验证过程异常: {ve}")'''

    new_code = '''        # ===== 前后截图对比验证弹窗是否出现 =====
        click_x, click_y = dianzan_position
        verify_region = (max(0, click_x - 100), max(0, click_y - 50), 250, 120)

        try:
            before_shot = pyautogui.screenshot(region=verify_region)
            before_hash = hashlib.md5(np.array(before_shot).tobytes()).hexdigest()
        except Exception:
            before_hash = None

        print(f"🎯 准备点击目标点赞点: ({click_x},{click_y})")
        pyautogui.click(click_x, click_y)
        print("✅ 已点击点赞按钮，等待界面弹出...")
        time.sleep(1.5)

        try:
            after_shot = pyautogui.screenshot(region=verify_region)
            after_hash = hashlib.md5(np.array(after_shot).tobytes()).hexdigest()
            if before_hash and before_hash == after_hash:
                print("⚠️ 未检测到点赞弹窗出现（点击前后界面无变化），跳过图标检测")
                return False
            else:
                print("✅ 检测到界面变化，弹窗已出现")
        except Exception as ve:
            print(f"⚠️ 弹窗截图验证异常: {ve}")'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        write_file(core_engine_path, content)
        print("[OK] Fixed popup verification in check_and_perform_dianzan")
        return True
    else:
        print("[WARN] Could not find popup verification code to replace")
        return False

def add_ocr_fallback(core_engine_path):
    """添加OCR后备点赞方案"""
    content = read_file(core_engine_path)

    old_code = '''        except:
            pass

        print("⚠️ 无法执行点赞操作")
        return False

    except Exception as e:
        print(f"❌ 检测点赞状态失败: {e}")
        return False'''

    new_code = '''        except:
            pass

        # OCR后备：检测弹窗中的"赞"文字
        print("⚠️ 模板匹配未成功，尝试OCR检测'赞'文字...")
        try:
            ocr_region = pyautogui.screenshot(region=(
                max(0, click_x - 100), max(0, click_y - 50), 250, 120
            ))
            ocr_results = ocr_engine.recognize_text(np.array(ocr_region)) if ocr_engine else []
            if ocr_results:
                for det in ocr_results:
                    if len(det) >= 2:
                        text = str(det[1])
                        if "赞" in text or "取消" in text:
                            print(f"✅ OCR检测到操作栏文字'{text}'，点击确认")
                            bbox = det[0]
                            xs = [pt[0] for pt in bbox]
                            ys = [pt[1] for pt in bbox]
                            target_x = int(sum(xs) / len(xs)) + max(0, click_x - 100)
                            target_y = int(sum(ys) / len(ys)) + max(0, click_y - 50)
                            pyautogui.click(target_x, target_y)
                            time.sleep(1)
                            print("👍 OCR后备点赞操作完成")
                            return True
        except Exception as ocr_e:
            print(f"⚠️ OCR后备检测失败: {ocr_e}")

        print("⚠️ 无法执行点赞操作")
        return False

    except Exception as e:
        print(f"❌ 检测点赞状态失败: {e}")
        return False'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        write_file(core_engine_path, content)
        print("[OK] Added OCR fallback to check_and_perform_dianzan")
        return True
    else:
        print("[WARN] Could not find insertion point for OCR fallback")
        return False

def add_auto_detect_like_function(core_engine_path):
    """添加自动识别辅助点赞函数"""
    content = read_file(core_engine_path)

    auto_detect_func = '''

# ==================== 自动识别辅助点赞功能 ====================

def auto_detect_and_like_current_post(ocr_engine_ref=None):
    """
    自动识别当前朋友圈可见帖子的点赞按钮并点赞

    流程：
    1. 截取朋友圈窗口区域
    2. OCR识别所有用户名和点赞按钮
    3. 映射用户名到点赞按钮
    4. 对第一个可见帖子执行点赞
    5. 滚动到下一个帖子

    Returns:
        bool: 是否成功点赞至少一个帖子
    """
    print("\\n🔍 开始自动识别当前可见帖子...")

    if ocr_engine_ref and ocr_engine_ref.is_available():
        try:
            # 获取朋友圈窗口区域
            pengyouquan_region = get_pengyouquan_window_region(None, enable_window_resize=False)

            if not pengyouquan_region:
                print("❌ 无法获取朋友圈窗口区域")
                return False

            left, top, right, bottom = pengyouquan_region
            width, height = right - left, bottom - top

            if width <= 0 or height <= 0 or left < 0 or top < 0:
                print("❌ 朋友圈窗口区域无效")
                return False

            # 截取朋友圈窗口区域
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # OCR识别所有文字
            result = ocr_engine_ref.recognize_text(screenshot)

            if not result or len(result) == 0:
                print("⚠️ OCR识别结果为空")
                return False

            print(f"📋 本次识别到 {len(result)} 行文字")

            # 提取用户名候选
            username_candidates = _extract_first_line_username_candidates(result, pengyouquan_region)

            # 收集点赞按钮位置
            dianzan_positions = _collect_dianzan_positions_in_region(
                pengyouquan_region,
                screenshot=screenshot,
                ocr_engine_ref=ocr_engine_ref,
                username_candidates=username_candidates
            )

            # 映射用户名到点赞按钮
            mapped_posts = _map_username_to_first_dianzan(username_candidates, dianzan_positions)

            if not mapped_posts:
                print("⚠️ 未找到可点赞的帖子")
                return False

            print(f"🔗 找到 {len(mapped_posts)} 个可点赞的帖子")

            # 对第一个可见帖子执行点赞
            user_name, post_id, name_pos, dianzan_pos = mapped_posts[0]
            print(f"👍 正在点赞: {user_name}, 点赞按钮位置: {dianzan_pos}")

            if check_and_perform_dianzan(dianzan_pos, stop_flag_func=None):
                print(f"✅ 成功点赞: {user_name}")

                # 滚动到下一个帖子
                print("⬇️ 滚动到下一个帖子...")
                pyautogui.press('down')
                time.sleep(1)

                return True
            else:
                print(f"❌ 点赞失败: {user_name}")
                return False

        except Exception as e:
            print(f"❌ 自动识别辅助点赞出错: {e}")
            return False
    else:
        print("⚠️ RapidOCR不可用，无法执行自动识别")
        return False

'''

    insert_marker = '# ==================== 主程序 ===================='
    if insert_marker in content and auto_detect_func not in content:
        content = content.replace(insert_marker, auto_detect_func + '\n' + insert_marker)
        write_file(core_engine_path, content)
        print("[OK] Added auto_detect_and_like_current_post function")
        return True
    else:
        print("[WARN] Could not insert auto-detect function")
        return False

def modify_aux_like_gui(gui_path):
    """修改GUI中的辅助点赞功能为自动识别模式"""
    content = read_file(gui_path)

    old_code = '''    def execute_aux_like_once(self, from_hotkey=False):
        """执行一次辅助点赞动作：当前点 + 偏移点 + 可选向下滚动"""
        if from_hotkey and hasattr(self, 'aux_like_enable_checkbox') and not self.aux_like_enable_checkbox.isChecked():
            return

        with self._aux_like_lock:
            now = time.time()
            if now - self._aux_like_last_trigger_time < 0.25:
                return
            self._aux_like_last_trigger_time = now

        original_pause = pyautogui.PAUSE
        original_min_duration = getattr(pyautogui, 'MINIMUM_DURATION', 0.0)
        original_min_sleep = getattr(pyautogui, 'MINIMUM_SLEEP', 0.0)

        try:
            offset_x = self.aux_like_offset_x_spinbox.value()
            offset_y = self.aux_like_offset_y_spinbox.value()
            delay_ms = self.aux_like_delay_spinbox.value()
            scroll_lines = self.aux_like_scroll_lines_spinbox.value() if hasattr(self, 'aux_like_scroll_lines_spinbox') else 0
            scroll_delay_ms = self.aux_like_scroll_delay_spinbox.value() if hasattr(self, 'aux_like_scroll_delay_spinbox') else 0

            # 临时关闭PyAutoGUI全局延时，确保0ms场景也能极快执行
            pyautogui.PAUSE = 0
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0

            current_pos = pyautogui.position()
            target_x = current_pos.x + offset_x
            target_y = current_pos.y + offset_y

            trigger_source = "F10" if from_hotkey else "测试按钮"
            self.update_status(
                f"🖱️ 辅助点赞({trigger_source})：先点({current_pos.x},{current_pos.y})，再双击({target_x},{target_y})，下滚{scroll_lines}行({scroll_delay_ms}ms延时)",
                "#FF69B4"
            )

            pyautogui.click(current_pos.x, current_pos.y)
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)
            pyautogui.doubleClick(target_x, target_y)

            # 执行完成后将鼠标移回原始位置，避免影响后续操作
            pyautogui.moveTo(current_pos.x, current_pos.y, duration=0)

            # 下滚前的延时
            if scroll_delay_ms > 0 and scroll_lines > 0:
                time.sleep(scroll_delay_ms / 1000.0)

            # 完成全部动作后，按设置向下滚动指定行数
            if scroll_lines > 0:
                pyautogui.scroll(-int(scroll_lines))

        except Exception as e:
            self.update_status(f"❌ 辅助点赞执行失败: {e}", "#f44336")
        finally:
            pyautogui.PAUSE = original_pause
            pyautogui.MINIMUM_DURATION = original_min_duration
            pyautogui.MINIMUM_SLEEP = original_min_sleep'''

    new_code = '''    def execute_aux_like_once(self, from_hotkey=False):
        """执行一次辅助点赞动作：自动识别当前帖子 + 一键点赞 + 切换下一个"""
        if from_hotkey and hasattr(self, 'aux_like_enable_checkbox') and not self.aux_like_enable_checkbox.isChecked():
            return

        with self._aux_like_lock:
            now = time.time()
            if now - self._aux_like_last_trigger_time < 0.25:
                return
            self._aux_like_last_trigger_time = now

        original_pause = pyautogui.PAUSE
        original_min_duration = getattr(pyautogui, 'MINIMUM_DURATION', 0.0)
        original_min_sleep = getattr(pyautogui, 'MINIMUM_SLEEP', 0.0)

        try:
            # 临时关闭PyAutoGUI全局延时，确保0ms场景也能极快执行
            pyautogui.PAUSE = 0
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0

            trigger_source = "F10" if from_hotkey else "测试按钮"
            self.update_status(
                f"🤖 自动辅助点赞({trigger_source})：正在识别当前可见帖子...",
                "#FF69B4"
            )

            # 调用核心引擎的自动识别点赞功能
            success = auto_detect_and_like_current_post(ocr_engine_ref=ocr_engine)

            if success:
                self.update_status(
                    f"✅ 自动辅助点赞成功！已点赞并切换到下一个帖子",
                    "#2ecc71"
                )
            else:
                self.update_status(
                    f"⚠️ 自动辅助点赞失败，请确保朋友圈窗口可见",
                    "#f39c12"
                )

        except Exception as e:
            self.update_status(f"❌ 辅助点赞执行失败: {e}", "#f44336")
        finally:
            pyautogui.PAUSE = original_pause
            pyautogui.MINIMUM_DURATION = original_min_duration
            pyautogui.MINIMUM_SLEEP = original_min_sleep'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        write_file(gui_path, content)
        print("[OK] Modified execute_aux_like_once to auto-detect mode")
        return True
    else:
        print("[WARN] Could not find execute_aux_like_once to replace")
        return False

def update_aux_like_hint(gui_path):
    """更新辅助点赞提示文本"""
    content = read_file(gui_path)

    old_hint = '启用F10辅助点赞（每按一次F10仅执行一次）'
    new_hint = '启用F10自动辅助点赞（自动识别当前帖子，一键点赞并切换下一个）'

    if old_hint in content:
        content = content.replace(old_hint, new_hint)
        write_file(gui_path, content)
        print("[OK] Updated auxiliary like hint text")
        return True
    else:
        print("[WARN] Could not find hint text to update")
        return False

def main():
    print("=" * 60)
    print("WeChat Auto-Likes 优化补丁")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    core_engine_path = os.path.join(base_dir, 'wechat_core_engine.py')
    gui_path = os.path.join(base_dir, 'wechat_automation_gui.py')

    # 1. 修复弹窗验证
    print("\\n[1/5] 修复弹窗验证...")
    if os.path.exists(core_engine_path):
        apply_popup_verification_fix(core_engine_path)
    else:
        print(f"[ERROR] File not found: {core_engine_path}")

    # 2. 添加OCR后备
    print("\\n[2/5] 添加OCR后备点赞方案...")
    if os.path.exists(core_engine_path):
        add_ocr_fallback(core_engine_path)
    else:
        print(f"[ERROR] File not found: {core_engine_path}")

    # 3. 添加自动识别函数
    print("\\n[3/5] 添加自动识别辅助点赞函数...")
    if os.path.exists(core_engine_path):
        add_auto_detect_like_function(core_engine_path)
    else:
        print(f"[ERROR] File not found: {core_engine_path}")

    # 4. 修改GUI
    print("\\n[4/5] 修改GUI辅助点赞功能...")
    if os.path.exists(gui_path):
        modify_aux_like_gui(gui_path)
        update_aux_like_hint(gui_path)
    else:
        print(f"[ERROR] File not found: {gui_path}")

    # 5. 验证语法
    print("\\n[5/5] 验证语法...")
    all_ok = True
    if os.path.exists(core_engine_path):
        if check_syntax(core_engine_path):
            print(f"[OK] Core engine syntax OK")
        else:
            print(f"[ERROR] Core engine syntax error!")
            all_ok = False

    if os.path.exists(gui_path):
        if check_syntax(gui_path):
            print(f"[OK] GUI syntax OK")
        else:
            print(f"[ERROR] GUI syntax error!")
            all_ok = False

    print("\\n" + "=" * 60)
    if all_ok:
        print("补丁应用完成！")
        print("请运行 python wechat_automation_gui.py 启动应用")
    else:
        print("应用过程中出现错误，请检查上述输出")
        print("如需恢复，请运行: git checkout -- wechat_core_engine.py wechat_automation_gui.py")
    print("=" * 60)

if __name__ == '__main__':
    main()
