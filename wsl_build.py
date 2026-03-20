#!/usr/bin/env python3
"""
wsl_build.py - 在 WSL 内编译 YoloMirror Fabric 模组
用法: python3 wsl_build.py
"""

import subprocess
import sys
import os

# ============================================================
# 硬编码配置
# ============================================================

# WSL 内 JDK 路径
JAVA_HOME = "/root/JDKs/zulu21/zulu21.48.17-ca-jdk21.0.10-linux_x64"

# 代理地址
PROXY_HOST = "127.0.0.1"
PROXY_PORT = "7890"  # ← 如果代理端口不对请修改这里

# 项目根目录（WSL 绝对路径，hardcode）
PROJECT_DIR = "/mnt/d/aaaStuffsaaa/from_git/github/YoloMirror"

# ============================================================

def main():
    proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"

    # 设置环境变量
    env = os.environ.copy()
    env["JAVA_HOME"] = JAVA_HOME
    env["PATH"] = f"{JAVA_HOME}/bin:{env.get('PATH', '')}"
    env["HTTP_PROXY"] = proxy_url
    env["HTTPS_PROXY"] = proxy_url
    env["http_proxy"] = proxy_url
    env["https_proxy"] = proxy_url

    # Gradle 代理参数（每个都是独立 list 元素，不经过 shell 解析）
    gradle_proxy_args = [
        f"-Dhttp.proxyHost={PROXY_HOST}",
        f"-Dhttp.proxyPort={PROXY_PORT}",
        f"-Dhttps.proxyHost={PROXY_HOST}",
        f"-Dhttps.proxyPort={PROXY_PORT}",
        f"-Dhttp.nonProxyHosts=localhost|127.0.0.1",
    ]

    gradlew_path = os.path.join(PROJECT_DIR, "gradlew")

    print("=" * 60)
    print("YoloMirror Fabric Mod Builder (WSL)")
    print("=" * 60)
    print(f"[*] JAVA_HOME : {JAVA_HOME}")
    print(f"[*] 代理      : {proxy_url}")
    print(f"[*] 项目路径  : {PROJECT_DIR}")
    print("=" * 60)
    print()

    # /mnt/d 是 9p 挂载，CRLF 换行，不能直接 execve。
    # 把去掉 \r 后的内容写到 /tmp/gradlew_fixed 临时文件，
    # 再用 bash /tmp/gradlew_fixed 执行，$0 指向文件，脚本内部路径解析正常。
    tmp_gradlew = "/tmp/gradlew_fixed"
    print(f"[*] 读取 gradlew 并去除 CRLF -> {tmp_gradlew}")
    with open(gradlew_path, "rb") as f:
        gradlew_content = f.read().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    with open(tmp_gradlew, "wb") as f:
        f.write(gradlew_content)
    os.chmod(tmp_gradlew, 0o755)

    # 确认 java 可用
    java_bin = os.path.join(JAVA_HOME, "bin", "java")
    wrapper_jar = os.path.join(PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.jar")
    print(f"[*] 检查 java  : {java_bin} -> {'OK' if os.path.exists(java_bin) else 'NOT FOUND!'}")
    if not os.path.exists(java_bin):
        print("[✗] java 不存在，中止")
        sys.exit(1)

    # gradle-wrapper.jar 不存在时自动下载
    if not os.path.exists(wrapper_jar):
        print(f"[*] gradle-wrapper.jar 不存在，正在下载 ...")
        wrapper_jar_url = (
            "https://raw.githubusercontent.com/gradle/gradle/v9.2.1/"
            "gradle/wrapper/gradle-wrapper.jar"
        )
        os.makedirs(os.path.dirname(wrapper_jar), exist_ok=True)
        dl = subprocess.run(
            [
                "curl", "-fSL",
                "--proxy", proxy_url,
                "-o", wrapper_jar,
                wrapper_jar_url,
            ],
            env=env,
        )
        if dl.returncode != 0 or not os.path.exists(wrapper_jar):
            print("[✗] gradle-wrapper.jar 下载失败，中止")
            sys.exit(1)
        print(f"[*] 下载完成: {wrapper_jar}")
    else:
        print(f"[*] 检查 jar   : {wrapper_jar} -> OK")
    print()

    cmd = ["bash", tmp_gradlew, "build"] + gradle_proxy_args + ["--stacktrace"]
    gradle_args_str = " ".join(gradle_proxy_args)
    print(f"[*] 执行: bash {tmp_gradlew} build {gradle_args_str} --stacktrace")
    print()

    result = subprocess.run(
        cmd,
        env=env,
        cwd=PROJECT_DIR,
    )
    print(f"[*] Gradle 退出码: {result.returncode}")

    print()
    print("=" * 60)
    if result.returncode == 0:
        print("[✓] 编译成功！")
        print(f"[*] 产物路径: {PROJECT_DIR}/build/libs/")
    else:
        print(f"[✗] 编译失败，退出码: {result.returncode}")
        sys.exit(result.returncode)
    print("=" * 60)


if __name__ == "__main__":
    main()
