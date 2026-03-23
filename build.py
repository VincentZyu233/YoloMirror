#!/usr/bin/env python3
"""
win_build.py - 在 Windows 上编译 YoloMirror Fabric 模组
用法: python win_build.py [--version <version>]
"""

import subprocess
import sys
import os
import urllib.request
import re
import argparse

# ============================================================
# 硬编码配置
# ============================================================

# Windows 上的 JDK 路径
JAVA_HOME = r"D:\SSoftwareFiles\JDKs\zulu21.42.19-ca-jdk21.0.7-win_x64"

# 代理地址
PROXY_HOST = "192.168.31.233"
PROXY_PORT = "7890"

# 项目根目录
PROJECT_DIR = r"D:\aaaStuffsaaa\from_git\github\YoloMirror"

# gradle-wrapper.jar 下载地址（与 Gradle 版本无关，用固定的官方地址）
WRAPPER_JAR_URL = (
    "https://raw.githubusercontent.com/gradle/gradle/v9.2.1/"
    "gradle/wrapper/gradle-wrapper.jar"
)

# ============================================================

def ensure_wrapper_jar(jar_path: str, proxy_url: str):
    """如果 gradle-wrapper.jar 不存在则自动下载"""
    if os.path.exists(jar_path):
        print(f"[*] gradle-wrapper.jar 已存在，跳过下载")
        return

    print(f"[*] gradle-wrapper.jar 不存在，正在下载 ...")
    print(f"    URL  : {WRAPPER_JAR_URL}")
    print(f"    代理 : {proxy_url}")

    proxy_handler = urllib.request.ProxyHandler({
        "http": proxy_url,
        "https": proxy_url,
    })
    opener = urllib.request.build_opener(proxy_handler)

    try:
        with opener.open(WRAPPER_JAR_URL, timeout=60) as resp:
            data = resp.read()
        os.makedirs(os.path.dirname(jar_path), exist_ok=True)
        with open(jar_path, "wb") as f:
            f.write(data)
        print(f"[*] 下载完成：{jar_path}  ({len(data):,} bytes)")
    except Exception as e:
        print(f"[✗] 下载失败: {e}")
        sys.exit(1)


def update_mod_version(gradle_properties_path: str, new_version: str):
    """更新 gradle.properties 中的 mod_version"""
    # 验证版本号格式
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', new_version):
        print(f"[✗] 版本号格式无效: {new_version}")
        print("    版本号只能包含字母、数字、下划线、横杠和点")
        sys.exit(1)

    # 读取文件
    with open(gradle_properties_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换 mod_version
    new_content = re.sub(r'^mod_version\s*=.*$', f'mod_version = {new_version}', content, flags=re.MULTILINE)

    # 写入文件
    with open(gradle_properties_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[*] 已更新 mod_version 为: {new_version}")


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="YoloMirror Fabric Mod Builder")
    parser.add_argument('--version', type=str, help="指定新的模组版本号")
    args = parser.parse_args()

    proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"
    java_exe = os.path.join(JAVA_HOME, "bin", "java.exe")
    jar_path = os.path.join(PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.jar")
    gradle_properties_path = os.path.join(PROJECT_DIR, "gradle.properties")

    # 确保 wrapper jar 存在
    ensure_wrapper_jar(jar_path, proxy_url)

    # 如果指定了版本号，更新 gradle.properties
    if args.version:
        update_mod_version(gradle_properties_path, args.version)

    # 设置环境变量
    env = os.environ.copy()
    env["JAVA_HOME"] = JAVA_HOME
    env["PATH"] = f"{JAVA_HOME}\\bin;{env.get('PATH', '')}"
    env["HTTP_PROXY"] = proxy_url
    env["HTTPS_PROXY"] = proxy_url
    env["http_proxy"] = proxy_url
    env["https_proxy"] = proxy_url

    # Gradle 代理参数
    gradle_proxy_args = [
        f"-Dhttp.proxyHost={PROXY_HOST}",
        f"-Dhttp.proxyPort={PROXY_PORT}",
        f"-Dhttps.proxyHost={PROXY_HOST}",
        f"-Dhttps.proxyPort={PROXY_PORT}",
        "-Dhttp.nonProxyHosts=localhost|127.0.0.1",
    ]

    print("=" * 60)
    print("YoloMirror Fabric Mod Builder (Windows)")
    print("=" * 60)
    print(f"[*] JAVA_HOME : {JAVA_HOME}")
    print(f"[*] 代理      : {proxy_url}")
    print(f"[*] 项目路径  : {PROJECT_DIR}")
    print("=" * 60)
    print()

    # 用 java -jar gradle-wrapper.jar 直接启动，不依赖 gradlew.bat
    cmd = (
        [java_exe]
        + gradle_proxy_args
        + [
            "-jar", jar_path,
            "build",
            "--stacktrace",
        ]
    )

    gradle_args_str = " ".join(gradle_proxy_args)
    print(f"[*] 执行: java {gradle_args_str} -jar gradle-wrapper.jar build --stacktrace")
    print()

    result = subprocess.run(cmd, env=env, cwd=PROJECT_DIR)

    print()
    print("=" * 60)
    if result.returncode == 0:
        print("[✓] 编译成功！")
        print(f"[*] 产物路径: {PROJECT_DIR}\\build\\libs\\")
    else:
        print(f"[✗] 编译失败，退出码: {result.returncode}")
        sys.exit(result.returncode)
    print("=" * 60)


if __name__ == "__main__":
    main()
