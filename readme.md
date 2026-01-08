以下是你提供内容的 优雅、规范、可直接用于文档或 README 的补全版本，符合 Python ≥3.10 要求，并采用标准项目安装格式：

🚀 安装 Bestman 及机器人 SDK

✅ 要求：Python ≥ 3.10

- 创建 Conda 环境（推荐）

  ```
  conda create -n bestman python=3.10 -y
  conda activate bestman

- 安装 bestman 主包（可编辑模式）

```
cd ./bestman
pip install -e .
```

- 按需安装机器人驱动支持

🔧 XArm 支持（UFACTORY）

``` 
pip install bestman[xarm]
```

运行示例：

```
# 在项目根目录下运行
python ./examples/xarm/xarm7/00_init_from_class.py
python ./examples/xarm/xarm7/00_init_from_factory.py

更多示例见 ./examples/xarm/xarm7
```

🔧 Piper 机械臂支持（AgileX Robotics）

```
pip install bestman[piper]
```

运行示例：

```
暂无
```


🔧 Startouch 

```
pip install bestman[startouch]
```

运行示例：

```
暂无
```



- 验证安装

```
cd examples
python -c "import bestman; print(bestman.version)"
```



💡 提示

- 所有可选依赖均通过 extras_require 定义，避免不必要的包安装。

- 若遇网络问题，可添加 -i https://pypi.tuna.tsinghua.edu.cn/simple 使用国内镜像。

- 开发者建议安装完整依赖：  
    
    ```
    pip install -e ".[all]"
    ```



📌 版本兼容性说明  
本项目不严格地测试于 Python 3.10。



目前只有XArm7的wrapper

