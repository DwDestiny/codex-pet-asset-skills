# Codex Pet-like 动画行参考

这份参考来自官方 `hatch-pet` skill 的素材处理规格，用于需要做 Codex pet-like spritesheet 时。普通网页动画不必强制使用这套 8x9 atlas。

## Atlas 规格

- 尺寸：`1536x1872`
- 网格：8 列 x 9 行
- 单格：`192x208`
- 背景：透明
- 未使用格子：必须全透明

## 行定义

| Row | State | Used columns | Durations |
| --- | --- | ---: | --- |
| 0 | idle | 0-5 | 280, 110, 110, 140, 140, 320 ms |
| 1 | running-right | 0-7 | 120 ms each, final 220 ms |
| 2 | running-left | 0-7 | 120 ms each, final 220 ms |
| 3 | waving | 0-3 | 140 ms each, final 280 ms |
| 4 | jumping | 0-4 | 140 ms each, final 280 ms |
| 5 | failed | 0-7 | 140 ms each, final 240 ms |
| 6 | waiting | 0-5 | 150 ms each, final 260 ms |
| 7 | running | 0-5 | 120 ms each, final 220 ms |
| 8 | review | 0-5 | 150 ms each, final 280 ms |

## 状态语义

- `idle`：低干扰呼吸/眨眼，第一帧要能当静态 reduced-motion 形态。
- `running-right`：向右移动，靠身体、肢体和道具运动表达，不要速度线和尘土。
- `running-left`：向左移动；只有角色左右对称时才可由 right 镜像。
- `waving`：靠手/爪姿态表达，不要波浪线和符号。
- `jumping`：靠身体高度和姿态表达，不要影子、落地尘、冲击线。
- `failed`：失败/沮丧/眩晕，可有贴在主体上的小泪珠、烟雾或星星，不要漂浮符号。
- `waiting`：等待时的小动作，区别于 idle。
- `running`：任务执行中，不是脚步跑步，不要方向位移。
- `review`：审查/思考/聚焦，靠眼神、倾身、头部动作表达。

## QA 红线

- 不能有文字、标签、帧号、网格线、UI、代码片段。
- 不能有白底、黑底、棋盘格背景、场景背景。
- 不能有投影、地面、光晕、半透明拖影、漂浮粒子。
- 不能跨格、裁切、混入相邻帧残片。
- 不能把同一张图简单缩放/旋转当成动画。
