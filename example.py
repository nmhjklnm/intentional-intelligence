from typing import Literal, assert_never

Command = Literal["start", "stop", "restart", "pause"]  # 新增 "pause"

def execute_command(cmd: Command) -> None:
    match cmd:
        case "start":
            print("启动服务")
        case "stop":
            print("停止服务")
        case "restart":
            print("重启服务")
        case _:
            assert_never(cmd)  # 这里会报错！