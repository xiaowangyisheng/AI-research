# 独立背景与 Adobe 交付包

## 背景原则

用户只要背景时，交付**仅背景图**，不重新生成或扁平化其现有主体；截图中的边框、选中框和 UI 不进入背景。
背景应补足空间层次，不增加新的生物学含义。默认不放 DNA、细胞、分子、网格、光斑或装饰箭头。
先读主体配色、标签位置与空间；常见方案是近白浅蓝灰 + 很淡的紫/米色，文字与结论区更接近白色。深度应在最终尺寸下判断，而不是只在放大预览上判断。
用户未要求透明时可生成白底浅色背景；要求透明时使用真实透明通道。独立 PNG 的“正常”底层用法与“正片叠底”顶层用法均可说明，不能把透明与正片叠底混为一谈。

背景提示词框架：

```text
Standalone background plate ONLY, no foreground artwork, no text, no labels,
no scientific symbols, no arrows, no screenshot UI. Landscape [ratio].
Existing figure palette: [colors]; keep [label regions] near-white.
Broad, very pale, smoothly blended [colors] with restrained transitions.
No distinct decorative motifs, noisy texture, dark vignette or shiny rendering.
Background must remain subordinate to black labels and existing artwork.
```

使用 GPT 图像工具生成并保留提示词。用户要求独立背景时，不用程序生成渐变代替图像工具；若用户明确要求可编辑矢量背景，才按其选择制作矢量渐变版本。

## Illustrator 操作说明：先诊断，再选一种主方案

当次讲解菜单或操作时核对官方文档，尤其版本差异。不要给用户多套相互矛盾的层级指令。

**优先：普通底层背景。**适合前景本来透明或能单独隐藏整张白底的文件。

1. 另存副本，创建独立 Background 图层。
2. 文件 → 置入 PNG；说明链接/嵌入的区别，便于交付通常嵌入。
3. 背景铺满画板，使用对齐到画板居中；比例不同则等比覆盖后裁切，不拉伸组织主体。
4. 将 Background 置于最底层，正常模式；仅调背景不透明度，锁层。

**备选：顶层正片叠底色调层。**适合描摹文件含大量不透明白底、用户不想逐块清理的情况。

1. 创建最上层 Background tone，置入独立浅色背景并覆盖画板。
2. 只选背景图片，窗口 → 透明度 → 正片叠底。
3. 从较轻的不透明度试起，例如 40%–70%；不是所有背景都必须使用同一个数值。
4. 说明：黑文字仍清楚，但主体颜色会轻微变暗/染色；如果要求原色不变，应清理单独白底并改用底层正常模式。
5. 锁定色调层，不要降低整个前景/文本图层透明度。

不要建议全选相同白色并删除：骨孔、细胞内部、注射器和文字反白可能同为白色。
不能承诺“顶层正片叠底完全不改变主体颜色”。合成效果预览须标注为预览，不能覆盖可编辑主文件。

官方说明入口：

- https://helpx.adobe.com/illustrator/using/place-multiple-files.html
- https://helpx.adobe.com/illustrator/using/manage-linked-and-embedded-files.html
- https://helpx.adobe.com/illustrator/using/transparency-blending-modes-alt.html

## 打包结构：按本次授权范围裁剪

完整任务建议如下；只要求背景时不补造 SVG/PDF，只要求 SVG 时也不自动画新背景。

```text
study_graphical_abstract_vNN/
  01_original/       原始生成 PNG 或用户授权复制的内容母版
  02_editable/       最终 SVG；真实生成的 AI/PDF（如有）
  03_background/     仅背景 PNG/SVG，不合并主体
  04_preview/        最终渲染预览；可选合成预览
  05_notes/          Illustrator 打开/图层/字体/背景说明、图注（如要求）
  06_provenance/     提示词、来源/证据表、QA、版本说明
  delivery_manifest.json
```

背景与主体分别可下载，并在 ZIP 中分目录保存。不把截图替代原始图，不把预览文件假称高分辨率源图。不要把未授权的全文稿件、临时依赖、缓存或 API 凭证打入包。

版本说明记录母版、改变了什么、保留了什么、未解决什么；不要收集无关个人路径或敏感信息。稿件顺序、图注字体等如被用户明确要求，作为项目约束记录，不强制每个项目都“十张图”或使用同一种字体。

## 文件清单与打包脚本

创建项目专属 JSON（下面文件名仅是示例，必须替换为实际存在且授权交付的文件）：

```json
{
  "project": "study_graphical_abstract",
  "version": "v01",
  "requested_model": "user-requested version or unspecified",
  "actual_model": "built-in image tool; exact version unverified",
  "illustrator_tested": false,
  "required_roles": ["original", "editable", "background", "preview", "instructions"],
  "files": [
    {"path": "01_original/figure.png", "role": "original"},
    {"path": "02_editable/figure.svg", "role": "editable", "editability": "paths-and-live-text"},
    {"path": "03_background/background.png", "role": "background"},
    {"path": "04_preview/figure.png", "role": "preview"},
    {"path": "05_notes/Illustrator操作说明.md", "role": "instructions"}
  ]
}
```

调用（脚本相对于本技能目录）：

```bash
python3 scripts/package_delivery.py --root /absolute/path/study_graphical_abstract_v01 --manifest /absolute/path/study_graphical_abstract_v01/delivery_manifest.json --output /absolute/path/study_graphical_abstract_v01.zip
```

脚本只打包清单内文件，检查重复/越界路径、缺失角色和空文件，写入 SHA-256 便于归档追踪，不覆盖已有 ZIP。`required_roles` 由实际任务范围决定，不能为了通过校验把背景伪标成其他角色。
脚本不保证 Illustrator 已实测或模型版本真实；这些元数据必须有工作记录支持。

## 最终检查与交付措辞

- 科学：证据强度、箭头、标签、上下标、处理顺序、来源边界。
- 视觉：最终尺寸可读、插画风格连贯、背景不抢戏、边界不裁字、无重影。
- 编辑：文本/路径/位图实际数量和声明一致，无失效外链，字体说明清楚。
- 归档：原图非破坏保存，背景独立，最新用户编辑没有被旧版覆盖，ZIP 可解包。
- 完成说明：提供主文件、背景、完整包链接；告知编辑限制、是否在 Illustrator 内实测及核心打开步骤。不要把技能自身代码当作用户的图稿交付文件。
