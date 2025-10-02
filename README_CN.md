# SoraCleaner-Sora2视频水印去除工具

[English Version](./README.md)

一个强大的视频水印去除工具，使用 AI 驱动的修复技术。工具会自动检测视频方向（横屏/竖屏）并应用相应的水印去除配置。

## 功能特性

- **多水印去除**：一次性去除视频中的多个水印
- **自动方向检测**：自动检测横屏/竖屏并使用相应的水印位置配置
- **音频保留**：处理后的视频保持原始音轨
- **批量处理**：支持处理整个目录的视频文件
- **AI 驱动修复**：使用 STTN（时空变换网络）实现无缝水印去除

## 系统要求

- Python >= 3.12
- FFmpeg 和 FFprobe 已安装并在 PATH 中
- 支持 CUDA 的 GPU（推荐，加速处理）

## 安装步骤

1. 克隆仓库（包含子模块）：

```bash
git clone https://github.com/zstar1003/SoraCleaner
cd SoraCleaner
```

2. 安装依赖：

```bash
uv sync
```

## 配置说明

编辑 `config.yaml` 配置水印位置：

```yaml
watermark:
  positions_landscape:  # 横屏视频的水印位置
    - [35, 585, 176, 638]   # 格式：[xmin, ymin, xmax, ymax]
    - [30, 68, 179, 118]
    - [1112, 321, 1266, 367]
  positions_portrait:  # 竖屏视频的水印位置
    - [28, 1029, 175, 1091]
    - [538, 604, 685, 657]
    - [25, 79, 173, 136]
  ckpt_p: "./weights/sttn.pth"
  mask_expand: 30          # 遮罩扩展像素数
  neighbor_stride: 10      # 修复时的时间跨度
```

### 如何获取水印位置

1. 在视频播放器或图像编辑器中打开视频
2. 记录水印左上角和右下角的像素坐标 (x, y)
3. 将位置添加为 `[xmin, ymin, xmax, ymax]` 格式到相应配置段

## 使用方法

### 处理单个视频

```bash
python main.py --input /path/to/video.mp4
```

### 批量处理目录

```bash
python main.py --input /path/to/video/directory/
```

工具会执行以下步骤：

1. 自动检测视频方向（横屏/竖屏）
2. 从配置中选择相应的水印位置
3. 从视频中提取帧
4. 使用 AI 修复技术去除水印
5. 重新生成视频并保留原始音频
6. 保存输出为 `{原文件名}_output.mp4`

## 工作原理

1. **视频分析**：检测 FPS 和方向（横屏/竖屏）
2. **帧提取**：从视频中提取所有帧
3. **方向检测**：判断视频是横屏（宽 >= 高）还是竖屏
4. **水印遮罩**：为所有配置的水印位置创建遮罩
5. **AI 修复**：使用 STTN 模型自然填充遮罩区域
6. **视频重建**：将处理后的帧与原始音频合并

## 项目结构

```
.
├── config.yaml           # 配置文件
├── main.py              # 主程序入口
├── modules/
│   ├── __init__.py
│   ├── erase.py         # 水印去除逻辑
│   └── sttn.py          # STTN 模型实现
├── utils/
│   ├── image_utils.py   # 图像处理工具
│   ├── logging_utils.py # 日志工具
│   └── video_utils.py   # 视频处理工具
├── weights/             # 模型权重目录
└── STTN/               # STTN 子模块
```

## 常见问题

**找不到 FFmpeg**

- 确保 FFmpeg 和 FFprobe 已安装并在系统 PATH 中

**CUDA 内存不足**

- 处理较短的视频或降低配置中的 `neighbor_stride` 值
- 使用 CPU 模式（较慢但无需 GPU）

**水印未完全去除**

- 在 config.yaml 中调整水印坐标
- 增加 `mask_expand` 值以扩大覆盖范围

**音视频不同步**

- 检查原始视频的 FPS 是否正确检测
- 确保 FFmpeg 是最新版本

## 许可证

本项目仅供教育和研究目的使用。

## 致谢

- [STTN](https://github.com/researchmm/STTN) - 用于视频修复的时空变换网络
- [KLing-Video-WatermarkRemover-Enhancer](https://github.com/chenwr727/KLing-Video-WatermarkRemover-Enhancer) - 参考了此项目的基础代码
