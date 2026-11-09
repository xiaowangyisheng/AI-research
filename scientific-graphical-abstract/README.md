# 科研绘图核武 Skill

将已有科研示意图、手绘图或生成图，整理成可在 Adobe Illustrator 中继续编辑的 SVG。也可以结合参照图和论文摘要，先改绘科研机制图，再制作可编辑版本。

## 适用场景

- 论文 Graphical Abstract、机制图和实验设计图。
- 已有图片的文字、关键箭头与图形轮廓需要继续修改。
- 参照已有画面，结合研究摘要重新组织版式和科学关系。

## 工作流程

1. 准备一张参照图，或已经画好、生成好的示意图。
2. 选择 **GPT-6 astra**，推理强度设为 **High**。模型选择由运行环境控制，安装 Skill 不会自动切换模型。
3. 明确需要“保留原图转 SVG”，还是“结合摘要改绘后转 SVG”。
4. 调用 `$scientific-graphical-abstract`。根据任务范围，整理图形路径、原生文字、主要箭头、高清预览和编辑说明。
5. 在 Illustrator 中打开 SVG，继续修改并按需另存为 `.ai`。

已有原生 SVG 等可编辑文件时，优先保留并修改原对象。图片转换后的插画可能是彩色描摹路径；具体可编辑层级以交付说明为准。

## 安装

把本仓库中的 `scientific-graphical-abstract/` 文件夹复制到 Codex 的 skills 目录：

```text
~/.codex/skills/scientific-graphical-abstract/
```

如果设置了 `CODEX_HOME`，使用 `$CODEX_HOME/skills/`。已有同名版本时请先备份。重新加载 Skill 列表或新开聊天后即可调用。

## 使用示例

```text
使用 $scientific-graphical-abstract，把附件图转换为 Adobe Illustrator
可编辑 SVG。保留科学内容、构图和配色，文字可直接修改，关键箭头
独立编辑，并提供高清 PNG 和简短编辑说明。
```

结合摘要重新设计时，请额外提供科学摘要，并说明参照图用于内容还是风格。

## 仓库结构

```text
scientific-graphical-abstract/
├── SKILL.md              # Skill 入口和工作流程
├── agents/openai.yaml    # 界面展示信息
├── references/           # 生成、SVG 转换和交付说明
└── scripts/              # SVG 结构检查、交付打包及测试
使用说明.md               # 安装与使用简要说明
```

运行随附的脚本测试：

```bash
python3 -m unittest discover -s scientific-graphical-abstract/scripts -p test_helpers.py -v
```

详细说明见 [使用说明.md](使用说明.md)。
